#!/usr/bin/env python
from __future__ import annotations

__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, Image Junk Snooper"
__credits__ = []
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "anagel@keh.com"
__status__ = "Development"
__package__ = "image_junk_snooper"
__github__ = 'https://github.com/arnagel/image_junk_snooper.git'

# imports
import configparser
import getopt
import logging
import pprint
import sys
from typing import Union
from datetime import datetime, date
# Classes
from classes.ijs_folder import IJSFolder

config_path_file = './config/config.ini'
in_data = ''
tmp_data = ''
log_data = ""
input_file = ''
tmp_file = ''
csv_ext = ''
log_file_name = log_data + 'image_junk_snooper_' + str(date.today()) + '.log'
vm_url = ''
vm_bucket = ''
vm_parent_folders = []


def main(args):
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                        , filename=log_file_name, level=logging.DEBUG)
    get_args(args)


def get_config():
    config = configparser.ConfigParser()
    config_sections = config.sections()
    config.read(config_path_file)
    pprint.pprint(f"Config Section: {config_sections}")


def get_args(argv):
    global input_file
    global trip_name

    try:
        opts, args = getopt.getopt(argv, "ht:i:", ["trip=", "ifile="])
    except getopt.GetoptError:
        print('main.py -t <trip_name> -i <input_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -t <trip_name>  -i <input_file>')
            sys.exit()
        elif opt in ("-t", "--trip"):
            trip_name = arg
        elif opt in ("-i", "--ifile"):
            input_file = arg


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
