#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import click
import sqlite3
import time
import re
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from subprocess import call, check_output


def load_config():
    """ Read and parse the config file """
    config_path = Path(".") / "config.file"
    load_dotenv(dotenv_path=config_path)


def get_logger():
    """ Return the logger object """
    return logging.getLogger(__name__)

def setup_logging():
    """ Configure the logger object """
    lvl = os.getenv("LOG_LEVEL")
    path = os.getenv("LOG_PATH")

    logger = get_logger()
    logger.setLevel(lvl)

    filehandler = logging.FileHandler(path)
    filehandler.setLevel(lvl)
    filehandler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%d-%m %H:%M:%S"
    ))

    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(lvl)
    streamhandler.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)

def log(message, lvl="INFO"):
    """ Write to log """
    logger = get_logger()
    logger.log(getattr(logging, lvl), message)


def dt_now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def db_connect():
    """ Get database connection """
    path = os.getenv("DB_PATH")
    return sqlite3.connect(path)

def create_observation():
    """ Create new observation """
    db = db_connect()
    cursor = db.cursor()

    sql = "INSERT INTO observation (created_at) VALUES (?)"
    values = (dt_now_str(), )

    log(sql + " (" + " ".join(values) + ")", "DEBUG")

    cursor.execute(sql, values)
    db.commit()

    return cursor.lastrowid

def get_observation(id):
    """ Get observation by id """
    db = db_connect()
    cursor = db.cursor()

    sql = "SELECT * FROM observation WHERE id = ?"
    values = (id, )

    log(sql + " (" + " ".join(map(str, values)) + ")", "DEBUG")

    cursor.execute(sql, values)
    return cursor.fetchone()

def create_observation_raw(observation_id, description, output):
    """ Create new raw observation """
    db = db_connect()
    cursor = db.cursor()

    sql = "INSERT INTO observation_raw (observation_id, description, output) VALUES (?, ?, ?)"
    values = (observation_id, description, output)

    cursor.execute(sql, values)
    db.commit()

def create_network_connections(observation_id, network_connections):
    db = db_connect()
    cursor = db.cursor()

    sql = "INSERT INTO network_connection (observation_id, command, pid, user, node, name) VALUES (?, ?, ?, ?, ?, ?)"

    for con in network_connections:
        values = (
            observation_id,
            con["command"],
            con["pid"],
            con["user"],
            con["node"],
            con["name"]
        )

        log(sql + " (" + " ".join(map(str, values)) + ")", "DEBUG")

        cursor.execute(sql, values)
        db.commit()

def update_observation(observation_id, uptime, network_connections):
    """ Create new raw observation """
    db = db_connect()
    cursor = db.cursor()

    sql = "UPDATE observation SET uptime = ?, users = ?, load_average = ?, network_connections = ? WHERE id = ?"
    values = (
        uptime["uptime"],
        uptime["users"],
        uptime["load_average"],
        len(network_connections),
        observation_id
    )

    log(sql + " (" + " ".join(map(str, values)) + ")", "DEBUG")

    cursor.execute(sql, values)
    db.commit()



def get_uptime():
    return check_output("uptime").decode("utf-8")

def parse_uptime(cli_output):
    csv = cli_output.split(",")

    uptime = csv[1].strip()
    users = re.sub("[^0-9]", "", csv[2])

    load = re.search("load average:\s+(\d,\d\d)", cli_output).group(1)
    load = re.sub(",", ".", load)
    load_average = float(load)

    return {
        "uptime": uptime,
        "users": users,
        "load_average": load_average,
    }

def get_network_connections():
    return check_output(["lsof", "-i"]).decode("utf-8")

def parse_network_connections(cli_output):
    lines = cli_output.split("\n")[1:]
    parsed = []

    for line in lines:
        parts = line.split()
        if not parts:
            continue
        parsed.append({
            "command": parts[0],
            "pid": parts[1],
            "user": parts[2],
            "pid": parts[1],
            "node": parts[7],
            "name": " ".join(parts[8:])
        })

    return parsed


@click.group()
def monitor():
    """ CPU and network monitor """
    pass

@monitor.command("db-create")
def db_create():
    """ Create needed database file and tables """
    # touch file
    path = os.getenv("DB_PATH")
    open(path, "a").close()

    db = db_connect()
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

@monitor.command("db-console")
def db_console():
    """ Open sqlite3 console """
    path = os.getenv("DB_PATH")
    cmd = ["sqlite3", "-column", "-header", path]
    log("$ " + " ".join(cmd), "DEBUG")
    call(cmd)

@monitor.command("start")
def start():
    """ Start to monitor """
    sleep_time = int(os.getenv("INTERVAL"))

    while True:
        log("Monitor gathering observations at %s" % dt_now_str())

        obs_id = create_observation()
        obs = get_observation(obs_id)
        log("Created observation " + str(obs), "DEBUG")

        uptime_out = get_uptime()
        create_observation_raw(obs_id, "uptime", uptime_out)
        uptime = parse_uptime(uptime_out)
        log("Uptime: " + str(uptime), "DEBUG")

        net_cons_out = get_network_connections()
        create_observation_raw(obs_id, "network_connections", net_cons_out)
        net_cons = parse_network_connections(net_cons_out)

        create_network_connections(obs_id, net_cons)
        update_observation(obs_id, uptime, net_cons)

        log("Going to sleep for %d sec" % sleep_time)
        time.sleep(sleep_time)



if __name__ == "__main__":
    load_config()
    setup_logging()
    monitor()
