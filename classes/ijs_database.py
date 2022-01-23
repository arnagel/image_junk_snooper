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


class IJSDatabase:

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
                                         'APP_file_name',
                                         'META_file_size',
                                         'META_creation_date',
                                         'META_last_modified',
                                         'META_file_stats',
                                         'APP_image_type',
                                         'Base_Filename',
                                         'Base_Format',
                                         'Base_Data_Type',
                                         'Base_Bit_Depth_(per_Channel)',
                                         'Base_Bit_Depth_(per_Pixel)',
                                         'Base_Number_of_Channels',
                                         'Base_Mode',
                                         'Base_Palette',
                                         'Base_Width',
                                         'Base_Height',
                                         'Base_Megapixels',
                                         'EXIF_GPSInfoIFD',
                                         'EXIF_ResolutionUnit',
                                         'EXIF_ExifIFD',
                                         'EXIF_Make',
                                         'EXIF_Model',
                                         'EXIF_Software',
                                         'EXIF_Orientation',
                                         'EXIF_DateTime',
                                         'EXIF_YCbCrPositioning',
                                         'EXIF_ReferenceBlackWhite',
                                         'EXIF_YResolution',
                                         'EXIF_Copyright',
                                         'EXIF_XResolution',
                                         'EXIF_Artist',
                                         'iptc_title',
                                         'iptc_description',
                                         'iptc_headline',
                                         'iptc_city',
                                         'iptc_copyright',
                                         'iptc_country_primary',
                                         'iptc_country_detail',
                                         'iptc_creator',
                                         'iptc_creator_job_title',
                                         'iptc_credit_line',
                                         'iptc_date_created',
                                         'iptc_time_created',
                                         'iptc_caption_description_writer',
                                         'iptc_instructions',
                                         'iptc_intellectual_ genre',
                                         'iptc_job_identifier',
                                         'iptc_keywords',
                                         'iptc_province_state',
                                         'iptc_source',
                                         'iptc_subject_code',
                                         'iptc_sub_location',
                                         'error_String']

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

    def insert_csv_to_sql_convert(self, database_table, lst_dict_csv_record) -> str | bool:
        lst_insert_statements = []
        insert_str = "INSERT INTO " + database_table
        # add column names
        insert_col = ''
        for col in self.lst_col_name_file_report:
            insert_col += col + ', '
        insert_col = "(" + insert_col + ") "
        for dict_csv_record in lst_dict_csv_record:
            # add values
            insert_values = ''
            for key in dict_csv_record:
                insert_values += "'" + dict_csv_record[key] + "', "
            insert_values = "VALUES(" + insert_values + ");"

            insert_str += insert_col + insert_values

        return insert_str

    def save_statement_to_sql_file(self, path_file_name, statement) -> bool:
        # write the statement to the file
        try:
            with open(path_file_name, 'w') as file:
                file.write(statement)
            file.close()
            return True
        except IOError:
            logging.error(f"failed to save statement to sql|error: {IOError}")
            return False
