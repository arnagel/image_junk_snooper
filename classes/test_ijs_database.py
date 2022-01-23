#!/usr/bin/env python
__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, image_junk_snooper project"
__license__ = ""
__version__ = "0.0.1"

import unittest
import logging
from datetime import date


class TestIJSDatabase(unittest.TestCase):
    def setUp(self) -> None:
        log_data = "../log_data/log_files/"
        log_file_name = log_data + 'test_image_junk_snooper_' + str(date.today()) + '.log'
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                            , filename=log_file_name, level=logging.DEBUG)
        from ijs_database import IJSDatabase
        self.ijs_database = IJSDatabase()

        self.url_path = '../output_data/test_file_report/'

    def tearDown(self) -> None:
        pass

    def test_create_file_report(self):
        path = self.url_path
        file_name = "file_data_version_0.csv"
        content = [{'model_id': '387385',
                    'item_id': '3464354',
                    'barcode': '',
                    'sequence': '08',
                    'APP:file_name': 'D:/projects/keh-photos-local/uploads/2021-11-22\\\\387385-3464354_08.jpg',
                    'no_content': 0,
                    'META:file_size': 11155,
                    'META:creation_date': 1637624065.9839623,
                    'META:last_modified': 1637624066.111192,
                    'META:file_stats': 'os.stat_result(st_mode=33206, st_ino=281474976911702,st_dev=1859694110, '
                                       'st_nlink=1, st_uid=0, st_gid=0, st_size=11155, st_atime=1639167154, '
                                       'st_mtime=1637624066, st_ctime=1637624065)',
                    'APP:image_type': 'JPEG',
                    'Base:Filename': 'D:/projects/keh-photos-local/uploads/2021-11-22\\\\387385-3464354_08.jpg',
                    'Base:Format': 'JPEG',
                    'Base:Data_Type': 'uint8',
                    'Base:Bit_Depth_(per_Channel)': '8',
                    'Base:Bit_Depth_(per_Pixel)': 24,
                    'Base:Number_of_Channels': 3,
                    'Base:Mode': 'RGB',
                    'Base:Palette': None,
                    'Base:Width': 400,
                    'Base:Height': 400,
                    'Base:Megapixels': 0.16,
                    'EXIF:GPSInfoIFD': 11942,
                    'EXIF:ResolutionUnit': 2,
                    'EXIF:ExifIFD': 216, 'EXIF:Make': 'Canon',
                    'EXIF:Model': 'Canon EOS 6D',
                    'EXIF:Software': 'Ortery Photography Solutions',
                    'EXIF:Orientation': 1,
                    'EXIF:DateTime': '2021:11:19 16:03:46',
                    'EXIF:YCbCrPositioning': 2,
                    'EXIF:ReferenceBlackWhite': (0.0, 255.0, 128.0, 255.0, 128.0, 255.0),
                    'EXIF:YResolution': 0.0,
                    'EXIF:Copyright': '',
                    'EXIF:XResolution': 0.0,
                    'EXIF:Artist': '',
                    'error': 'Exception err: D:/projects/keh-photos-local/uploads/2021-11-22\\\\371656-3469730_08.jpg '
                             '- Error MSG: Could not find a backend to open '
                             '`D:/projects/keh-photos-local/uploads/2021-11-22\\\\371656-3469730_08.jpg`` with iomode '
                             '`ri`.',
                    'OEM': 'MFG',
                    'copy': '1',
                    'iptc:title': 'test me',
                    'iptc:description': 'we all',
                    'iptc:headline': 'no only you',
                    'iptc:city': 'Bear Cave',
                    'iptc:copyright': 'me',
                    'base64_error': 0}]
        msg = "Cannot create report"

        for idx, value in enumerate(content):
            self.assertTrue(self.ijs_report.create_file_report(path, file_name, value), msg)

    def test_insert_csv_to_sql_convert(self):
        msg = 'Failed to convert the csv record to the insert statement'
        database_table = "it-department-150323.bq_data_warehouse_dev.image_inventory"
        csv_record = '207750,3464082,,1,0,0,,,,,,,X:/uploads/2022-01-03/207750-3464082_01.jpg,128870,1/4/2022 4:30,' \
                     '1/4/2022 4:30,"os.stat_result(st_mode=33206, st_ino=13816, st_dev=3562129770, st_nlink=1, ' \
                     'st_uid=0, st_gid=0, st_size=128870, st_atime=1641252647, st_mtime=1641252647, ' \
                     'st_ctime=1641252647)",JPEG,X:/uploads/2022-01-03/207750-3464082_01.jpg,JPEG,uint8,8,24,3,RGB,,' \
                     '1000,1000,1,11918,2,316,Canon,Canon EOS 6D,Ortery Photography Solutions,1,2022:01:04 09:03:12,' \
                     '2,"(0.0, 255.0, 128.0, 255.0, 128.0, 255.0)",0,,0,,,,,,,,,,,,,,,,,,,,,,, | '
        assert_value = "INSERT INTO it-department-150323.bq_data_warehouse_dev.image_inventory(model_id,item_id," \
                       "barcode,sequence,no_content,base64_error,height,width,OEM,copy,copy_pos_4,copy_pos_5,APP_file_name," \
                       "META_file_size,META_creation_date,META_last_modified,META_file_stats,APP_image_type," \
                       "Base_Filename,Base_Format,Base_Data_Type,Base_Bit_Depth_per_Channel,Base_Bit_Depth_per_Pixel," \
                       "Base_Number_of_Channels,Base_Mode,Base_Palette,Base_Width,Base_Height,Base_Megapixels," \
                       "EXIF_GPSInfoIFD,EXIF_ResolutionUnit,EXIF_ExifIFD,EXIF_Make,EXIF_Model,EXIF_Software," \
                       "EXIF_Orientation,EXIF_DateTime,EXIF_YCbCrPositioning,EXIF_ReferenceBlackWhite,EXIF_YResolution," \
                       "EXIF_Copyright,EXIF_XResolution,EXIF_Artist,iptc_title,iptc_description,iptc_headline,iptc_city," \
                       "iptc_copyright,iptc_country_primary,iptc_country_detail,iptc_creator,iptc_creator_job_title," \
                       "iptc_credit_line,iptc_date_created,iptc_time_created,iptc_caption_description_writer," \
                       "iptc_instructions,iptc_intellectual_genre,iptc_job_identifier,iptc_keywords,iptc_province_state," \
                       "iptc_source,iptc_subject_code,iptc_sub_location,error_STRING) VALUES ('207750','3464082',NULL," \
                       "'1','0','0',NULL,NULL,NULL,NULL,NULL,NULL,'X:/uploads/2022-01-03/207750-3464082_01.jpg'," \
                       "'128870','1/4/2022 4:30','1/4/2022 4:30','os.stat_result(st_mode=33206, st_ino=13816, " \
                       "st_dev=3562129770, st_nlink=1, st_uid=0, st_gid=0, st_size=128870, st_atime=1641252647, " \
                       "st_mtime=1641252647, st_ctime=1641252647)','JPEG','X:/uploads/2022-01-03/207750-3464082_01.jpg'," \
                       "'JPEG','uint8','8','24','3','RGB',NULL,'1000','1000','1','11918','2','316','Canon','Canon EOS " \
                       "6D','Ortery Photography Solutions','1','2022:01:04 09:03:12','2','(0.0, 255.0, 128.0, 255.0, " \
                       "128.0, 255.0)','0',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL," \
                       "NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'|'); "
        self.assertEquals(self.ijs_database.insert_csv_to_sql_convert(database_table, csv_record), assert_value, msg)

    def test_save_statement_to_sql_file(self):
        msg = 'Cannot save the sql statement to the sql file'
        path_file_name = '../output_data/sql_files/test_sql_file.sql'
        statement = "INSERT INTO it-department-150323.bq_data_warehouse_dev.image_inventory(model_id,item_id,barcode," \
                    "sequence,no_content,base64_error,height,width,OEM,copy,copy_pos_4,copy_pos_5,APP_file_name," \
                    "META_file_size,META_creation_date,META_last_modified,META_file_stats,APP_image_type," \
                    "Base_Filename,Base_Format,Base_Data_Type,Base_Bit_Depth_per_Channel,Base_Bit_Depth_per_Pixel," \
                    "Base_Number_of_Channels,Base_Mode,Base_Palette,Base_Width,Base_Height,Base_Megapixels," \
                    "EXIF_GPSInfoIFD,EXIF_ResolutionUnit,EXIF_ExifIFD,EXIF_Make,EXIF_Model,EXIF_Software," \
                    "EXIF_Orientation,EXIF_DateTime,EXIF_YCbCrPositioning,EXIF_ReferenceBlackWhite,EXIF_YResolution," \
                    "EXIF_Copyright,EXIF_XResolution,EXIF_Artist,iptc_title,iptc_description,iptc_headline,iptc_city," \
                    "iptc_copyright,iptc_country_primary,iptc_country_detail,iptc_creator,iptc_creator_job_title," \
                    "iptc_credit_line,iptc_date_created,iptc_time_created,iptc_caption_description_writer," \
                    "iptc_instructions,iptc_intellectual_genre,iptc_job_identifier,iptc_keywords,iptc_province_state," \
                    "iptc_source,iptc_subject_code,iptc_sub_location,error_STRING) VALUES ('207750','3464082',NULL," \
                    "'1','0','0',NULL,NULL,NULL,NULL,NULL,NULL,'X:/uploads/2022-01-03/207750-3464082_01.jpg'," \
                    "'128870','1/4/2022 4:30','1/4/2022 4:30','os.stat_result(st_mode=33206, st_ino=13816, " \
                    "st_dev=3562129770, st_nlink=1, st_uid=0, st_gid=0, st_size=128870, st_atime=1641252647, " \
                    "st_mtime=1641252647, st_ctime=1641252647)','JPEG','X:/uploads/2022-01-03/207750-3464082_01.jpg'," \
                    "'JPEG','uint8','8','24','3','RGB',NULL,'1000','1000','1','11918','2','316','Canon','Canon EOS " \
                    "6D','Ortery Photography Solutions','1','2022:01:04 09:03:12','2','(0.0, 255.0, 128.0, 255.0, " \
                    "128.0, 255.0)','0',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL," \
                    "NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'|'); "

        self.assertTrue(self.ijs_database.save_statement_to_sql_file(path_file_name, statement), msg)


if __name__ == '__main__':
    unittest.main()
