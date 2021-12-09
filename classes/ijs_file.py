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
import classes
from classes.ijs_image import IJSImage
import logging
import pprint
import sys
from typing import Union
from datetime import datetime
import os


class IJSFile(IJSImage):

    def check_files(self, file_name):
        dict_out = {'APP:file_name': file_name}
        if not os.path.isfile(file_name):
            logging.warning(f"Not a file or not the correct location: {file_name}")
        dict_out.update(self.get_file_meta_data(file_name))
        if 'file_size' in dict_out:
            if dict_out['file_size'] <= 1:
                dict_out['no_content'] = True
        """Check the file image content"""
        dict_out.update(self.check_image_content(file_name))

        # logging.debug(f"Check File Meta: {dict_out}")
        return dict_out

    def get_file_meta_data(self, file) -> dict:
        """Get file meta data"""
        dic_meta = {
            'META:file_size': os.path.getsize(file),
            'META:creation_date': os.path.getctime(file),
            'META:last_modified': os.path.getmtime(file),
            'META:file_stats': os.stat(file)
        }
        # logging.debug(f"File Meta Data: {dic_meta}")
        return dic_meta

    def check_create_open_file(self, path, file_name, file_ext, mode='a+') -> object | bool:
        cnt = 0
        file_search = path + file_name + str(cnt) + file_ext
        while os.path.exists(file_search):
            cnt += 1
            file_search = path + file_name + str(cnt) + file_ext

        try:
            f_obj = open(file_search, mode)
            logging.info(f"Created file: {file_search}")
            return f_obj
        except IOError as io_error:
            logging.debug(f"Error: {io_error}")
            return False
