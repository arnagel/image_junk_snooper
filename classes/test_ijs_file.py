#!/usr/bin/env python
__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, image_junk_snooper project"
__license__ = ""
__version__ = "0.0.1"

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

    def test_check_create_open_file(self):
        path = "../output_data/test_file_report/"
        file_name = "file_data_version_"
        file_ext = ".csv"
        mode = ""
        msg = "Failed to create or open the file"
        self.assertIsInstance(self.ijs_file.check_create_open_file(path, file_name, file_ext), object, msg)

    def test_check_create_open_file_fail(self):
        path = "../output_nix/test_file_report/"
        file_name = "file_data_version_"
        file_ext = ".csv"
        mode = ""
        msg = "Failed to fail open the file"
        self.assertFalse(self.ijs_file.check_create_open_file(path, file_name, file_ext), msg)



if __name__ == '__main__':
    unittest.main()
