#!/usr/bin/env python
__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, image_junk_snooper project"
__license__ = ""
__version__ = "0.0.1"

import pprint
import unittest
import logging
from datetime import date


class TestIjsFile(unittest.TestCase):
    def setUp(self) -> None:
        log_data = "../log_data/log_files/"
        log_file_name = log_data + 'test_image_junk_snooper_' + str(date.today()) + '.log'
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                            , filename=log_file_name, level=logging.DEBUG)
        from ijs_file import IJSFile
        self.url = "D:/Projects/keh-photos-local/"
        self.ijs_file = IJSFile()

    def tearDown(self) -> None:
        pass

    def test_check_files(self):
        path = 'media/'
        msg = "Cannot check files"
        lst_files = ['D:/projects/keh-photos-local/media/10000232238593_01.jpg',
                     'D:/projects/keh-photos-local/media/10000232238593_02.jpg',
                     'D:/projects/keh-photos-local/media/10000232238593_03.jpg',
                     'D:/projects/keh-photos-local/media/10000232238593_04.jpg',
                     'D:/projects/keh-photos-local/media/10000232238593_05.jpg',
                     'D:/projects/keh-photos-local/media/10000232238593_06.jpg',
                     'D:/projects/keh-photos-local/media/10000232238593_07.jpg',
                     'D:/projects/keh-photos-local/media/10000232238593_08.jpg',
                     'D:/projects/keh-photos-local/media/10000239654683_01.jpg',
                     'D:/projects/keh-photos-local/media/10000239654683_02.jpg',
                     'D:/projects/keh-photos-local/media/10000239654683_03.jpg',
                     'D:/projects/keh-photos-local/media/10000239654683_04.jpg',
                     'D:/projects/keh-photos-local/media/10000239654683_05.jpg',
                     'D:/projects/keh-photos-local/media/10000239654683_06.jpg']
        for idx, f in enumerate(lst_files):
            logging.debug(f"File Name: {f}")
            self.assertIsInstance(self.ijs_file.check_files(f), dict, msg)

    def test_get_file_meta_data(self):
        url = "D:/Projects/keh-photos-local/"
        path = 'media/'
        file = '10000232238593_01.jpg'
        url_path_file = url + path + file
        msg = "Cannot get file meta data"
        self.assertIsInstance(self.ijs_file.get_file_meta_data(url_path_file), dict, msg)

    def test_create_file(self):
        path = "../output_data/test_file_report/"
        file_name = "file_data_version_0.csv"
        mode = ""
        msg = "Failed to create or open the file"
        self.assertIsInstance(self.ijs_file.create_file(path, file_name), object, msg)

    def test_check_file_name(self):
        path = "../output_data/test_file_report/"
        file_name = "file_data_version_"
        file_ext = ".csv"
        msg = "Failed to check for file"
        self.assertIsInstance(self.ijs_file.check_file_name(path, file_name, file_ext), str ,msg)

    def test_check_file_name(self):
        path = "../output_data/sql_files/"
        file_name = "test_sql_file"
        file_ext = "sql"
        msg = "Failed to check for file"
        self.assertIsInstance(self.ijs_file.check_file_name(path, file_name, file_ext), str, msg)

    def test_get_file_name(self):
        path_file_name = ['D:/projects/keh-photos-local/media/10000232238593_08.jpg',
                          'D:/projects/keh-photos-local/media/catalog\\\\product\\\\3\\\\3\\\\331358-6460_470x313.jpg']
        msg = f"Cannot get the file name from the path file name {path_file_name}"

        for idx, value in enumerate(path_file_name):
            self.assertIsInstance(self.ijs_file.get_file_name(value), str, msg)

    def test_reached_max_file_size_true(self):
        path_file_name = '../output_data/sql_files/test_sql_file.sql'
        max_file_size = 30000  # Smaller then current file size
        msg = "Cannot check file size"

        self.assertTrue(self.ijs_file.check_reached_max_file_size(path_file_name, max_file_size), msg)

    def test_reached_max_file_size_false(self):
        path_file_name = '../output_data/sql_files/test_sql_file.sql'
        max_file_size = 40000  # larger then curr file size
        msg = "Cannot check file size"

        self.assertFalse(self.ijs_file.check_reached_max_file_size(path_file_name, max_file_size), msg)


if __name__ == '__main__':
    unittest.main()
