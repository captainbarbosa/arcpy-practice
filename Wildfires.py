# Author: Nadia Barbosa
# Purpose: Used to create an ArcPy tool in which
# attributes are read from a text file and
# then added to a feature class for spatial representation
# of wildfires.


import arcpy
import sys
import os


cur = None

try:
    #the output feature class name
    outputFC = arcpy.GetParameterAsText(0)

    #the template feature class that defines the attribute schema
    fcTemplate = arcpy.GetParameterAsText(1)

    #the wildfire data to read
    file_name = arcpy.GetParameterAsText(2)
    f = open(file_name, 'r')

    #Get the path of the output feature class name
    outputPath = os.path.split(outputFC)[0]

    #Get the file name of the output feature class name
    outputFile = os.path.split(outputFC)[1]

    #Create the new feature class
    arcpy.CreateFeatureclass_management(outputPath, outputFile, "point", fcTemplate)

    #Open an insurt cursor for the feature class
    cur = arcpy.da.InsertCursor(outputFC, ["SHAPE@", "CONFIDENCEVALUE"])

    cntr = 0

    for fire in f:
        
        if 'Latitude' in fire:
            continue
        
        listValues = fire.split(",")
        latitude = float(listValues[0])
        longitude = float(listValues[1])
        confid = float(listValues[2])

        pnt = arcpy.CreateObject("Point")
        pnt.X = longitude
        pnt.Y = latitude
        print pnt.X, pnt.Y

        cur.insertRow([pnt, confid])

        cntr +=1

        print "Record number " + str(cntr) + " written to feature class"

    print "Total: "+str(cntr)+" points inserted"
        

except Exception, e:
    print e
    print arcpy.GetMessages()

finally:
    if cur:
        del cur


        
    
