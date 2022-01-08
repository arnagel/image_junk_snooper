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
import pprint

import logging


class Barcode:

    def __init__(self):
        pass

    def read_barcode(self, code) -> dict | bool:
        type_id = code[0:-2]
        cd = int(code[-2:])
        verify = self.check_digit(type_id)
        if cd == verify:
            return {'id': int(type_id[2:]),
                    'type': int(type_id[0:2]),
                    'check': int(verify)}

        return False

    def check_digit(self, code) -> int:
        len_code = len(str(code))
        o = e = 0

        for i in range(0, len_code, 2):
            b_1 = bytes(code[i], 'UTF-8')
            o += b_1[0]
            if i + 1 < len_code:
                b_2 = bytes(code[i + 1], 'UTF-8')
                e += b_2[0]
            else:
                e += 0

        cd = ((o * 3) + e) % 100
        return 99 - cd
