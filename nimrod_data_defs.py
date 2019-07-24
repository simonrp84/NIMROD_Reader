#!/usr/bin/python
# Stores the definitions for each type of header data in the NIMROD format
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


# This is the first header, which stores only int16
main_int_header_fmt = np.dtype([
    ("VTyear", '>i2'),  # 1
    ("VTmonth", '>i2'),  # 2
    ("VTday", '>i2'),  # 3
    ("VThour", '>i2'),  # 4
    ("VTminute", '>i2'),  # 5
    ("VTsecond", '>i2'),  # 6
    ("DTyear", '>i2'),  # 7
    ("DTmonth", '>i2'),  # 8
    ("DTday", '>i2'),  # 9
    ("DThour", '>i2'),  # 10
    ("DTminute", '>i2'),  # 11
    ("DataType", '>i2'),  # 12
    ("NumBytes", '>i2'),  # 13
    ("ExperimentNumber", '>i2'),  # 14
    ("HorizontalGridType", '>i2'),  # 15
    ("NumRows", '>i2'),  # 16
    ("NumCols", '>i2'),  # 17
    ("HeaderNum", '>i2'),  # 18
    ("FieldCodeNum", '>i2'),  # 19
    ("VerticalCoordType", '>i2'),  # 20
    ("VerticalCoordRefLevel", '>i2'),  # 21
    ("NumElementsFrm60", '>i2'),  # 22
    ("NumElementsFrm109", '>i2'),  # 23
    ("OriginLocation", '>i2'),  # 24
    ("MissingValue", '>i2'),  # 25
    ("InterestPeriodMins", '>i2'),  # 26
    ("NumModelLevels", '>i2'),  # 27
    ("ProjectionEllipsoid", '>i2'),  # 28
    ("EnsembleMemberID", '>i2'),  # 29
    ("OriginModelID", '>i2'),  # 30
    ("TimeAveraging", '>i2')  # 31
])

# Second header, for float32
main_real_header_fmt = np.dtype([
    ("Vert_Coord_Val", '>f4'),  # 32
    ("Vert_Coord_Ref", '>f4'),  # 33
    ("Northing_Coord_Of_Start_Line", '>f4'),  # 34
    ("Pixel_Size_In_Coords_Y_Direction", '>f4'),  # 35
    ("Easting_Coord_Of_Start_Line", '>f4'),  # 36
    ("Pixel_Size_In_Coords_X_Direction", '>f4'),  # 37
    ("Missing_Data_Value", '>f4'),  # 38
    ("MKS_Scaling_Factor", '>f4'),  # 39
    ("Data_Offset_Value", '>f4'),  # 40
    ("X_Offset_Model_To_Grid", '>f4'),  # 41
    ("Y_Offset_Model_To_Grid", '>f4'),  # 42
    ("Latitude_Of_True_Origin", '>f4'),  # 43
    ("Longitude_Of_True_Origin", '>f4'),  # 44
    ("Easting_Of_True_Origin", '>f4'),  # 45
    ("Northing_Of_True_Origin", '>f4'),  # 46
    ("Scale_Factor_Central_Meridian", '>f4'),  # 47
    ("Prob_Perc_Threshold", '>f4'),  # 48
    ("General_Header", '>f4', (11,)),  # 49-59
    ("Northing_Top_Left", '>f4'),  # 60
    ("Easting_Top_Left", '>f4'),  # 61
    ("Northing_Top_Right", '>f4'),  # 62
    ("Easting_Top_Right", '>f4'),  # 63
    ("Northing_Bottom_Right", '>f4'),  # 64
    ("Easting_Bottom_Right", '>f4'),  # 65
    ("Northing_Bottom_Left", '>f4'),  # 66
    ("Easting_Bottom_Left", '>f4'),  # 67
    ("Satellite_Cal_Coeff", '>f4'),  # 68
    ("Space_Count", '>f4'),  # 69
    ("Ducting_Index", '>f4'),  # 70
    ("Elevation_Angle", '>f4'),  # 71
    ("Neighbourhood_Size", '>f4'),  # 72
    ("Radius_Of_Interest", '>f4'),  # 73
    ("Recursive_Filter_Strength", '>f4'),  # 74
    ("Fuzzy_Threshold_Param", '>f4'),  # 75
    ("Fuzzy_Duration_Occurence", '>f4'),  # 76
    ("Spare", '>f4', (28,))  # 77-104
])

# Character header
main_char_header_fmt = np.dtype([
    ('Field_Units', 'S8'),  # 105
    ('Data_Source', 'S24'),  # 106
    ('Field_Title', 'S24')  # 107
])

# Data specific header, note that only radar is supported here
data_header_fmt = np.dtype([
    ('Single_Site_Radar_Number', '>i2'),  # 108
    ('Composite_Radars_Used_1', '>i2'),  # 109
    ('Composite_Radars_Used_2', '>i2'),  # 110
    ('Clutter_Map_Number', '>i2'),  # 111
    ('Calibration_Type', '>i2'),  # 112
    ('Bright_Band_Height', '>i2'),  # 113
    ('Bright_Band_Intensity', '>i2'),  # 114
    ('Bright_Band_Test_P1', '>i2'),  # 115
    ('Bright_Band_Test_P2', '>i2'),  # 116
    ('Infill_Flag', '>i2'),  # 117
    ('Stop_Elevation', '>i2'),  # 118
    ('COSMOS_Header_1', '>i2', (13,)),  # 119-131
    ('COSMOS_Header_2', '>i2', (8,)),  # 132-139
    ('Sat_Sensor_ID', '>i2'),  # 140
    ('Meteosat_ID', '>i2'),  # 141
    ('Synop_Availability', '>i2'),  # 143
    ('Data_Specific_Entries', '>i2', (15,)),  # 144-159
    ('Period_Of_Interest_Accum', '>i2')  # 159
])
