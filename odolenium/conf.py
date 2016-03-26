#! python3
# -*- coding: utf-8 -*-
import configparser
import os
import sys
import logging

from .error import *


__all__ = ["loadconfig","log"]

format = "%(asctime)s %(levelname)s %(name)s: %(message)s"

log = logging.getLogger("Odolenium")

defaults = {
    "url": "http://localhost:8069",
    "admin_password": "admin",
    "log_level": "INFO",
}

def loadconfig(config):
    global defaults

    if isinstance(config, dict):
        defaults.update(config)

    elif os.path.isfile(config):
        reader = configparser.ConfigParser()
        reader.read(config)

        if "odolenium" in reader.sections():
            defaults.update(reader["odolenium"])
        else:
            raise OdoleniumError("No [odolenium] section presents in '{}'".format(config))

    else:
        raise OdoleniumError("No such configration file '{}'".format(config))

    # setting up
    logging.basicConfig(format=format,level=logging._nameToLevel[defaults["log_level"]], stream=sys.stdout)

    return defaults