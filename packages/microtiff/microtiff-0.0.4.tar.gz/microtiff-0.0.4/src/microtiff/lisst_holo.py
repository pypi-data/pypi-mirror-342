#!/bin/python3

# Copyright 2024, A Baldwin, S Giering, W Major and M Masoudi
#
# This file is part of microtiff.
#
# microtiff is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# microtiff is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with microtiff.  If not, see <http://www.gnu.org/licenses/>.

'''
lisst_holo.py

A converter for image data from the LISST-Holo and LISST-Holo2 holographic sensors
'''

import argparse
import os
import re
import csv
import json
from PIL import Image
from PIL.TiffImagePlugin import ImageFileDirectory_v2
import numpy as np
import matplotlib.pyplot as plt

# Specific to the PGM spec
def is_whitespace(char):
    if char == ' ':
        return True
    if char == '\t':
        return True
    if char == '\r':
        return True
    if char == '\n':
        return True
    return False

def read_string_till_space(fp):
    str_out = ""
    reading = False
    while True:
        char = chr(fp.read(1)[0])
        if reading:
            if is_whitespace(char):
                return str_out
            else:
                str_out = str_out + char
        else:
            # We don't want multiple spaces (or CRLF!) to return empty strings
            if not is_whitespace(char):
                reading = True
                str_out = str_out + char

def extract_image(target, no_metadata = False):
    image_map = []
    outputs = []
    with open(target + ".pgm", "rb") as f:
        bd = 255
        imd_start_byte = 0
        height = 0
        width = 0
        f.seek(0)
        header = ""
        footer = ""
        while imd_start_byte == 0:
            if not read_string_till_space(f) == "P5":
                raise ValueError("Invalid start to a PGM file")
            width = int(read_string_till_space(f))
            height = int(read_string_till_space(f))
            bd = int(read_string_till_space(f))
            imd_start_byte = f.tell()
        two_byte = False
        # Caveat of PGM files: they sometimes have more than 8 bpp. While the Holo2 doesn't, a future sensor might.
        if (bd > 255):
            two_byte = True
        imd_length = height * width
        if (two_byte):
            imd_length = imd_length * 2
        # Ignore zero-size images
        if (height * width > 0):
            f.seek(imd_start_byte)
            imdata = f.read(imd_length)
            imdata_reform = None
            if (two_byte):
                imdata_reform = np.reshape(np.frombuffer(imdata, dtype=np.uint16), (height, width))
            else:
                imdata_reform = np.reshape(np.frombuffer(imdata, dtype=np.uint8), (height, width))

            image = Image.fromarray(imdata_reform, "L")
            im_metadata = {}
            if not no_metadata:
                with open(target + ".json", "w") as f:
                    json.dump(im_metadata, f, ensure_ascii=False)
                outputs.append(target + ".json")
            image.save(target + ".tiff", "TIFF")

            outputs.append(target + ".tiff")

    return outputs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--exclude-metadata", action="store_true", required=False, help="don't add metadata to resulting image files.")
    parser.add_argument("file", nargs='+', help="any number of .pgm files")

    args = parser.parse_args()

    in_files = args.file
    targets = []

    for in_file in in_files:
        in_file_s = os.path.splitext(in_file)
        if in_file_s[1] == ".pgm":
            targets.append(in_file_s[0])
        else:
            print("invalid extension \"" + in_file_s[1][1:] + "\" in file \"" + in_file + "\", ignoring")

    # Get rid of duplicates
    targets = list(set(targets))

    for target in targets:
        extract_image(target, no_metadata = args.exclude_metadata)

