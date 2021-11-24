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
        self.ijs_file = IJSFile()

    def tearDown(self) -> None:
        pass

    def test_check_files(self):
        url = "D:/Projects/keh-photos-local/"
        path = 'media/'
        msg = "Cannot check files"
        lst_files = ['10000232238593_01.jpg', '10000232238593_02.jpg', '10000232238593_03.jpg', '10000232238593_04.jpg', '10000232238593_05.jpg', '10000232238593_06.jpg', '10000232238593_07.jpg', '10000232238593_08.jpg', '10000239654683_01.jpg', '10000239654683_02.jpg', '10000239654683_03.jpg', '10000239654683_04.jpg', '10000239654683_05.jpg', '10000239654683_06.jpg', '10000239654683_07.jpg', '10000239654683_08.jpg', '10000240308196_01.jpg', '10000240308196_02.jpg', '10000240308196_03.jpg', '10000240308196_04.jpg', '10000240308196_05.jpg', '10000240308196_06.jpg', '10000243809868_02.jpg', '10000243809868_03.jpg', '10000243809868_04.jpg', '10000243809868_05.jpg', '10000243809868_06.jpg', '10000243809868_07.jpg', '10000243809868_08.jpg']
        self.assertIsInstance(self.ijs_file.check_files(url, path, lst_files), dict, msg)

    def test_get_file_meta_data(self):
        url = "D:/Projects/keh-photos-local/"
        path = 'media/'
        file = '10000232238593_01.jpg'
        url_path_file = url + path + file
        msg = "Cannot get file meta data"
        self.assertIsInstance(self.ijs_file.get_file_meta_data(url_path_file), dict, msg)


if __name__ == '__main__':
    unittest.main()
