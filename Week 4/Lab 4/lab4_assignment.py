### Lab 4 Assignment
import arcpy

arcpy.env.workspace = r'C:\\Users\aikra\Documents\GitHub\krakau-GEOG-676\codes_env'
folder_path = r'C:\\Users\aikra\Documents\GitHub\krakau-GEOG-676\Week 4\Lab 4'
gdb_name = 'Test.gdb'
gdb_path = folder_path + '\\' + gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name)

csv_path = r'C:\\Users\aikra\Documents\GitHub\krakau-GEOG-676\Week 4\garages.csv'
garage_layer_name = 'Garage_Points'
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name

# open campus gdb and copy feature to our gdb
campus = r'C:\\Users\aikra\Documents\GitHub\krakau-GEOG-676\Week 4\Campus.gdb'
buildings_campus = campus + '\Structures'
buildings = gdb_path + '\\' + 'Buildings'

arcpy.Copy_management(buildings_campus, buildings)

# reprojection
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref)

#buffer the garage
garageBuffered = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_reprojected', gdb_path +'\Garage_Points_buffered', 150)

arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Building_Intersection', 'ALL')

arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersection.dbf', 'C:\\Users\aikra\Documents\GitHub\krakau-GEOG-676', 'NearbyBuildings.csv')

