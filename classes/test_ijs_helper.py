#!/usr/bin/env python
__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, image_junk_snooper project"
__license__ = ""
__version__ = "0.0.1"

import unittest
import logging
from datetime import date


class TestIJSHelper(unittest.TestCase):
    def setUp(self) -> None:
        log_data = "../log_data/log_files/"
        log_file_name = log_data + 'test_image_junk_snooper_' + str(date.today()) + '.log'
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s'
                            , filename=log_file_name, level=logging.DEBUG)
        from ijs_helper import IJSHelper
        self.ijs_helper = IJSHelper()

        self.url_path_file = '../output_data/test_file_report'

    def tearDown(self) -> None:
        pass

    def test_evaluate_model_item(self):
        file_names = ['my', 'big_black_bear.coder.jpg', '10000239654683_08.jpg', '33.jpg', '1780834-1958332_08',
                      '214510-2305437_05.jpg', '381966-3106923_02_MFG.jpg', '386759-3452409_03(1).jpg',
                      '330186-1_300x300.jpg', '330307_1_1000x1000.jpg', '331220_1_1000x1000_1.jpg',
                      '331263-2882_470x313.jpg', '330870_1_1000x1000_1_2.jpg', 'model_378836_417x417.jpg',
                      'model_378836_417x417_1.jpg', 'model341884.jpg', 'model378835_500x500.jpg',
                      'model378461_1_1000x1000.jpg', 'model378307_2_1000x1000_1.jpg', 'model368174_1.jpg']
        msg = 'Evaluation failed'
        self.assertIsInstance(self.ijs_helper.evaluate_model_item(file_names[3]), dict, msg)

    def test_eval_item_1(self):
        # file_name = '33'
        file_name = '1780834-1958332'
        # file_name = '214510-2305437'
        # file_name = '330186'
        # file_name = '331263-2882'
        # file_name = 'model'
        # file_name = 'model341884'
        # file_name = '10000239654683'
        msg = 'Item 1 Evaluation failed'
        self.assertIsInstance(self.ijs_helper.eval_item_1(file_name), dict, msg)

    def test_eval_item_2(self):
        # file_name = '08'      # sequence
        # file_name = '03(1)'   # sequence(copy)
        # file_name = '300x300' # Height x Width
        # file_name = '1'       # sequence
        file_name = '100'       # sequence
        # file_name = '378836'  # model_id

        msg = 'Item 2 Evaluation failed'
        self.assertIsInstance(self.ijs_helper.eval_item_2(file_name), dict, msg)

    def test_check_id(self):
        test_id = '37883'         # fail
        # test_id = '378836'      # pass
        # test_id = '3788360'     # pass
        # test_id = '37883601'    # pass
        # test_id = '137883601'   # fail

        msg = 'Check id failed'
        self.assertTrue(self.ijs_helper.check_id(test_id), msg)

    def test_get_height_width(self):
        name = '300x300'

        msg = 'Getting height and width failed'
        self.assertIsInstance(self.ijs_helper.get_height_width(name), dict, msg)

    def test_get_sequence_copy(self):
        name = '04(2)'

        msg = 'Getting sequence and copy failed'
        self.assertIsInstance(self.ijs_helper.get_sequence_copy(name), dict, msg)


if __name__ == '__main__':
    unittest.main()
