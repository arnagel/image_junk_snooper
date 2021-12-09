#!/usr/bin/env python
__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, image_junk_snooper project"
__license__ = ""
__version__ = "0.0.1"

import unittest
import logging
from datetime import date


class TestIJSReport(unittest.TestCase):
    def setUp(self) -> None:
        log_data = "../log_data/log_files/"
        log_file_name = log_data + 'test_image_junk_snooper_' + str(date.today()) + '.log'
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                            , filename=log_file_name, level=logging.DEBUG)
        from ijs_report import IJSReport
        self.ijs_report = IJSReport()

        self.url_path = '../output_data/test_file_report/'

    def tearDown(self) -> None:
        pass

    def test_create_file_report(self):
        path = self.url_path
        file_name = "file_data_version_"
        file_ext = ".csv"
        content = {'APP:file_name': 'D:/projects/keh-photos-local/uploads/2021-11-22\\\\387385-3464354_08.jpg',
                   'META:file_size': 11155, 'META:creation_date': 1637624065.9839623,
                   'META:last_modified': 1637624066.111192,
                   'META:file_stats': 'os.stat_result(st_mode=33206, st_ino=281474976911702, st_dev=1859694110, st_nlink=1, st_uid=0,st_gid=0, st_size=11155, st_atime=1638893490,st_mtime=1637624066, st_ctime=1637624065)',
                   'APP:image_type': 'JPEG',
                   'Base:Filename': 'D:/projects/keh-photos-local/uploads/2021-11-22\\\\387385-3464354_08.jpg',
                   'Base:Format': 'JPEG', 'Base:Data_Type': 'dtype(\'uint8\')', 'Base:Bit_Depth_(per_Channel)': '8',
                   'Base:Bit_Depth_(per_Pixel)': 24, 'Base:Number_of_Channels': 3, 'Base:Mode': 'RGB',
                   'Base:Palette': None, 'Base:Width': 400, 'Base:Height': 400, 'Base:Megapixels': 0.16,
                   'EXIF:GPSInfoIFD': 11942, 'EXIF:ResolutionUnit': 2, 'EXIF:ExifIFD': 216, 'EXIF:Make': 'Canon',
                   'EXIF:Model': 'Canon EOS 6D', 'EXIF:Software': 'Ortery Photography Solutions', 'EXIF:Orientation': 1,
                   'EXIF:DateTime': '2021:11:19 16:03:46', 'EXIF:YCbCrPositioning': 2,
                   'EXIF:ReferenceBlackWhite': (0.0, 255.0, 128.0, 255.0, 128.0, 255.0), 'EXIF:YResolution': 0.0,
                   'EXIF:Copyright': '', 'EXIF:XResolution': 0.0, 'EXIF:Artist': '',
                   'error': 'Exception err: D:/projects/keh-photos-local/uploads/2021-11-22\\\\371656-3469730_08.jpg - Error MSG: Could not find a backend to open `D:/projects/keh-photos-local/uploads/2021-11-22\\\\371656-3469730_08.jpg with iomode ri.',
                   'funny': 'me'}

        self.assertTrue(self.ijs_report.create_file_report(path, file_name, file_ext, content))


if __name__ == '__main__':
    unittest.main()
