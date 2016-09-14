'''
DikeLocatorIterator.py
Ian McNair
Last updated: 5.26.2016
This program seeks to iterate through a list of rasters and run the dike locator
tool on each of them.
'''

import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')
arcpy.env.overwriteOutput = True


#Grabs parameters
Slope_Threshold = raw_input("Input desired slope threshold or hit enter for default (12): " + "\n")
if Slope_Threshold == '#' or not Slope_Threshold:
    Slope_Threshold = "12" # provide a default value if unspecified

Buffer_Distance = raw_input("Input desired buffer distance or hit enter for default (5): " + "\n")
if Buffer_Distance == '#' or not Buffer_Distance:
    Buffer_Distance = "5" # provide a default value if unspecified

Tolerance = raw_input("Input desired tolerance or hit enter for default (0.5): " + "\n")
if Tolerance == '#' or not Tolerance:
    Tolerance = "0.5" # provide a default value if unspecified

Fragment_Area_Threshold__m_2_ = raw_input("Input desired fragment area threshold or hit enter for default (Area >= 500): " + "\n")
if Fragment_Area_Threshold__m_2_ == '#' or not Fragment_Area_Threshold__m_2_:
    Fragment_Area_Threshold__m_2_ = "Area >= 500" # provide a default value if unspecified

Raster_Location = raw_input("Input the path name for where the rasters are, for example (exactly like this):" + "\n" + "\n" "'C:\Workspace\DikeLocator\Data\Test.gdb'" + "\n" + "\n" + "Or hit enter for the default ('C:\Workspace\DikeLocator\Data\RasterClip.gdb'):" + "\n")
if Raster_Location == "#" or not Raster_Location:
    Raster_Location = r"C:\Workspace\DikeLocator\Data\RasterClip.gdb" # provide a default value if unspecified
#else:
    #Raster_Location = "r" + Raster_Location

Output_Location = raw_input("Please input desired output location or hit enter for default ('C:\Workspace\Dikelocator\Data\DikeLocationsTest.gdb') :" + "\n")
if Output_Location == "#" or not Output_Location:
    Output_Location = r"C:\Workspace\Dikelocator\Data\DikeLocationsTest.gdb"

                            
#Gets a list of rasters in folder
arcpy.env.workspace = Raster_Location
rasterList = arcpy.ListRasters()

failed_rasters = []


#Loops through the list of rasters and applies the DikeLocator tool to each one.
for raster in rasterList:

    try:    
        fname = Output_Location + "\DL" + str(raster[3:])
        print "Processing raster " + str(raster[3:]) + "\n"
              
        #Process: Slope
        print "Calculating Slope" + "\n"
        modslope = Slope(raster,"DEGREE", "1")
        modslope.save(r"C:\Workspace\Dikelocator\Data\scratch.gdb\modslope")

        #Process: Map Algebra
        print "Performing Map Algebra" + "\n"
        rastercalc = Con(modslope, 1, 0, "Value > " + str(Slope_Threshold))
        #rastercalc.save(r"C:\Workspace\Dikelocator\Data\scratch.gdb\rastercalc")

        #Process: Extract Attributes
        print "Extracting by Attributes" + "\n" 
        rastercalc2 = ExtractByAttributes(rastercalc, "Value = 1")
        rastercalc2.save(r"C:\Workspace\Dikelocator\Data\scratch.gdb\rastercalc")
        #rastercalc2 = r"C:\Workspace\Dikelocator\Data\scratch.gdb\rastercalc"

        # Process: Raster to Polygon
        print "Converting from raster to polygon" + "\n" 
        modelpoly = r"C:\Workspace\Dikelocator\Data\scratch.gdb\modelpoly"
        arcpy.RasterToPolygon_conversion(rastercalc2, modelpoly, "SIMPLIFY")
        
        # Process: Buffer
        print "Buffering" + "\n"
        path = r"C:\Workspace\Dikelocator\Data\scratch.gdb\modelpoly_buf" + "\n" 
        modelpoly_buf = arcpy.Buffer_analysis(modelpoly, path, Buffer_Distance, "FULL", "ROUND", "NONE", "", "PLANAR")

        # Process: Generalize
        print "Generalizing" + "\n" 
        arcpy.Generalize_edit(modelpoly_buf, "0.5")

        # Process: Multipart to Singlepart
        print "Performing Multipart to singlepart" + "\n" 
        modelsinglepart = r"C:\Workspace\Dikelocator\Data\scratch.gdb\modelsinglepart"
        arcpy.MultipartToSinglepart_management(modelpoly_buf, modelsinglepart)

        #Process: Add Field
        print "Adding field: Area" + "\n" 
        arcpy.AddField_management(modelsinglepart, "Area", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        
        #Process: Calculate Field
        print "Calculating field: Area" + "\n" 
        arcpy.CalculateField_management(modelsinglepart, "Area", "!shape.area@SQUAREMETERS!", "PYTHON", "")

        #Process: Select
        print "Selecting Area >= 500" + "\n" 
        DL = r"C:\Workspace\Dikelocator\Data\DikeLocationsTest.gdb\DL" + str(raster[3:])
        arcpy.Select_analysis(modelsinglepart, DL, "Area >= 500")

        #Process: Add Field
        print "Adding field: Dike_ID" + "\n" 
        arcpy.AddField_management(DL, "Dike_ID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

        #Process: Calculate Field
        print "Calculating field: Dike_ID" + "\n" 
        arcpy.CalculateField_management(DL, "Dike_ID", "[OBJECTID] + 1", "VB", "")
        
        #Process: Zonal Statistics as Table
        print "Generating Zonal Statistics" + "\n" 
        zonalresults4 = r"C:\Workspace\Dikelocator\Data\scratch.gdb\zonalresults4"
        ZonalStatisticsAsTable(DL, "Dike_ID", raster, zonalresults4, "DATA", "MEAN")

        #Process: Join Field
        print "Adding Area and Mean to Dike Locations" + "\n" 
        arcpy.JoinField_management(DL, "Dike_ID", zonalresults4, "Dike_ID", "Dike_ID;Area;Mean")

        #Process: Add Field
        print "Adding field: Aprx_Volum" + "\n" 
        arcpy.AddField_management(DL, "Aprx_Volum", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
       
        #Process: Calculate Field
        print "Calculating field: Aprx_Volum" + "\n" 
        arcpy.CalculateField_management(DL, "Aprx_Volum", "[Area] * [Mean]", "VB", "")
        
        #Process: Delete Field 
        print "Deleting uneccessary fields" + "\n" 
        arcpy.DeleteField_management(DL, "ID;BUFF_DIST:ORIG_FID:Dike_ID")


        
        
    except:
        print "An error has occurred with raster " + str(raster[3:]) + ". Moving on." + "\n" 
        failed_rasters.append(raster)

print "Process complete. Please investigate the following rasters, as they were unable to be processed: " + ', '.join(failed_rasters)    
