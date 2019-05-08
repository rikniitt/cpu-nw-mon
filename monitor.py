#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import click
import time
from datetime import datetime, timedelta
from subprocess import call
from monitor.helper import dt_now_str, load_config
from monitor.log import log, setup_logging
import monitor.db
import monitor.metrics
import monitor.plot
import monitor.table


@click.group()
def monitor_cli():
    """ CPU and network monitor """
    pass

@monitor_cli.command("db-create")
def db_create():
    """ Create needed database file and tables """
    # touch file
    path = os.getenv("DB_PATH")
    open(path, "a").close()

    db = monitor.db.connect()
    cursor = db.cursor()

    create_tables = (
        """
            CREATE TABLE IF NOT EXISTS observation (
                id INTEGER PRIMARY KEY,
                created_at TEXT,
                uptime TEXT,
                users INTEGER,
                load_average REAL,
                network_connections INTEGER
            )
        """,
        """
            CREATE TABLE IF NOT EXISTS observation_raw (
                id INTEGER PRIMARY KEY,
                observation_id INTEGER,
                description TEXT,
                output TEXT
            )
        """,
        """
            CREATE TABLE IF NOT EXISTS network_connection (
                id INTEGER PRIMARY KEY,
                observation_id INTEGER,
                command TEXT,
                pid INTEGER,
                user TEXT,
                node TEXT,
                name TEXT
            )
        """
    )

    log("Creating database tables")

    for sql in create_tables:
        log(sql, "DEBUG")
        cursor.execute(sql)
        db.commit()

    log("Database created")

@monitor_cli.command("db-console")
def db_console():
    """ Open sqlite3 console """
    path = os.getenv("DB_PATH")
    cmd = ["sqlite3", "-column", "-header", path]
    log("$ " + " ".join(cmd), "DEBUG")
    call(cmd)

@monitor_cli.command("start")
def start():
    """ Start to monitor """
    sleep_time = int(os.getenv("INTERVAL"))

    while True:
        log("Monitor gathering observations at %s" % dt_now_str())

        obs_id = monitor.db.create_observation()
        obs = monitor.db.get_observation(obs_id)
        log("Created observation " + str(obs), "DEBUG")

        uptime_out = monitor.metrics.get_uptime()
        monitor.db.create_observation_raw(obs_id, "uptime", uptime_out)
        uptime = monitor.metrics.parse_uptime(uptime_out)
        log("Uptime: " + str(uptime), "DEBUG")

        net_cons_out = monitor.metrics.get_network_connections()
        monitor.db.create_observation_raw(obs_id, "network_connections", net_cons_out)
        net_cons = monitor.metrics.parse_network_connections(net_cons_out)

        monitor.db.create_network_connections(obs_id, net_cons)
        monitor.db.update_observation(obs_id, uptime, net_cons)

        log("Going to sleep for %d sec" % sleep_time)
        time.sleep(sleep_time)

@monitor_cli.command("plot-stats")
@click.option("--start", "-s", required=False, type=click.DateTime(), default=None)
@click.option("--end", "-e", required=False, type=click.DateTime(), default=None)
def plot_stats(start, end):
    """ Plot statistics """
    if not start:
        start = datetime.now() - timedelta(hours=24)
    if not end:
        end = datetime.now()

    observations = monitor.db.get_observations_range(start, end)
    monitor.plot.observations(observations)

@monitor_cli.command("print-observations")
@click.option("--start", "-s", required=False, type=click.DateTime(), default=None)
@click.option("--end", "-e", required=False, type=click.DateTime(), default=None)
def plot_stats(start, end):
    """ Print observations """
    if not start:
        start = datetime.now() - timedelta(hours=24)
    if not end:
        end = datetime.now()

    observations = monitor.db.get_observations_range(start, end)
    print(monitor.table.observations(observations))

if __name__ == "__main__":
    load_config()
    setup_logging()
    monitor_cli()
