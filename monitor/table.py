# -*- coding: utf-8 -*-

from tabulate import tabulate

def observations(observations):
    headers = observations[0].keys()
    rows = [obs.values() for obs in observations]
    return tabulate(rows, headers=headers)