# -*- coding: utf-8 -*-

import re
from subprocess import check_output


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
