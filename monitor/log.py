# -*- coding: utf-8 -*-

import os
import logging


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
