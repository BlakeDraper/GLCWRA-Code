"""
CalculateIndexWeb.py
Ian McNair
Last Edit: 9/9/2016
Seeks to define a function that performs the restoration index calculation on a
given area given a set of 7 rasters (parameter 0 through parameter 6) and weight associated with each.
"""

import arcpy

# Check out the spatial analysis extension
arcpy.CheckOutExtension('Spatial')

# Allows the script to overrite files if necessary
arcpy.env.overwriteOutput = True
# Sets the cell size for the environment
arcpy.env.cellSize = 10

# Establishes a base path since the parameter rasters are all in the same folder
base_path = 'C:/Workspace/IndexTest/Data/WLERA_Raster_Data'

# Sets the file locations for the parameters as variables
p0 = arcpy.Raster(base_path + '/WLERA_P0_Mask_Water.tif')
p1 = arcpy.Raster(base_path + '/WLERA_P1_Hydroperiod.tif')
p2 = arcpy.Raster(base_path + '/WLERA_P2_WetlandSoils.tif')
p3 = arcpy.Raster(base_path + '/WLERA_P3_Flowlines.tif')
p4 = arcpy.Raster(base_path + '/WLERA_P4_CARL.tif')
p5 = arcpy.Raster(base_path + '/WLERA_P5_Impervious.tif')
p6 = arcpy.Raster(base_path + '/WLERA_P6_Landuse.tif')


def getIndex(p0, p1, p2, p3, p4, p5, p6):
    #    Sets weights for each parameter.
    w1 = 10
    w2 = 5
    w3 = 7.5
    w4 = 2.5
    w5 = 7.5
    w6 = 2.5

    #Begin calculations based on Justin Saarinen's instruction
    #Apply the weights to all of the parameters
    #Parameters 1 and 5 range from 0-100, so we divide by 10 to normalize their values
    wp1 = (p1 * w1) / 10
    wp2 = p2 * w2
    wp3 = p3 * w3
    wp4 = p4 * w4
    wp5 = (p5 * w5) / 10
    wp6 = p6 * w6

    # Establish the 'positive parameter' values - higher values in these parameters should provide additional restorability likelihood
    pos = wp1 + wp2 + wp3 + wp4
    # pos_max indicates the highest possible weight
    pos_max = (w1 * 10) + w2 + w3 + (w4 * 4)
    pos_term = pos / pos_max
    
    # Establish the 'negative' parameter values - higher values in these parameters should provide lower restorability likelihood
    neg = wp5 + wp6
    # neg_max indicates the highest possible weight
    neg_max = (w5 * 10) + w6
    neg_term = neg / neg_max

    # Subtract the negative term from the positive term, which gets the prescore values
    prescore = pos_term - neg_term
    # Multiply the prescore values by 100 to shift the values, then multiply by the value of the water mask parameter
    # If an area is not suitable for restoration because it is in the water, it will have a value of 0 -- which makes the index score 0
    index_score = (prescore * 100) * p0
    return index_score


def main():
    #t0 = time.clock()
    index_score = getIndex(p0, p1, p2, p3, p4, p5, p6)
    outPath = 'C:/Workspace/IndexTest/PythonOut'
    # Creates a copy of the raster created from getIndex -- this should be the only output file. Changes some characteristics of the raster, like pixel_type
    arcpy.CopyRaster_management(index_score, outPath + '/indexcompositeWeb.tif', pixel_type='8_BIT_SIGNED',
                                nodata_value='-128')
    print('The restoration index has been placed in ' + outPath + '.')
    #print time.clock() - t0


main()
