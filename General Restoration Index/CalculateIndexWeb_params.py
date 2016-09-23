"""
CalculateIndexWeb.py
Ian McNair
Last Edit: 9/20/2016
Seeks to define a function that performs the restoration index calculation on a
given area given a set of 7 rasters (parameter 0 through parameter 6) and weight associated with each.
"""
#test weight order: wlera '10;5;7.5;2.5;7.5;2.5'

import arcpy

#inputRootPath = 'C:/Workspace/IndexTest/Data/WLERA_Raster_Data/'
inputRootPath = 'D:/Projects/Scripts/GLCWRA/GLCWRAIndexCalculatorPy'
#outPath = 'C:/Workspace/IndexTest/PythonOut'
outPath = 'D:/Projects/Scripts/GLCWRA/GLCWRAIndexCalculatorPy/IndexCalcOutput'

# Check out the spatial analysis extension
arcpy.CheckOutExtension('Spatial')

# Allows the script to overrite files if necessary
arcpy.env.overwriteOutput = True
# Sets the cell size for the environment
arcpy.env.cellSize = 10

#Capture the study area as a string
studyArea = arcpy.GetParameterAsText(0)

#Checks to see whether studyArea is one of the predefined variables. Prints an error out if it is not.
# Setting p0 should fail if studyArea is not an appropriate value.
if studyArea == 'wlera':
    base_path = inputRootPath + '/WLERA_Raster_Data/WLERA_'

elif studyArea == 'crsra':
    base_path =  inputRootPath + '/CRSRA_Raster_Data/CRSRA_'

elif studyArea == 'sbra':
    base_path =  inputRootPath + '/SBRA_Raster_Data/SBRA_'

else:
    print('Error, ' + studyArea + ' is not a valid study area.')

# Establishes a base path since the parameter rasters are all in the same folder
#base_path = 'C:/Workspace/IndexTest/Data/CRSRA_Raster_Data'

# Sets the file locations for the parameters as variables
p0 = arcpy.Raster(base_path + 'P0_Mask.tif')
p1 = arcpy.Raster(base_path + 'P1_Hydroperiod.tif')
p2 = arcpy.Raster(base_path + 'P2_WetlandSoils.tif')
p3 = arcpy.Raster(base_path + 'P3_Flowlines.tif')
p4 = arcpy.Raster(base_path + 'P4_CARL.tif')
p5 = arcpy.Raster(base_path + 'P5_Impervious.tif')
p6 = arcpy.Raster(base_path + 'P6_Landuse.tif')

#capture the weights string to use as parameter
paramWeights = arcpy.GetParameterAsText(1)
print("paramWeights from GetParameterAsText:" + paramWeights)
#parse out weight values delimited with semicolon (arcgis requirement)
paramWeightList = paramWeights.split(";")
print("Weights provided: " + paramWeights)

#dictionary to store weight parameter values
weightsDict = {}
#use python 'enumerate' loop grab the weights from the parameter string
for index, w in enumerate(paramWeightList):
    #add 1 to index to start at 1 instead of 0
    weightNumber = index+1
    print("Param " + str(weightNumber) + " = " + w)
    #build the weights dictionary, converting strings to float
    weightsDict["w{0}".format(weightNumber)] = float(w)
print(weightsDict)

def getIndex(p0, p1, p2, p3, p4, p5, p6):
    #    Sets weights for each parameter.
    # w1 = 10
    # w2 = 5
    # w3 = 7.5
    # w4 = 2.5
    # w5 = 7.5
    # w6 = 2.5

    w1 = weightsDict['w1']
    w2 = weightsDict['w2']
    w3 = weightsDict['w3']
    w4 = weightsDict['w4']
    w5 = weightsDict['w5']
    w6 = weightsDict['w6']

    #Begin calculations based on Justin Saarinen's instruction
    wp1 = (p1 * w1) / 10
    wp2 = p2 * w2
    wp3 = p3 * w3
    wp4 = p4 * w4
    wp5 = (p5 * w5) / 10
    wp6 = p6 * w6

    pos = wp1 + wp2 + wp3 + wp4
    pos_max = (w1 * 10) + w2 + w3 + (w4 * 4)
    pos_term = pos / pos_max

    neg = wp5 + wp6
    neg_max = (w5 * 10) + w6
    neg_term = neg / neg_max

    prescore = pos_term - neg_term
    index_score = (prescore * 100) * p0
    return index_score


def main(studyArea):
    t0 = time.clock()
    index_score = getIndex(p0, p1, p2, p3, p4, p5, p6)
    #outPath = 'C:/Workspace/IndexTest/PythonOut'
    # Creates a copy of the raster created from getIndex -- this should be the only output file. Changes some characteristics of the raster, like pixel_type
    arcpy.CopyRaster_management(index_score, outPath + '/' + studyArea + 'Index.tif', pixel_type='8_BIT_SIGNED',
                                nodata_value='-128')
    print('The restoration index has been placed in ' + outPath + '.')
    #print('This process took apporximately ' + str(time.clock() - t0) + ' seconds to run.')
    print('This process took apporximately ' + "%.2f" % (time.clock() - t0)+ ' seconds to run.')


main(studyArea)
