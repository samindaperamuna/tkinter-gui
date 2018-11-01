import json
import logging
from shutil import copyfile

RESOURCE_FILE = "resources/parameters.json"
DEFAULT_FILE = "resources/default.json"


def read_settings():
    """Read the JSON settings file and entries."""
    try:
        with open(RESOURCE_FILE) as file:
            return json.load(file)
    except Exception as e:
        logging.critical("Couldn't parse the JSON file: {0}".format(str(e)))
        return ""


def write_settings(data_dict):
    try:
        with open(RESOURCE_FILE, 'w') as fp:
            json.dump(data_dict, fp)
        return True
    except Exception as e:
        logging.critical("Couldn't save the JSON file: {0}".format(str(e)))
        return False


def reset_default():
    copyfile(DEFAULT_FILE, RESOURCE_FILE)
