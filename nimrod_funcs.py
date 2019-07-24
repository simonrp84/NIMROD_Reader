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

from osgeo import gdal, osr
import numpy as np


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


def create_gdal_output(nimrod, output_file):
    ''' This function creates a GDAL TIFF file with projection
    information from the NIMROD dataset, and saves it to disk.
    '''
    # Option 0 is the UK 1km composite data
    # Option 3 is the European 5km composite data
    if (nimrod["I_Hdr"]['HorizontalGridType'][0] != 0):
        print("THIS PROJECTION IS NOT SUPPORTED")
    else:
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(27700)
        sr_wkt = srs.ExportToWkt()

        x_px = nimrod["I_Hdr"]['NumRows'][0]
        y_px = nimrod["I_Hdr"]['NumCols'][0]
        px_size_x = nimrod["R_Hdr"]['Pixel_Size_In_Coords_X_Direction'][0]
        px_size_y = nimrod["R_Hdr"]['Pixel_Size_In_Coords_Y_Direction'][0]

        northing = nimrod["R_Hdr"]['Northing_Coord_Of_Start_Line'][0]
        easting = nimrod["R_Hdr"]['Easting_Coord_Of_Start_Line'][0]

        driver = gdal.GetDriverByName('GTiff')

        dataset = driver.Create(output_file,
                                int(y_px),
                                int(x_px),
                                1,
                                gdal.GDT_Float32)

        dataset.SetGeoTransform((
            easting,    # 0
            px_size_y,  # 1
            0,                      # 2
            northing,    # 3
            0,                      # 4
            -px_size_x))

        dataset.SetProjection(sr_wkt)
        dataset.GetRasterBand(1).WriteArray(nimrod['Data'])
