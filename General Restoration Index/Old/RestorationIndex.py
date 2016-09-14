'''
RestorationIndex.py
Ian McNair
Last updated: 10.28.2015
This program seeks to isolate a study area by hexagon and then calculate the
CWA Restoration Index using the 7 parameters as input. Intended to be used in
conjunction with some other scripts to end up with and output of a Normalized
CWA Restoration Index for all of the hexagons in the study area. 
'''

import arcpy
arcpy.env.workspace = 'C:/Users/ian.mcnair12/Desktop/WLER Local Workspace/data'
arcpy.env.overwriteOutput = True


#Gets a list of the rasters in folder 
rasterList = arcpy.ListRasters()
print rasterList


#Loops through list of rasters and clips the paramaters (as designated by the 'p'
#by an index hexagon

hexnumber = '7'

for raster in rasterList:
    if raster[0] == 'p': #clips only the rasters that are paramters
        outputPath = 'C:/Users/ian.mcnair12/Desktop/WLER Local Workspace/data/Python Output/' + str(raster[0:2]) # creates output path name based on parameter name
        clipby = 'C:/Users/ian.mcnair12/Desktop/WLER Local Workspace/data/Python Output/' + 'hex' + str(hexnumber) + '.shp'
        arcpy.Clip_management(in_raster = raster, rectangle = '#', out_raster = outputPath + '.tif', in_template_dataset = clipby, clipping_geometry = 'True') 

