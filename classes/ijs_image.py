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
import imageio
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.TiffTags import TAGS
from PIL.PngImagePlugin import PngImageFile, PngInfo


class IJSImage(object):

    def check_image_content(self, url_path_file) -> dict | bool:
        dict_out = {}
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
            if img_type.format == "PNG":
                dict_png = self.get_png_data(image_name)
                dict_out.update(dict_png)
            # logging.debug(f"Image Content: {dict_out}")
            img_type.close()
        except OSError as os_err:
            dict_out['error'] = f"Cannot open image file: {url_path_file} - Error MSG: {os_err}"
            logging.error(f"OS Error: {dict_out}")
        except Exception as ex_err:
            dict_out['error'] = f"Exception err: {url_path_file} - Error MSG: {ex_err}"
            logging.error(f"Exception: {dict_out}")
        return dict_out

    def get_base_date(self, img_type, pic) -> dict:
        # Calculations
        megapixels = (img_type.size[0] * img_type.size[1] / 1000000)  # Megapixels
        d = re.sub(r'[a-z]', '', str(pic.dtype))  # Dtype
        t = len(Image.Image.getbands(img_type))  # Number of channels

        dict_base = {
            "Base:Filename": img_type.filename,
            "Base:Format": img_type.format,
            "Base:Data_Type": pic.dtype,
            "Base:Bit_Depth_(per_Channel)": d,
            "Base:Bit_Depth_(per_Pixel)": (int(d) * int(t)),
            "Base:Number_of_Channels": t,
            "Base:Mode": img_type.mode,
            "Base:Palette": img_type.palette,
            "Base:Width": img_type.size[0],
            "Base:Height": img_type.size[1],
            "Base:Megapixels": megapixels
        }
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
