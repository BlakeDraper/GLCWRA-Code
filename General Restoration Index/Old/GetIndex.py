'''
GetIndex.py
Ian McNair
Last Edit: 11/3/2015
Seeks to define a function in which map algebra is performed on a given set of
rasters to calculate the restoration index
'''

import arcpy, arcinfo

arcpy.CheckOutExtension("Spatial")

arcpy.env.workspace = 'C:/Users/ian.mcnair12/Desktop/WLER Local Workspace/data/Python Output'
arcpy.env.overwriteOutput = True

base_path = 'C:/Users/ian.mcnair12/Desktop/WLER Local Workspace/data/Python Output'

p0_raster = arcpy.Raster(base_path + '/p0.tif')
p1_raster = arcpy.Raster(base_path + '/p1.tif')
p2_raster = arcpy.Raster(base_path + '/p2.tif')
p3_raster = arcpy.Raster(base_path + '/p3.tif')
p4_raster = arcpy.Raster(base_path + '/p4.tif')
p5_raster = arcpy.Raster(base_path + '/p5.tif')
p6_raster = arcpy.Raster(base_path + '/p6.tif')


def GetIndex(p0, p1, p2, p3, p4, p5, p6):
    index_raster = p0 * ((p1 + (p2 * 10) + (p3 * 2) + (p4 * 5))/(p5 +1 ) + (p6 * 7.5))
    index_raster.save(base_path + '/index.tif')

index = GetIndex(p0_raster, p1_raster, p2_raster, p3_raster, p4_raster, p5_raster, p6_raster)
