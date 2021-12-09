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
import pprint


class IJSFolder:

    def get_folder_content(self, start_folder) -> dict:
        dict_out = {'folders': [start_folder], 'files': []}
        for root, dirs, files in os.walk(start_folder):
            for name in files:
                dict_out['files'].append(os.path.join(root, name))
            for name in dirs:
                dict_out['folders'].append(os.path.join(root, name))
        return dict_out

    def get_folder_content_old(self, path) -> dict:
        if os.path.isdir(path):
            dic_out = {}
            lst_files = []
            lst_folders = []
            for item in os.scandir(path):
                if item.is_file():
                    lst_files.append(item.name)
                elif item.is_dir():
                    lst_folders.append(item.name)
                else:
                    logging.error(f"Unknown item in folder: {path} - {item.name}")

            # logging.info(f"path:{path}, type:folder:{len(lst_folders)} - type:file:{len(lst_files)}")
            return {'files': lst_files, 'folders': lst_folders}
        else:
            logging.error(f"This folder does not exist or cannot be accessed: {path}")
            return {'error': f"This folder does not exist or cannot be accessed: {path}"}


