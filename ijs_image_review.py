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
import sys
from datetime import date

# Classes
from classes.ijs_folder import IJSFolder
from classes.ijs_file import IJSFile
from classes.ijs_helper import IJSHelper
from classes.ijs_report import IJSReport

config_path_file = './config/config.ini'
user_output_file_name = ''
user_db_name = ''
db_engine = 'bq'
db_table_prefix = ''
output_file_name = ''
output_folder = ''
output_ext = ''
avail_file_name = ''
input_file = ''
csv_ext = ''
log_file_name = ''
vm_url = ''
vm_bucket = ''
vm_parent_folders = []
obj_file = None


def main(args):
    global obj_file
    global avail_file_name
    get_args(args)
    get_config()
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                        , filename=log_file_name, level=logging.DEBUG)
    ijs_folder = IJSFolder()
    ijs_file = IJSFile()

    stdout_bear()

    avail_file_name = ijs_file.check_file_name(output_folder, output_file_name, output_ext)
    obj_file = ijs_file.create_file(output_folder, avail_file_name)
    if isinstance(obj_file, bool):
        logging.error(
            f"Cannot create the output file: {output_folder + avail_file_name}. Cannot continue, need to exit")
        sys.exit("Fail")
    """Close the file for now, no need to keep it open for the first part"""
    obj_file.close()

    repo_path = vm_url + vm_bucket
    for parent_folder in vm_parent_folders:
        parent_folder += '/'
        parent_folder = parent_folder.strip()
        dict_folder_content = ijs_folder.get_folder_content(repo_path + parent_folder)
        loop_over_files(dict_folder_content['files'])


def stdout_bear() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s',
                                  '%m-%d-%Y %H:%M:%S')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('/var/log/bbbc_image_snooper.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('/var/log/bbbc_image_snooper.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def loop_over_files(dict_files) -> None:
    ijs_file = IJSFile()
    ijs_helper = IJSHelper()
    ijs_report = IJSReport()
    dict_file_data = {}
    for path_file_name in dict_files:
        """Get the file name components"""
        file_name = ijs_file.get_file_name(path_file_name)
        dict_file_data.update(ijs_helper.evaluate_model_item(file_name))
        logging.info(f"After model eval: {dict_file_data}")
        dict_file_data.update(ijs_file.check_files(path_file_name))
        logging.info(f"After file check: {dict_file_data}")
        ijs_report.create_file_report(output_folder, avail_file_name, dict_file_data)


def get_config() -> None:
    global log_file_name
    global vm_url
    global vm_bucket
    global vm_parent_folders
    global output_file_name
    global output_folder
    global output_ext
    global db_table_prefix
    config = configparser.ConfigParser()
    config.read(config_path_file)
    log_data = config['Log_Setup']['log_data']
    log_name = config['Log_Setup']['log_file_name']
    log_ext = config['Log_Setup']['log_file_ext']
    log_file_name = log_data + log_name + str(date.today()) + log_ext
    logging.debug(f"Log File Name: {log_file_name}")
    vm_url = config['VM_Access_Setup']['vm_url']
    vm_bucket = config['VM_Access_Setup']['vm_bucket']
    vm_parent_folders = config['VM_Access_Setup']['vm_parent_folders']
    vm_parent_folders = vm_parent_folders.split(',')
    logging.debug(f"VM url: {vm_url} / Bucket: {vm_bucket} / Folders: {vm_parent_folders}")
    output_folder = config['Output_File_Setup']['output_folder']
    output_ext = config['Output_File_Setup']['output_ext']
    output_file_name = user_output_file_name + '_' + str(date.today()) + '_'
    logging.debug(f"Output File Name: {output_file_name}")
    db_table_prefix = config['Sql_Database_Names']['bq_it_department']


def get_args(argv) -> None:
    global user_output_file_name
    global user_db_name
    global db_engine

    try:
        opts, args = getopt.getopt(argv, "ht:o:db", ["ofile=", "dbname="])
    except getopt.GetoptError:
        print('ijs_image_review.py -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('ijs_image_review.py -o <output_file> -db <database_name>')
            sys.exit()
        elif opt in ("-o", "--ofile"):
            user_output_file_name = arg
        elif opt in ("-db", "--dbname"):
            user_db_name = arg
        elif opt in ("-dbe", "--dbengine"):
            db_engine = arg


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
