#!/usr/bin/env python
__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, image_junk_snooper project"
__license__ = ""
__version__ = "0.0.1"

import unittest
import logging
from datetime import date

import ijs_image_review


class TestIjsImageReview(unittest.TestCase):
    def setUp(self) -> None:
        log_data = "./log_data/log_files/"
        log_file_name = log_data + 'test_image_junk_snooper_' + str(date.today()) + '.log'
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                            , filename=log_file_name, level=logging.DEBUG)
        import ijs_image_review
        self.config_path_file = './config/config.ini'

    def tearDown(self) -> None:
        pass

    def test_get_config(self):
        msg = "Did not get config information"
        self.assertIsNone(ijs_image_review.get_config(), msg)


if __name__ == '__main__':
    unittest.main()
