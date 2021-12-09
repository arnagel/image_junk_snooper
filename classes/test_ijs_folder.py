#!/usr/bin/env python
__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, image_junk_snooper project"
__license__ = ""
__version__ = "0.0.1"

import unittest
import logging
from datetime import date


class TestIjsFolder(unittest.TestCase):
    def setUp(self) -> None:
        log_data = "../log_data/log_files/"
        log_file_name = log_data + 'test_image_junk_snooper_' + str(date.today()) + '.log'
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                            , filename=log_file_name, level=logging.DEBUG)
        from ijs_folder import IJSFolder
        self.ijs_folder = IJSFolder()

    def tearDown(self) -> None:
        pass

    def test_get_folder_content(self):
        # start_folder = 'D:\\Projects\\keh-photos-local\\media\\'
        start_folder = 'D:\\Projects\\keh-photos-local\\uploads\\'
        msg = "Did not get a dictionary returned"
        self.assertIsInstance(self.ijs_folder.get_folder_content(start_folder), dict, msg)

    def test_get_folder_content_old(self):
        path = 'D:\\Projects\\keh-photos-local\\media\\'
        msg = "Did not get a dictionary returned"
        self.assertIsInstance(self.ijs_folder.get_folder_content(path), dict, msg)

    def test_get_folder_content_fail(self):
        path = 'D:\\Projects\\keh-photos-local\\bear\\'
        msg = "The folder should not exist"
        self.assertFalse(self.ijs_folder.get_folder_content(path), msg)


if __name__ == '__main__':
    unittest.main()
