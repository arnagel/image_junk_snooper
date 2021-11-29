#!/usr/bin/env python
from __future__ import annotations

__author__ = "Andreas Nagel"
__copyright__ = "Copyright 2021, Image Junk Snooper"
__credits__ = []
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "anagel@keh.com"
__status__ = "Development"
__package__ = "image_junk_snooper"
__github__ = 'https://github.com/arnagel/image_junk_snooper.git'

# imports
import logging
import pprint
import re
import sys
from typing import Union
from datetime import datetime


class IJSHelper:

    def __init__(self):
        pass

    def evaluate_model_item(self, file_name) -> dict:
        """different formats of model/item/barcode filename:

        barcode, model_id, item_id, seq, copy_1, copy_2, ?
        , height, width, pre_text, post_text, other

        Split by period (.)
        Split by underscore (_)

        item #1a = numeric with hyphen

        item #2a = 01 - 20
        item #2b = has x
        item #2c = has single digit
        item #2d = numeric len >= 6
        item #2e = has ( and )

        [item #3a = numeric, single digit]
        [item #3b = alpha]
        [item #3c = has x]

        [item #4a = numeric, single digit]

        [item #5a = numeric, single digit]

        1780834-1958332_08.jpg: model_id-item_id_sequence
        214510-2305437_05.jpg: model_id-item_id_sequence
        381966-3106923_02_MFG.jpg: model_id-item_id_sequence_text
        386759-3452409_03(1).jpg: model_id-item_id_sequence(copies)

        330186-1_300x300.jpg: model_id-sequence_HxW
        330307_1_1000x1000.jpg: model_id-sequence_HxW
        331220_1_1000x1000_1.jpg: model_id-sequence_HxW_copies
        331263-2882_470x313.jpg: model_id-?_HxW
        330870_1_1000x1000_1_2.jpg : model_id-sequence_HxW_copies_copies

        model_378836_417x417.jpg: text_model_HxW
        model_378836_417x417_1.jpg: text_model_HxW_sequence
        model341884.jpg: textmodel
        model378835_500x500.jpg: textmodel_HxW
        model378461_1_1000x1000.jpg: textmodel_sequence_HxW
        model378307_2_1000x1000_1.jpg: textmodel_sequence_HxW_copies
        model368174_1.jpg: textmodel_sequence
        10000239654683_08.jpg: barcode
        33.jpg - Other not applicable/Disregard
        """
        dict_out = {}
        if file_name:
            split_period = file_name.split('.')
            pprint.pprint(f"Period Split: :{split_period}")
            len_period = len(split_period)
            if len_period <= 1 or len_period > 2:
                dict_out["error"] = file_name
                return dict_out
            """We use only item 0 from the returned period list"""
            name = split_period[0]
            """Underscore split"""
            split_name = name.split('_')
            pprint.pprint(f"Underscore Split: :{split_name}")

            """Evaluate the first item in the return underscore list"""
            dict_name = self.eval_item_1(split_name[0])
            dict_out.update(dict_name)
            dict_name = self.eval_item_2(split_name[1])
            dict_out.update(dict_name)

            if 'error' in dict_out:
                pprint.pprint(f"Eval model item: :{dict_out}")
                return dict_out

            pprint.pprint(f"Eval model item: :{dict_out}")
            return dict_out
        else:
            dict_out["error"] = file_name
            return dict_out

    def eval_item_1(self, name) -> dict:
        """
        #1a1 = split hyphen
        $1a2 = item 1 > 6 (model_id)
        $1a3 = item 2 > 6 (item_id)
        """
        """check if we have a hyphen in the name"""
        f_str = "-"
        dict_item = {}
        if f_str not in name:
            """No hyphen 
            item #1b = numeric len > 10
            item #1c = alphanumeric
            item #1d = alpha"""
            len_name = len(name)
            if name.isnumeric():
                if len_name > 10:
                    """Barcode"""
                    dict_item["barcode"] = name
                elif self.check_id(name):
                    """model_id"""
                    dict_item["model_id"] = name
                else:
                    dict_item["error"] = name
            elif name.isalnum():
                """We have something like model23455"""
                temp = re.compile("([a-zA-Z]+)([0-9]+)")
                res = temp.match(name).groups()
                dict_item["model_id"] = res[1]
            elif isinstance(name, str):
                """nothing we can use"""
                dict_item["error"] = name
        else:
            """We have a hyphen and need to split"""
            split_hyphen = name.split('-')
            if self.check_id(split_hyphen[0]):
                dict_item["model_id"] = split_hyphen[0]
            else:
                dict_item["error"] = split_hyphen[0]
            if self.check_id(split_hyphen[1]):
                dict_item["item_id"] = split_hyphen[1]
            else:
                dict_item["error"] = split_hyphen[1]
        return dict_item

    def eval_item_2(self, name) -> dict:
        """
        item  # 2a = 01 - 20
        item  # 2b = has x
        item  # 2c = has single digit
        item  # 2d = numeric len >= 6
        item  # 2e = has ( and ) """
        dict_out = {}
        x_str = "x"
        bracket_str = "("
        if x_str in name:
            pprint.pprint(f"Found x: {name}")
            dict_out = self.get_height_width(name)
        elif bracket_str in name:
            pprint.pprint(f"Found brackets: {name}")
            dict_out = self.get_sequence_copy(name)
        elif len(name) > 5:
            pprint.pprint(f"Found model id: {name}")
            if self.check_id(name):
                dict_out['model_id'] = name
        elif int(name) in range(0, 99):
            pprint.pprint(f"Found sequence: {name}")
            dict_out = {'sequence': name}
        else:
            dict_out = {"error": f"No match for: {name}"}

        pprint.pprint(f"Dict Out: {dict_out}")

        return dict_out





        pass

    def get_sequence_copy(self, str_s_c) -> dict:
        lst_s_c = str_s_c.split('(')
        return {'sequence': lst_s_c[0], 'copy': lst_s_c[1].rstrip(')')}

    def get_height_width(self, str_h_w) -> dict:
        lst_h_w = str_h_w.split('x')
        return {'height': lst_h_w[0], 'width': lst_h_w[1]}

    def check_id(self, test_id) -> bool:
        len_test_id = len(test_id)
        if 6 <= len_test_id <= 8:
            return True
        return False
