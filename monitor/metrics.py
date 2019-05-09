# -*- coding: utf-8 -*-

import re
from subprocess import check_output


def get_uptime():
    return check_output("uptime").decode("utf-8")

def parse_uptime(cli_output):
    csv = cli_output.split(",")

    uptime = csv[1].strip()
    users = int(re.sub("[^0-9]", "", csv[2]))

    matches = re.search("load average:\s+(\d,\d\d),\s+(\d,\d\d),\s+(\d,\d\d)", cli_output)
    load_1 = float(re.sub(",", ".", matches.group(1)))
    load_5 = float(re.sub(",", ".", matches.group(1)))
    load_15 = float(re.sub(",", ".", matches.group(1)))

    return {
        "uptime": uptime,
        "users": users,
        "load_average_1": load_1,
        "load_average_5": load_5,
        "load_average_15": load_15
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

def get_process_count():
    return check_output(["ps", "aux", "--sort=-pcpu"]).decode("utf-8")

def parse_process_count(cli_output):
    # It would better to use pipe and wc to get this, but py subprocess with pipes is clumsy
    return len(cli_output.split("\n")) - 1

def get_free_memory():
    return check_output("free").decode("utf-8")

def parse_free_memory(cli_output):
    matches = re.search("Mem:\s+(\d+)\s+(\d+)\s+(\d+)", cli_output)

    return {
        "total": int(matches.group(1)),
        "used": int(matches.group(2)),
        "free": int(matches.group(3))
    }
