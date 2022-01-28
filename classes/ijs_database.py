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


class IJSDatabase(IJSFile):

    def __init__(self):
        super().__init__()

    def insert_csv_to_sql_convert(self, database_table, lst_dict_csv_record) -> list | bool:
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
            lst_insert_statements.append(insert_str)

        return lst_insert_statements

    def save_statement_to_sql_file(self, path, file_name, lst_statement) -> bool:
        # check the current file
        # if current file is larger then max, create new file name
        # check if new file name already exist
        # if yes, create new file name, do while file name exist
        max_file_size = 30000
        file_ext = '.jpg'
        if self.check_reached_max_file_size(path_file_name, max_file_size):
            # we need a new file name
            new_filename = self.check_file_name(path, file_name, file_ext)

        # write the statement to the file
        line_break = '\n'
        max_file_size = 30000
        with open(path_file_name, 'a+') as file:
            file.seek(0)
            for statement in lst_statement:
                # if file name reaches max file size, save the remaining list
                # close the current file
                # create a new filename
                # write the remaining list to file






                try:
                    file.write(statement + line_break)
                    file.seek(0, os.SEEK_END)
                    curr_file_size = file.tell()
                    if curr_file_size >= max_file_size:
                        print(f"Reach the maximum: {curr_file_size}")
                except IOError:
                    logging.error(f"failed to save statement to sql|error: {IOError}")
