'''
GetHex.py
Ian McNair
Last updated: 10.28.2015
This function seeks to export an index (or indices later on) based on user input. 
'''

import arcpy
arcpy.env.workspace = 'C:/Users/ian.mcnair12/Desktop/WLER Local Workspace/data/CWA.gdb'
arcpy.env.overwriteOutput = True


hexnumber = raw_input('Which index hexagon would you like to select by? ')

#Creates individual index hexagon based on selection

def getHex (hexnumber):
    inFeatures = 'hexagon5kbuf40'
    outLocation = 'C:/Users/ian.mcnair12/Desktop/WLER Local Workspace/data/Python Output'
    outName = 'hex' + str(hexnumber)
    where = ''' "ID" = ''' + str(hexnumber)
    arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outName, where)
    
 
getHex(hexnumber)

