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
import os
from classes.ijs_file import IJSFile
from classes.ijs_helper import IJSHelper


class IJSReport(IJSFile, IJSHelper):

    def __init__(self):
        self.lst_col_name_file_report = ['model_id',
                                         'item_id',
                                         'barcode',
                                         'sequence',
                                         'no_content',
                                         'base64_error',
                                         'height',
                                         'width',
                                         'OEM',
                                         'copy',
                                         'copy_pos_4',
                                         'copy_pos_5',
                                         'APP:file_name',
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
                                         'iptc:title',
                                         'iptc:description',
                                         'iptc:headline',
                                         'iptc:city',
                                         'iptc:copyright',
                                         'iptc:country_primary',
                                         'iptc:country_detail',
                                         'iptc:creator',
                                         'iptc:creator_job_title',
                                         'iptc:credit_line',
                                         'iptc:date_created',
                                         'iptc:time_created',
                                         'iptc:caption_description_writer',
                                         'iptc:instructions',
                                         'iptc:intellectual_ genre',
                                         'iptc:job_identifier',
                                         'iptc:keywords',
                                         'iptc:province_state',
                                         'iptc:source',
                                         'iptc:subject_code',
                                         'iptc:sub_location',
                                         'error']

    def create_file_report(self, path, file_name, content) -> bool:
        """Open the file and get the file object"""
        f_obj = self.create_file(path, file_name)
        if not isinstance(f_obj, object):
            logging.error("Cannot open file")
            return False

        """Create the csv object"""
        csv_dict_writer = csv.DictWriter(f_obj, self.lst_col_name_file_report)
        """Write header if the file is empty"""
        if os.fstat(f_obj.fileno()).st_size < 10:
            csv_dict_writer.writeheader()

        """Loop over the content and place it into the correct position of the csv string"""
        lst_content = {'error': ''}
        for key in self.lst_col_name_file_report:
            if key in content:
                if key == 'META:creation_date' or key == 'META:last_modified':
                    lst_content[key] = self.convert_Unix_to_Human(content[key], 5, '%m/%d/%Y %H:%M:%S')
                elif key == 'error':
                    lst_content[key] += f"{content[key]} | "
                else:
                    lst_content[key] = content[key]
            else:
                lst_content[key] = ''
                logging.info(f"Cannot find: {key} in content")

        """Write the content to the file"""
        csv_dict_writer.writerow(lst_content)

        """Close the file object"""
        f_obj.close()

        return True

    def read_file_report(self, path_file_name) -> list | bool:
        lst_content = []
        try:
            with open(path_file_name, newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                try: 
                    for row in reader:
                        lst_content.append(row)
                except csv.Error as err:
                    logging.error(f'file {path_file_name}, line {reader.line_num}: {err}')
            csv_file.close()
            return lst_content
        except IOError as err:
            logging.error(f'Failed to open file to read csv data: {path_file_name}: {err}')
            return False




