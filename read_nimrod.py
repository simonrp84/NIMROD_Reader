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
#
# LICENSE:
# This is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this.  If not, see <http://www.gnu.org/licenses/>.


import sys
import struct
import numpy as np
import nimrod_data_defs as ndd

def read_nimrod_data(input_file):
    print("Input file is", input_file)

    #Open the file for reading and check the initial header size
    file_id = open(input_file, "rb")
    record_length, = struct.unpack(">l", file_id.read(4))
    if (record_length != 512):
        raise RuntimeError("Incorrect record length", record_length)

    # Read the four main headers from the file
    print(" -   Reading header")
    int_hdr_bytes = np.fromfile(file_id, dtype=ndd.main_int_header_fmt, count=1)
    real_hdr_bytes = np.fromfile(file_id, dtype=ndd.main_real_header_fmt, count=1)
    char_hdr_bytes = np.fromfile(file_id, dtype=ndd.main_char_header_fmt, count=1)
    data_hdr_bytes = np.fromfile(file_id, dtype=ndd.data_header_fmt, count=1)
    record_length, = struct.unpack(">l", file_id.read(4))
    if (record_length != 512):
        raise RuntimeError("Incorrect record length", record_length)

    # Convert the four headers into one large header dictionary
    nimrod_output = {
        "I_Hdr": ndd.recarray2dict(int_hdr_bytes),
        "R_Hdr": ndd.recarray2dict(real_hdr_bytes),
        "C_Hdr": ndd.recarray2dict(char_hdr_bytes),
        "D_Hdr": ndd.recarray2dict(data_hdr_bytes)
        }
    print(" -   Header successfully read")

    # Compute size of the actual data array using header info
    data_array_size = (nimrod_output["I_Hdr"]['NumRows'][0].astype(np.int32) *
                       nimrod_output["I_Hdr"]['NumCols'][0].astype(np.int32))

    # Check the data record size is consistent with the array size
    record_length, = struct.unpack(">l", file_id.read(4))
    if (record_length != data_array_size * 2):
        raise RuntimeError("Incorrect record length. Got", record_length,
                           "expected", data_array_size * 2)

    # Create the data array format, then read data from file
    data_fmt = ndd.create_data_dtype(nimrod_output["I_Hdr"]['NumRows'][0],
                                     nimrod_output["I_Hdr"]['NumCols'][0])
    data_array = np.fromfile(file_id, dtype=data_fmt, count=1)

    # Radar data stores values multiplied by 32.
    nimrod_output['Data'] = np.squeeze(data_array['Data']) / 32.

    # Done reading data
    file_id.close()
    print(" -   Data successfully read")
    
    return nimrod_output
    

if __name__ == '__main__':
    # Get the input file from the command line
    if (len(sys.argv) < 2):
        print("Error: You must enter the input filename on the command line")
        quit()
    else:
        input_file = sys.argv[1]

    # Call the main function
    nimrod = read_nimrod_data(input_file)

    print(nimrod['R_Hdr']['Northing_Coord_Of_Start_Line'])
    print(nimrod['R_Hdr']['Easting_Coord_Of_Start_Line'])
    print(nimrod['R_Hdr']['Pixel_Size_In_Coords_X_Direction'])
    print(nimrod['R_Hdr']['Pixel_Size_In_Coords_Y_Direction'])
