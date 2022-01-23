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
from classes.ijs_helper import IJSHelper


class IJSDatabase(IJSHelper):

    def __init__(self):
        super().__init__()

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
