'''
GetHex.py
Ian McNair
Last updated: 10.28.2015
This function seeks to export an index (or indices later on) based on user input. 
'''

import arcpy
arcpy.env.workspace = 'C:/Workspace/DikeLocator'
arcpy.env.overwriteOutput = True

#hexnumber = raw_input('Which index hexagon would you like to select by? ')

#Creates individual index hexagon based on selection

InputFile = arcpy.GetParameterAsText(0)
OutputFile = arcpy.SetParameterAsText(0)

def getHex (hexnumber):
    inFeatures = InputFile
    outLocation = OutputFile
    outName = 'hex' + str(hexnumber)
    where = ''' "ID" = ''' + str(hexnumber)
    arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outName, where)
    

InputFile = arcpy.GetParameterAsText(0)
OutputFile = arcpy.SetParameterAsText(0)

 
getHex(hexnumber)

