# -*- coding: utf-8 -*-

from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path


def dt_now_str():
    """ Return current date and time as string """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_config():
    """ Read and parse the config file """
    config_path = (Path(".") / "config.file").as_posix()
    load_dotenv(dotenv_path=config_path)
