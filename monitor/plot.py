# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime

def observations(observations):
    """ Plot observations """
    y_users = np.array([obs["users"] for obs in observations], dtype=int)
    y_load = np.array([obs["load_average_1"] for obs in observations])
    y_cons = np.array([obs["network_connections"] for obs in observations], dtype=int)
    y_pscnt = np.array([obs["processes"] for obs in observations], dtype=int)
    y_free = np.array([obs["free_memory"] for obs in observations], dtype=int)

    x_labels = [datetime.strptime(obs["created_at"], "%Y-%m-%d %H:%M:%S") for obs in observations]

    plt.figure(1, figsize=(8, 8))
    plt.suptitle(
        "From %s to %s" % (x_labels[0].strftime("%Y-%m-%d %H:%M:%S"), x_labels[-1].strftime("%Y-%m-%d %H:%M:%S"))
    )

    axes = plt.subplot(321)
    axes.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.plot(x_labels, y_users, "b-")
    plt.ylabel("users")

    plt.subplot(322)
    plt.plot(x_labels, y_load, "c-")
    plt.ylabel("load average")

    axes = plt.subplot(323)
    axes.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.plot(x_labels, y_cons, "m-")
    plt.ylabel("nw connections")

    axes = plt.subplot(324)
    axes.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.plot(x_labels, y_pscnt, "g-")
    plt.ylabel("ps count")

    axes = plt.subplot(325)
    axes.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.plot(x_labels, y_free, "y-")
    plt.ylabel("free memory")

    plt.gcf().autofmt_xdate()

    plt.show()
