# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def observations(observations):
    """ Plot observations """
    y_users = np.array([obs["users"] for obs in observations])
    y_load = np.array([obs["load_average"] for obs in observations])
    y_cons = np.array([obs["network_connections"] for obs in observations])

    x_labels = [datetime.strptime(obs["created_at"], "%Y-%m-%d %H:%M:%S") for obs in observations]

    plt.figure(1, figsize=(8, 8))
    plt.suptitle(
        "From %s to %s" % (x_labels[0].strftime("%Y-%m-%d %H:%M:%S"), x_labels[-1].strftime("%Y-%m-%d %H:%M:%S"))
    )

    plt.subplot(311)
    plt.plot(x_labels, y_users, "b-")
    plt.ylabel("users")

    plt.subplot(312)
    plt.plot(x_labels, y_load, "c--")
    plt.ylabel("load average")

    plt.subplot(313)
    plt.plot(x_labels, y_cons, "m-.")
    plt.ylabel("nw connections")

    plt.gcf().autofmt_xdate()

    plt.show()
