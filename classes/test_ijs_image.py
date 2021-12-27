#!/usr/bin/env python
__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, image_junk_snooper project"
__license__ = ""
__version__ = "0.0.1"

import pprint
import unittest
import logging
from datetime import date
import tracemalloc


class TestIJSImage(unittest.TestCase):
    def setUp(self) -> None:
        log_data = "../log_data/log_files/"
        log_file_name = log_data + 'test_image_junk_snooper_' + str(date.today()) + '.log'
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                            , filename=log_file_name, level=logging.DEBUG)
        from ijs_image import IJSImage
        self.ijs_image = IJSImage()

    def tearDown(self) -> None:
        pass

    def test_check_image_content(self):
        tracemalloc.start()
        url = "D:/Projects/keh-photos-local/"
        path = 'media/'
        # file = '10000232238593_01.jpg'
        # url_path_file = url + path + file
        file = 'C:/Users/anagel.LAPTOP-8N7VRN57/OneDrive/Pictures/KEH/ITPC Image Standard/IPTC-PhotometadataRef-Std2021.1.jpg'
        url_path_file = file
        msg = "Cannot get file content information"
        self.assertIsInstance(self.ijs_image.check_image_content(url_path_file), dict, msg)
        # snapshot = tracemalloc.take_snapshot()
        # for stat in snapshot.statistics("lineno"):
        #    pprint.pprint(stat)

    def test_check_image_content_fail(self):
        url = "D:/Projects/keh-photos-local/"
        path = 'media/'
        msg = "Cannot check files"
        file = '10000232238593_01_01.jpg'
        url_path_file = url + path + file
        msg = "Should return false, and it returns something else"
        self.assertFalse(self.ijs_image.check_image_content(url_path_file), msg)

    def test_test_base_64_convert(self):
        tracemalloc.start()
        url = "D:/Projects/keh-photos-local/"
        path = 'media/'
        file = '10000232238593_01.jpg'
        msg = "Cannot convert image to base64"
        url_path_file = url + path + file
        msg = "Cannot get file content information"
        self.assertTrue(self.ijs_image.test_base64_convert(url_path_file), msg)

    def test_getITPC_meta_data(self):
        lst_files = ['C:/Users/anagel.LAPTOP-8N7VRN57/OneDrive/Pictures/KEH/ITPC Image Standard/IPTC-PhotometadataRef-Std2021.1.jpg',
                     "D:/Projects/keh-photos-local/media/10000232238593_01.jpg"]
        msg = "Cannot get the ITPC meta data"
        for idx, val in enumerate(lst_files):
            self.assertIsInstance(self.ijs_image.get_ITPC_meta_data(val), dict, msg)

    def test_getITPC_data(self):
        lst_files = ['C:/Users/anagel.LAPTOP-8N7VRN57/OneDrive/Pictures/KEH/ITPC Image Standard/IPTC-PhotometadataRef-Std2021.1.jpg'
            , "D:/Projects/keh-photos-local/media/10000232238593_01.jpg"]
        msg = "Cannot get the ITPC meta data"
        for idx, val in enumerate(lst_files):
            self.assertIsInstance(self.ijs_image.get_ITPC_data(val), dict, msg)


if __name__ == '__main__':
    unittest.main()
