def dataset_prop(climate_dataset):
        '''Get properties, URL, and variables of each climate dataset'''
        if climate_dataset == 'PRISM':
            ds_dict = {'name':'PRISM', 'url':'http://cida.usgs.gov/thredds/dodsC/prism', 'timestep':'Monthly','Vars':['ppt','tmx','tmn']}
        elif climate_dataset == 'DAYMET':
            #ds_dict = {'name':'DAYMET', 'url':'dods://cida-eros-mows1.er.usgs.gov:8080/thredds/dodsC/daymet', 'timestep':'Daily', 'Vars':['prcp','tmax','tmin']}
            ds_dict = {'name':'DAYMET', 'url':'http://thredds.daac.ornl.gov/thredds/dodsC/daymet-agg/daymet-agg.ncml', 'timestep':'Daily', 'Vars':['prcp','tmax','tmin']}
        elif climate_dataset == 'Gridded Observed Data' or climate_dataset == 'GSD':
            ds_dict = {'name':'Gridded Observed Data(1949-2010)', 'url':'http://cida.usgs.gov/thredds/dodsC/new_gmo', 'timestep':'Daily', 'Vars':['pr','tas']}
        return ds_dict

def get_GDP_data(shapefile,gage_id,climate_data,Period,idfield):
    '''Retrieves climate dataset from GDP and parses into individual variables'''
    myGDP = pyGDP.pyGDPwebProcessing()
    shapefiles = myGDP.getShapefiles()
    for shp in shapefiles:
        print shp

    justfname = os.path.splitext(os.path.split(shapefile)[1])[0]
    print (justfname)
    shapefile = 'upload:'+justfname
    user_attribute = idfield
    user_value = None

    dataSet = climate_data['url']
    dataType = climate_data['Vars']

    timeBegin = Period['Start Time']
    timeEnd = Period['End Time']

    gmlIDs=None
    verbose=True
    coverage = 'false'
    delim='COMMA'
    stats='MEAN'
    print(shapefile)
    print(dataSet)
    print(dataType)
    print(timeBegin)
    print(timeEnd)
    print(user_attribute)
    print (shapefile+" "+dataSet+" "+str(dataType)+" "+str(timeBegin)+" "+str(timeEnd)+" "+user_attribute)
    outputPath = myGDP.submitFeatureWeightedGridStatistics(shapefile, dataSet, dataType, timeBegin, timeEnd, user_attribute, user_value, gmlIDs, verbose, coverage, delim, stats)
    print outputPath
    shutil.copy2(outputPath, climate_data['name']+'_'+gage_id+'.csv')

    '''Beginning of parsing steps'''
    csvread = csv.reader(open(climate_data['name']+'_'+gage_id+'.csv', 'rb'))
    csvwrite = csv.writer(open(dataType[0]+'.csv', "wb"))

    index = 0

    temp = csvread
    var = temp.next()
    var[0] = '#'+dataType[0]
    temp.next()
    gage = []
    gage.append('')
    gage.append(gageid)
    csvwrite.writerow(var)
    csvwrite.writerow(gage)
    parsedFiles = []
    for variable in dataType:

        for row in csvread:

            if variable == dataType[len(dataType) - 1]:
                csvwrite.writerow(row)
            else:
                if (row[0] in '#'+dataType[index+1]) or (row[0] in '# '+dataType[index+1]):
                    var = '#'+dataType[index+1]
                    csvwrite = csv.writer(open(dataType[index+1] + '.csv', "wb"))
                    row[1:] = ""
                    row[0] = var
                    csvwrite.writerow(row)
                    #csvwrite.writerow(gage)

                    if len(dataType) == 2:
                        csvwrite.writerow(csvread.next())
                        csvwrite.writerow(csvread.next())
                    else:
                        csvread.next()
                        csvwrite.writerow(csvread.next())
                    break
                else:
                    if dataType[index+1] not in row[0] and row[0] not in dataType[index+1]:
                        csvwrite.writerow(row)

        parsedFiles.append(os.getcwd()+'\\'+variable+'.csv')
        print "Finished parsing " + variable + ".csv"
        if (index + 1) < len(dataType):
            index += 1


import sys
import owslib
import csv, owslib, os, shutil, sys, tempfile
import Format_monthly_func_VT, Format_daily_func_VT,sys
from pyGDP import pyGDP
myGDP = pyGDP.pyGDPwebProcessing()
global wkdir,os

def main_func(gage, shapefile, data, por, idfield):
    global data_set, gageid

    gageid = gage
    shpfile = shapefile
    data_set = data

    inPOR = por
    gdPOR={'Start Time':inPOR['Start Date']+'T00:00:00.000Z','End Time':inPOR['End Date']+'T00:00:00.000Z'}

    climate_dataset = dataset_prop(data_set)
##    get_GDP_data(shpfile,gageid,climate_dataset,gdPOR, idfield)
##
##    if climate_dataset['timestep'] == 'Monthly':
##        Format_monthly_func_VT.Format_monthly(climate_dataset,gageid,os.getcwd())
##    elif climate_dataset['timestep'] == 'Daily':
##        Format_daily_func_VT.Format_daily(climate_dataset, gageid, os.getcwd())

    return climate_dataset