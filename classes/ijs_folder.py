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
import logging
import os


class IJSFolder:

    def __init__(self):
        pass

    def get_folder_content(self, url, path) -> dict | bool:
        folder_location = url + path
        if os.path.isdir(folder_location):
            dic_out = {}
            lst_files = []
            lst_folders = []
            for item in os.scandir(folder_location):
                if item.is_file():
                    lst_files.append(item.name)
                elif item.is_dir():
                    lst_folders.append(item.name)
                else:
                    logging.info(f"Unknown item in folder: {folder_location} - {item.name}")

            logging.info(f"[type:file, path:{path}, cnt:{len(lst_files)}]")
            logging.info(f"[type:folder, path:{path}, cnt:{len(lst_folders)}]")
            dic_out['files'] = lst_files
            dic_out['folders'] = lst_folders
            return dic_out
        else:
            logging.error(f"This folder does not exist or cannot be accessed: {folder_location}")
            return False


