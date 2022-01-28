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
from classes.ijs_image import IJSImage
from classes.ijs_helper import IJSHelper
import logging
import os
import re


class IJSFile(IJSImage, IJSHelper):

    def check_files(self, file_name):
        dict_out = {'APP:file_name': file_name, 'no_content': 0}
        if not os.path.isfile(file_name):
            logging.warning(f"Not a file or not the correct location: {file_name}")
        dict_out.update(self.get_file_meta_data(file_name))
        if 'META:file_size' in dict_out:
            if dict_out['META:file_size'] <= 1:
                dict_out['no_content'] = 1
        """Check the file image content"""
        dic_return = self.check_image_content(file_name)
        if dic_return:
            dict_out.update(dic_return)
        logging.debug(f"Check File Meta: {dict_out}")
        return dict_out

    def get_file_meta_data(self, file) -> dict:
        """Get file meta data"""
        dic_meta = {
            'META:file_size': os.path.getsize(file),
            'META:creation_date': os.path.getctime(file),
            'META:last_modified': os.path.getmtime(file),
            'META:file_stats': f"{os.stat(file)}"
        }
        logging.debug(f"File Meta Data: {dic_meta}")
        return dic_meta

    def create_file(self, path, file_name, mode='a+') -> object | bool:
        path_file_name = path + file_name
        try:
            f_obj = open(path_file_name, mode, newline='', encoding='utf-8')
            logging.info(f"Created/Open file: {path_file_name}")
            return f_obj
        except IOError as io_error:
            logging.debug(f"Error: {io_error}")
            return False

    def check_file_name(self, path, file_name, file_ext) -> str:
        cnt = 0
        file_search = path + file_name + "_" + str(cnt) + "." + file_ext
        while os.path.exists(file_search):
            cnt += 1
            file_search = path + file_name + "_" + str(cnt) + "." + file_ext
        logging.debug(f"Available File Name: {file_search}")
        return file_name + "_" + str(cnt) + "." + file_ext

    def get_file_name(self, path_file_name) -> str:
        lst_file_name = re.split('[/|\\\\]', path_file_name)
        logging.debug(f"File name: {lst_file_name[-1]}")
        return lst_file_name[-1]

    def check_reached_max_file_size(self, path_file_name, max_file_size) -> bool:
        curr_file_size = os.path.getsize(path_file_name)
        if curr_file_size >= max_file_size:
            return True
        return False
