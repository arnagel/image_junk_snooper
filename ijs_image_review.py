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

config_path_file = './config/config.ini'
user_output_file_name = ''
output_file_name = ''
input_file = ''
csv_ext = ''
log_file_name = ''
vm_url = ''
vm_bucket = ''
vm_parent_folders = []


def main(args):
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                        , filename=log_file_name, level=logging.DEBUG)
    get_args(args)


def get_config() -> None:
    global log_file_name
    global vm_url
    global vm_bucket
    global vm_parent_folders
    global output_file_name
    config = configparser.ConfigParser()
    config.read(config_path_file)
    # pprint.pprint(f"Config Section: {config_sections}")
    log_data = config['Log_Setup']['log_data']
    log_name = config['Log_Setup']['log_file_name']
    log_ext = config['Log_Setup']['log_file_ext']
    log_file_name = log_data + log_name + str(date.today()) + log_ext
    # pprint.pprint(f"Log File Name: {log_file_name}")
    vm_url = config['VM_Access_Setup']['vm_url']
    vm_bucket = config['VM_Access_Setup']['vm_bucket']
    vm_parent_folders = config['VM_Access_Setup']['vm_parent_folders']
    logging.info(f"These are the parent folder we need to process: {vm_parent_folders}")
    # pprint.pprint(f"VM url: {vm_url} / Bucket: {vm_bucket} / Folders: {vm_parent_folders}")
    output_folder = config['Output_File_Setup']['output_folder']
    output_ext = config['Output_File_Setup']['output_ext']
    output_file_name = output_folder + user_output_file_name + str(date.today()) + output_ext
    # pprint.pprint(f"Output File Name: {output_file_name}")


def get_args(argv):
    global user_output_file_name

    try:
        opts, args = getopt.getopt(argv, "ht:o:", ["ofile="])
    except getopt.GetoptError:
        print('main.py -i <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -o <output_file>')
            sys.exit()
        elif opt in ("-o", "--ofile"):
            user_output_file_name = arg


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
