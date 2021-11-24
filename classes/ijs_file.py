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
import pprint
import sys
from typing import Union
from datetime import datetime
import os


class IJSFile:

    def __init__(self):
        pass

    def check_files(self, url, path, lst_files):
        for idx, file_name in enumerate(lst_files):
            url_path_file = url + path + file_name
            dict_file_meta = {'url': url, 'path': path, 'file_name': file_name}
            if not os.path.isfile(url_path_file):
                logging.warning(f"Not a file or not the correct location: {url_path_file}")
            dict_file_meta.update(self.get_file_meta_data(url_path_file))
            if 'file_size' in dict_file_meta:
                if dict_file_meta['file_size'] <= 1:
                    dict_file_meta['no_content'] = True

            """Check the file image content"""



        pprint.pprint(f"File Meta: {dict_file_meta}")
        return dict_file_meta

    def get_file_meta_data(self, file) -> dict:
        """Get file meta data"""
        dic_meta = {
            'file_size': os.path.getsize(file),
            'creation_date': os.path.getctime(file),
            'last_modified': os.path.getmtime(file),
            'file_stats': os.stat(file)
        }
        return dic_meta
