#!/usr/bin/env python
__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, image_junk_snooper project"
__license__ = ""
__version__ = "0.0.1"

import pprint
import unittest
import logging
from datetime import date


class TestBarcode(unittest.TestCase):
    def setUp(self) -> None:
        log_data = "../log_data/log_files/"
        log_file_name = log_data + 'test_image_junk_snooper_' + str(date.today()) + '.log'
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                            , filename=log_file_name, level=logging.DEBUG)
        from barcode import Barcode
        self.barcode = Barcode()

    def test_read_barcode(self):
        barcode_val = '10000232238593'
        dict_return = {'check': 93, 'id': 2322385, 'type': 10}
        self.assertDictEqual(self.barcode.read_barcode(barcode_val), dict_return)

    def test_check_digit(self):
        code_val = '100002322385'
        self.assertEqual(self.barcode.check_digit(code_val), 93)


if __name__ == '__main__':
    unittest.main()
