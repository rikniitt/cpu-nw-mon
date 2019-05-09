# -*- coding: utf-8 -*-

import os
import sqlite3
from monitor.helper import dt_now_str
from monitor.log import log


def connect():
    """ Get database connection """
    path = os.getenv("DB_PATH")
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db

def create_observation():
    """ Create new observation """
    db = connect()
    cursor = db.cursor()

    sql = "INSERT INTO observation (created_at) VALUES (?)"
    values = (dt_now_str(), )

    log(sql + " (" + " ".join(values) + ")", "DEBUG")

    cursor.execute(sql, values)
    db.commit()

    return cursor.lastrowid

def get_observation(id):
    """ Get observation by id """
    db = connect()
    cursor = db.cursor()

    sql = "SELECT * FROM observation WHERE id = ?"
    values = (id, )

    log(sql + " (" + " ".join(map(str, values)) + ")", "DEBUG")

    cursor.execute(sql, values)
    return dict(cursor.fetchone())

def create_observation_raw(observation_id, description, output):
    """ Create new raw observation """
    db = connect()
    cursor = db.cursor()

    sql = "INSERT INTO observation_raw (observation_id, description, output) VALUES (?, ?, ?)"
    values = (observation_id, description, output)

    cursor.execute(sql, values)
    db.commit()

def create_network_connections(observation_id, network_connections):
    """ Create new network connections """
    db = connect()
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

def update_observation(observation_id, uptime, network_connections, process_count, free_memory):
    """ Update observation row """
    db = connect()
    cursor = db.cursor()

    sql = "UPDATE observation SET uptime = ?, users = ?, load_average_1 = ?, network_connections = ?, processes = ?, free_memory = ? WHERE id = ?"
    values = (
        uptime["uptime"],
        uptime["users"],
        uptime["load_average_1"],
        len(network_connections),
        process_count,
        free_memory["free"],
        observation_id
    )

    log(sql + " (" + " ".join(map(str, values)) + ")", "DEBUG")

    cursor.execute(sql, values)
    db.commit()

def get_observations_range(start, end):
    """ Get all observations between start and end datetimes """
    db = connect()
    cursor = db.cursor()

    sql = "SELECT * FROM observation WHERE created_at BETWEEN ? and ?"
    values = (start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"))

    log(sql + " (" + " ".join(map(str, values)) + ")", "DEBUG")

    return [dict(row) for row in cursor.execute(sql, values)]
