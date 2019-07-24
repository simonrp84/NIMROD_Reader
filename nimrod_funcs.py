#!/usr/bin/python
# Functions for reading, processing and saving NIMROD data
# Copyright 2019, Simon R Proud, University of Oxford,
# Contact: simon.proud@physics.ox.ac.uk
#
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

import numpy as np
import gdal

def recarray2dict(arr):
    ''' Converts a numpy array with descriptions
    into a python dict, where the descriptions match
    the key names.
    This function is taken from the Satpy library:
    https://github.com/pytroll/satpy
    '''    
    res = {}
    for dtuple in arr.dtype.descr:
        key = dtuple[0]
        ntype = dtuple[1]
        data = arr[key]
        if isinstance(ntype, list):
            res[key] = recarray2dict(data)
        else:
            res[key] = data

    return res


def create_data_dtype(xs, ys):
    ''' This function creates the numpy format descriptor
    for the NIMROD main data array, based on the x and y sizes
    given in the header info
    '''    
    data_array_fmt = np.dtype([
        ("Data", '>i2', (xs, ys,))
    ])

    return data_array_fmt
