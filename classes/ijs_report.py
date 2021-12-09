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
import csv
import pprint
import sys
from typing import Union
from datetime import datetime
from classes.ijs_file import IJSFile


class IJSReport(IJSFile):

    def __init__(self):
        self.lst_col_name_file_report = ['APP:file_name',
                                         'META:file_size',
                                         'META:creation_date',
                                         'META:last_modified',
                                         'META:file_stats',
                                         'APP:image_type',
                                         'Base:Filename',
                                         'Base:Format',
                                         'Base:Data_Type',
                                         'Base:Bit_Depth_(per_Channel)',
                                         'Base:Bit_Depth_(per_Pixel)',
                                         'Base:Number_of_Channels',
                                         'Base:Mode',
                                         'Base:Palette',
                                         'Base:Width',
                                         'Base:Height',
                                         'Base:Megapixels',
                                         'EXIF:GPSInfoIFD',
                                         'EXIF:ResolutionUnit',
                                         'EXIF:ExifIFD',
                                         'EXIF:Make',
                                         'EXIF:Model',
                                         'EXIF:Software',
                                         'EXIF:Orientation',
                                         'EXIF:DateTime',
                                         'EXIF:YCbCrPositioning',
                                         'EXIF:ReferenceBlackWhite',
                                         'EXIF:YResolution',
                                         'EXIF:Copyright',
                                         'EXIF:XResolution',
                                         'EXIF:Artist',
                                         'error',
                                         'not_registered']

    def create_file_report(self, path, file_name, file_ext, content):
        """Open the file and get the file object"""
        f_obj = self.check_create_open_file(path, file_name, file_ext)
        if f_obj is False:
            logging.error("Cannot create file report, file issues")
            return False

        """Create the csv object"""
        csv_dict_writer = csv.DictWriter(f_obj, self.lst_col_name_file_report)
        """Add the headers to the file"""
        csv_dict_writer.writeheader()

        """Loop over the content and place it into the correct position of the csv string"""
        lst_content = {}
        for key in self.lst_col_name_file_report:
            if key in content:
                lst_content[key] = content[key]
            else:
                lst_content[key] = ''
                logging.error(f"Cannot find: {key} content")

        """Write the content to the file"""
        csv_dict_writer.writerow(lst_content)

        """Close the file object"""
        f_obj.close()

        return False

# TODO: Get the model and item id, and added to the content object
# TODO: Convert the timestamp from UNIX to human readable.
# TODO: Remove the empty line in the csv file
# TODO: We need to open the same file to add the content.





