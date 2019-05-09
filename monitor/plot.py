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

    x_labels = [datetime.strptime(obs["created_at"], "%Y-%m-%d %H:%M:%S") for obs in observations]

    plt.figure(1, figsize=(8, 8))
    plt.suptitle(
        "From %s to %s" % (x_labels[0].strftime("%Y-%m-%d %H:%M:%S"), x_labels[-1].strftime("%Y-%m-%d %H:%M:%S"))
    )

    axes = plt.subplot(311)
    axes.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.plot(x_labels, y_users, "b-")
    plt.ylabel("users")

    plt.subplot(312)
    plt.plot(x_labels, y_load, "c--")
    plt.ylabel("load average")

    axes = plt.subplot(313)
    axes.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.plot(x_labels, y_cons, "m-.")
    plt.ylabel("nw connections")

    plt.gcf().autofmt_xdate()

    plt.show()
