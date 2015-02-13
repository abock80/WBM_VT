def dataset_prop(climate_dataset,scenario):
        '''Get properties, URL, and variables of each climate dataset'''
        if climate_dataset=='BCSD_CMIP3':
            ds_dict={'name':'BCSD_CMIP3', 'url':'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml', 'timestep':'Monthly','Vars':['Prcp','Tavg']}
            if scenario == 'a1b':
                gcm_dict={'bccr-bcm2-0':[1],'cccma-cgcm3-1':[1,2,3,4,5],'cnrm-cm3':[1],'csiro-mk3-0':[1],'gfdl-cm2-1':[1],'inmcm3-0':[1],'ipsl-cm4':[1],
                'miroc3-2-medres':[1,2,3],'miub-echo-g':[1,2,3],'mpi-echam5':[1,2,3],'mri-cgcm2-3-2a':[1,2,3,4,5],'ncar-ccsm3-0':[1,2,3,5,6,7],'ncar-pcm1':[1,2,3],'ukmo-hadcm3':[1]}
            elif scenario == 'a2':
                gcm_dict={'ncar-pcm1':[2,3,4],'bccr-bcm2-0':[1],'cccma-cgcm3-1':[1,2,3,4],'cnrm-cm3':[1],'csiro-mk3-0':[1],'gfdl-cm2-1':[1],'inmcm3-0':[1],'ipsl-cm4':[1],
                'miroc3-2-medres':[1,2,3],'miub-echo-g':[1,2,3],'mpi-echam5':[1,2,3],'mri-cgcm2-3-2a':[1,2,3,4],'ncar-ccsm3-0':[1,2,3,4],'ukmo-hadcm3':[1]}
            elif scenario == 'b1':
                gcm_dict={'bccr-bcm2-0':[1],'cccma-cgcm3-1':[1,2,3,4,5],'cnrm-cm3':[1],'csiro-mk3-0':[1],'gfdl-cm2-1':[1],'inmcm3-0':[1],'ipsl-cm4':[1],
                'miroc3-2-medres':[1,2,3],'miub-echo-g':[1,2,3],'mpi-echam5':[1,2,3],'mri-cgcm2-3-2a':[1,2,3,4,5],'ncar-ccsm3-0':[1,2,3,4,5,6,7],'ncar-pcm1':[2,3],'ukmo-hadcm3':[1]}
        elif climate_dataset=='BCSD_CMIP5':
            ds_dict={'name':'BCSD_CMIP5', 'url':'http://cida.usgs.gov/thredds/dodsC/cmip5_bcsd/future', 'timestep':'Monthly','Vars':['pr','tas']}
            if scenario == 'rcp4.5':
                gcm_dict={'ACCESS1_0':2,'ACCESS1_3':2,'bcc_csm1_1_m':2,'bcc_csm1_1':3,'BNU_ESM':2,'CanESM2':2,'CCSM4':2,'CESM1_BGC':2,'CESM1_CAM5':2,
                'CMCC_CM':2,'CNRM_CM5':2,'CSIRO_Mk3_6_0':2,'EC_EARTH':2,'FGOALS_g2':2,'FGOALS_s2':2,'FIO_ESM':2,'GFDL_CM3':2,'GFDL_ESM2G':2,'GFDL_ESM2M':2,'GISS_E2_H_CC':2,
                'GISS_E2_R':2,'GISS_E2_R_CC':2,'HadCM3':4,'HadGEM2_AO':3,'HadGEM2_CC':5,'HadGEM2_ES':1,'inmcm4':2,'IPSL_CM5A_LR':2,'IPSL_CM5A_MR':2,'IPSL_CM5B_LR':2,
                'MIROC4h':4,'MIROC5':2,'MIROC_ESM':2,'MIROC_ESM_CHEM':2,'MPI_ESM_LR':2}
            elif scenario == 'rcp6.0':
                gcm_dict={'bcc_csm1_1':3,'CCSM4':2,'CESM1_CAM5':2,'CSIRO_Mk3_6_0':2,'FIO_ESM':2,'GFDL_CM3':2,'GFDL_ESM2G':2,'GFDL_ESM2M':2,
                'GISS_E2_R':2,'HadGEM2_AO':3,'HadGEM2_ES':1,'IPSL_CM5A_LR':2,'IPSL_CM5A_MR':2,'MIROC5':2,'MIROC_ESM':2,'MIROC_ESM_CHEM':2}
            elif scenario == 'rcp8.5':
                gcm_dict={'ACCESS1_0':2,'ACCESS1_3':2,'bcc_csm1_1_m':2,'bcc_csm1_1':3,'BNU_ESM':2,'CanESM2':2,'CCSM4':2,'CESM1_BGC':2,'CESM1_CAM5':2,
                'CMCC_CM':2,'CNRM_CM5':2,'CSIRO_Mk3_6_0':2,'EC_EARTH':2,'FGOALS_g2':2,'FGOALS_s2':2,'FIO_ESM':2,'GFDL_CM3':2,'GFDL_ESM2G':2,'GFDL_ESM2M':2,
                'GISS_E2_R':2,'HadGEM2_AO':3,'HadGEM2_CC':5,'HadGEM2_ES':1,'inmcm4':2,'IPSL_CM5A_LR':2,'IPSL_CM5A_MR':2,'IPSL_CM5B_LR':2,'MIROC5':2,
                'MIROC_ESM':2,'MIROC_ESM_CHEM':2}
        return ds_dict,gcm_dict


def get_GDP_data(shapefile,gage_id,climate_data,scen,GCM,GCMrun,Period, idfield):
    '''Retrieves climate dataset from GDP and parses into individual variables'''
    myGDP = pyGDP.pyGDPwebProcessing()
    shapefiles = myGDP.getShapefiles()
    for shp in shapefiles:
        print shp
    justfname = os.path.splitext(os.path.split(shapefile)[1])[0]
    shapefile = 'upload:'+justfname
    user_attribute = idfield
    user_value = None

    dataSet = climate_data[0]['url']

    dataType=climate_data[0]['Vars']
    dataType2=[]
    for data in dataType:
        dataType2.append('sres'+scen+'_'+GCM+'_'+str(GCMrun)+'_'+data)

    timeBegin=Period['Start Time']
    timeEnd = Period['End Time']

    gmlIDs=None
    verbose=True
    coverage = 'false'
    delim='COMMA'
    stats='MEAN'

    print(timeBegin)
    print(timeEnd)
    print (scen)
    print(GCM)
    print(GCMrun)
    print(gage_id)
    outputPath = myGDP.submitFeatureWeightedGridStatistics(shapefile, dataSet, dataType2, timeBegin, timeEnd, user_attribute, user_value, gmlIDs, verbose, coverage, delim, stats)
    print outputPath
    filename = scen+'_'+GCM+'_'+str(GCMrun)+'_'+gage_id+'.csv'
    shutil.copy2(outputPath, filename)

    '''Beginning of parsing steps'''
    csvread = csv.reader(open(filename, 'rb'))
    csvwrite = csv.writer(open(dataType[0]+'.csv', "wb"))
    index = 0

    temp = csvread
    var = temp.next()
    var[0] = '#'+dataType[0]
    gage = temp.next()

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
                    #csvwrite = csv.writer(open(GCM+'_'+str(GCMrun)+'\\'+dataType[index+1] + '.csv', "wb"))
                    csvwrite = csv.writer(open(dataType[index+1] + '.csv', "wb"))
                    row[1:] = ""
                    row[0] = var
                    csvwrite.writerow(row)
                    csvwrite.writerow(gage)

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

        #parsedFiles.append(GCM+'_'+str(GCMrun)+'\\'+variable+'.csv')
        parsedFiles.append(variable+'.csv')
        print "Finished parsing " + variable + ".csv"
        if (index + 1) < len(dataType):
            index += 1

import sys
#sys.path.append("D:\\abock\\Water_Balance\\pyGDP\\OWSLib")
#sys.path.append("D:\\abock\\Water_Balance\\pyGDP\\pyGDP-master")
import Format_monthly_func_VT_FC
import csv, os, shutil, tempfile
from pyGDP import pyGDP
myGDP = pyGDP.pyGDPwebProcessing()

def main_func(gage, shapefile, data, por, idfield, scens):
    gageid = gage
    shpfile = shapefile
    shpName = shpfile.split('.')
    GDPfiles= myGDP.getShapefiles()
    if any ('upload:'+shpName[0] in item for item in GDPfiles) is False:
        print 'need to reupload dataset here'


    scenarios=scens
    for scenario in scenarios:
        print os.getcwd()
        print (scenario)
        os.chdir(scenario)
        if scenario in ['a1b','a2','b1']:
            data_set = 'BCSD_'+data
        elif scenario in ['rcp2.6','rcp4.5','rcp6.0','rcp8.5']:
            data_set = 'BCSD_CMIP5'

        inPOR = por
        gdPOR={'Start Time':inPOR['Start Date']+'T00:00:00.000Z','End Time':inPOR['End Date']+'T00:00:00.000Z'}

        climate_dataset = dataset_prop(data_set,scenario)
        print(climate_dataset)

        for i in range(0,len(climate_dataset[1])):
            gcmNames = climate_dataset[1].keys()[i]
            gcmRuns = climate_dataset[1].values()[i]

            #set directory to gageid/FC/climate dataset/scenario/gcmname
            curdir = os.getcwd()
            dirname = os.path.join(curdir, gcmNames)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            #change directory to gcm name
            os.chdir(dirname)
            print(gcmRuns)
            print (gcmNames)
            for runs in gcmRuns:
                #Set directory to gageid/FC/gcm1/scenario/gcmname/gcmrun/INPUT
                for sub in [gcmNames+'_'+str(runs), 'OUTPUT', 'INPUT']:
                    curdir = os.getcwd()
                    dirname = os.path.join(curdir, sub)
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)

                    if sub != 'OUTPUT':
                        os.chdir(dirname)

                get_GDP_data(shpfile,gageid,climate_dataset,scenario,gcmNames,runs,gdPOR, idfield)
                curdir = os.getcwd()
                Format_monthly_func_VT_FC.Format_monthly(climate_dataset,gageid,curdir, por)
                #set directory to gageid/FC/gcm1/scenario/gcmname
                os.chdir('..')
                os.chdir('..')
            #set directory to gageid/FC/gcm1/scenario
            os.chdir('..')
        os.chdir('..')

