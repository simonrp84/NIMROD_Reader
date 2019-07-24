#!/usr/bin/python
# This script can be used to read data in the Met Office NIMROD format
# It has been tested with data supplied via the BADC.
# Copyright 2019, Simon R Proud, University of Oxford,
# Contact: simon.proud@physics.ox.ac.uk
#
#
# Inspired by the original read_nimrod.py file created by Charles Kilburn
# This script is for Python 3, and uses numpy + dicts to store the headers
#
#
# Usage:
# python read_nimrod.py input_file_name
#   -   where input_file_name is a NIMROD file, uncompressed
# NOTE: This script has only been tested on 1km composite radar data
# Bugs: None known


import sys
import struct
import numpy as np
import nimrod_data_defs as ndd

input_file = sys.argv[1]

print("Input file is", input_file)

file_id = open(input_file, "rb")
record_length, = struct.unpack(">l", file_id.read(4))
if (record_length != 512):
    raise RuntimeError("Incorrect record length", record_length)
print(" -   Reading header")
int_hdr_bytes = np.fromfile(file_id, dtype=ndd.main_int_header_fmt, count=1)
real_hdr_bytes = np.fromfile(file_id, dtype=ndd.main_real_header_fmt, count=1)
char_hdr_bytes = np.fromfile(file_id, dtype=ndd.main_char_header_fmt, count=1)
data_hdr_bytes = np.fromfile(file_id, dtype=ndd.data_header_fmt, count=1)
record_length, = struct.unpack(">l", file_id.read(4))
if (record_length != 512):
    raise RuntimeError("Incorrect record length", record_length)

header = {
    "Int_Header": ndd.recarray2dict(int_hdr_bytes),
    "Real_Header": ndd.recarray2dict(real_hdr_bytes),
    "Char_Header": ndd.recarray2dict(char_hdr_bytes),
    "Data_Header": ndd.recarray2dict(data_hdr_bytes)
    }
print(" -   Header successfully read")

data_array_size = (header["Int_Header"]['NumRows'][0].astype(np.int32) *
                   header["Int_Header"]['NumCols'][0].astype(np.int32))

record_length, = struct.unpack(">l", file_id.read(4))
if (record_length != data_array_size * 2):
    raise RuntimeError("Incorrect record length. Got", record_length,
                       "expected", data_array_size * 2)

data_fmt = ndd.create_data_array_dtype(header["Int_Header"]['NumRows'][0],
                                       header["Int_Header"]['NumCols'][0])
data_array = np.fromfile(file_id, dtype=data_fmt, count=1)
data_array = np.squeeze(data_array['Data']) / 32.
file_id.close()

print(" -   Data successfully read")
