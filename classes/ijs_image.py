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
import re
import imageio
from PIL import Image, IptcImagePlugin
from PIL.ExifTags import TAGS
from PIL.TiffTags import TAGS
from PIL.PngImagePlugin import PngImageFile, PngInfo
import base64


class IJSImage(object):
    # IPTC fields are catalogued in:
    # https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata
    dict_iptc_meta = {
        1: ['iptc:title', 2, 5],
        2: ['iptc:description', 2, 120],
        3: ['iptc:headline', 2, 105],
        4: ['iptc:city', 2, 90],
        5: ['iptc:copyright', 2, 116],
        6: ['iptc:country_primary', 2, 101],
        7: ['iptc:country_detail', 2, 100],
        8: ['iptc:creator', 2, 80],
        9: ['iptc:creator_job_title', 2, 85],
        10: ['iptc:credit_line', 2, 110],
        11: ['iptc:date_created', 2, 55],
        12: ['iptc:time_created', 2, 60],
        13: ['iptc:caption_description_writer', 2, 122],
        14: ['iptc:instructions', 2, 40],
        15: ['iptc:intellectual_ genre', 2, 4],
        16: ['iptc:job_identifier', 2, 103],
        17: ['iptc:keywords', 2, 25],
        18: ['iptc:province_state', 2, 95],
        19: ['iptc:source', 2, 115],
        20: ['iptc:subject_code', 2, 12],
        21: ['iptc:sub_location', 2, 92],
    }

    def check_image_content(self, url_path_file) -> dict | bool:
        dict_out = {'base64_error': 0}
        try:
            # path to the image or video
            image_name = url_path_file
            pic = imageio.imread(image_name)
            # read the image data using PIL
            img_type = Image.open(image_name)
            dict_out['APP:image_type'] = img_type.format
            dict_base = self.get_base_date(img_type, pic)
            dict_out.update(dict_base)
            dict_exif = self.get_exif_data(img_type)
            dict_out.update(dict_exif)
            dict_iptc = self.get_ITPC_data(image_name)
            dict_out.update(dict_iptc)
            if img_type.format == "PNG":
                dict_png = self.get_png_data(image_name)
                dict_out.update(dict_png)
            """Check if image can be converted to base64"""
            if not self.test_base64_convert(image_name):
                dict_out['base64_error'] = 1
            logging.debug(f"Image Content: {dict_out}")
            img_type.close()
        except OSError as os_err:
            dict_out['error'] = f"Cannot open image file::Error MSG: {os_err}"
            logging.error(f"OS Error: {dict_out}")
            return False
        except Exception as ex_err:
            dict_out['error'] = f"Exception err::Error MSG: {ex_err}"
            logging.error(f"Exception: {dict_out}")
            return False
        return dict_out

    def get_base_date(self, img_type, pic) -> dict:
        # Calculations
        megapixels = (img_type.size[0] * img_type.size[1] / 1000000)  # Megapixels
        d = re.sub(r'[a-z]', '', str(pic.dtype))  # Dtype
        t = len(Image.Image.getbands(img_type))  # Number of channels

        dict_base = {
            "Base:Filename": img_type.filename,
            "Base:Format": img_type.format,
            "Base:Data_Type": f"{pic.dtype}",
            "Base:Bit_Depth_(per_Channel)": d,
            "Base:Bit_Depth_(per_Pixel)": (int(d) * int(t)),
            "Base:Number_of_Channels": t,
            "Base:Mode": img_type.mode,
            "Base:Palette": img_type.palette,
            "Base:Width": img_type.size[0],
            "Base:Height": img_type.size[1],
            "Base:Megapixels": megapixels
        }
        logging.debug(f"Check Image Content: {dict_base}")
        return dict_base

    def get_exif_data(self, obj_img) -> dict:
        dict_exif = {}
        # extract EXIF data
        exif_data = obj_img.getexif()
        # iterating over all EXIF data fields
        for tag_id in exif_data:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            # decode bytes
            if isinstance(data, bytes):
                data = data.decode()
            dict_exif['EXIF:' + tag] = data
        return dict_exif

    def get_tiff_data(self, obj_img) -> dict:
        dict_img = {}
        # extract EXIF data
        exif_data = obj_img.gettiff()
        # iterating over all EXIF data fields
        for tag_id in exif_data:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            # decode bytes
            if isinstance(data, bytes):
                data = data.decode()
            dict_img[tag] = data
        return dict_img

    def get_png_data(self, img) -> dict:
        img = PngImageFile(img)
        metadata = PngInfo()
        arr_exif = []
        dict_png = {}

        # Compile array from tags dict
        for i in img.text:
            png_compile = i, str(img.text[i])
            arr_exif.append(png_compile)
        # If XML metadata, pull out data by identifying data type and gathering useful meta
        if len(arr_exif) > 0:
            header = arr_exif[0][0]
        else:
            header = ""
            logging.error(f"No available metadata: {img}")
        xml_output = []
        if header.startswith("XML"):
            xml = arr_exif[0][1]
            xml_output.extend(xml.splitlines())
            # Remove useless meta tags
            for line in xml.splitlines():
                if "<" not in line:
                    if "xmlns" not in line:
                        # Remove equal signs, quotation marks, /> characters and leading spaces
                        xml_line = re.sub(r'[a-z]*:', '', line).replace('="', ': ')
                        xml_line = xml_line.rstrip(' />')
                        xml_line = xml_line.rstrip('\"')
                        xml_line = xml_line.lstrip(' ')
                        arr_exif.append(xml_line)

        elif header.startswith("Software"):
            logging.error(f"No available metadata: {img}")

        # If no XML, print available metadata
        else:
            for properties in arr_exif:
                if properties[0] != 'JPEGThumbnail':
                    arr_exif.append(': '.join(str(x) for x in properties))

        dict_png['PNG:meta_data'] = arr_exif
        dict_png['PNG:raw_meta_data'] = metadata
        return dict_png

    def test_base64_convert(self, pic) -> bool:
        try:
            image = open(pic, 'rb')
            image_read = image.read()
            base64.encodebytes(image_read)
            logging.info(f"Converted image: {pic} to base64")
            image.close()
            return True
        except base64.binascii.Error:
            logging.error(f"Cannot base64 image: {pic}. Error: {base64.binascii.Error}")
            image.close()
            return False
        except FileNotFoundError as fnferr:
            logging.error(f"Cannot open file for base64 check: {pic}. FileNotFoundError: {fnferr}")
            return False
        except IOError as ioerr:
            logging.error(f"Cannot open file for base64 check: {pic}. IOError: {ioerr}")
            image.close()
            return False

    def get_ITPC_data(self, pic) -> dict:
        try:
            img = Image.open(pic)
            raw_iptc = IptcImagePlugin.getiptcinfo(img)
            dict_out = {}
            for key, value in self.dict_iptc_meta.items():
                if raw_iptc and (value[1], value[2]) in raw_iptc:
                    if isinstance(raw_iptc[(value[1], value[2])], list):
                        dict_out[value[0]] = []
                        for idx, val in enumerate(raw_iptc[(value[1], value[2])]):
                            dict_out[value[0]].append(val.decode('utf-8', errors='replace'))
                    else:
                        dict_out[value[0]] = raw_iptc[(value[1], value[2])].decode('utf-8', errors='replace')
            img.close()
            return dict_out
        except SyntaxError:
            logging.info('IPTC Error in %s', pic)
            return dict_out
