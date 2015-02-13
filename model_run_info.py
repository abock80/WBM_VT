

# input arguments (input to Model input module)
# GageID = '06746095'
# Shapefile = 'G06746095.shp'
# startMonth = '1'
# startYear = '1980'
# endMonth = '12'
# endYear='1999'
# climateDataset='PRISM'

import os,datetime

def main_func(GageID, Shapefile, POR):#, climateDataset):
    startdate = POR["Start Date"].split("-")
    startMonth = startdate[1]
    startYear = startdate[0]
    enddate = POR["End Date"].split("-")
    endMonth = enddate[1]
    endYear = enddate[0]
    
    now=datetime.datetime.now()
    # create unique file name
    filename = GageID+"_"+str(now.month)+str(now.day)+str(now.year)+"_"+\
    str(now.hour)+str(now.minute)+str(now.second)+".txt"
    target = open(filename,'a')
    # the file should be stored in the Basin/Base folder
    if len(str(now.minute))==1:
        minute_str = "0"+str(now.minute)
    else:
        minute_str=str(now.minute)
    if len(str(now.second))==1:
        second_str = "0"+str(now.second)
    else:
        second_str=str(now.second)
    # write down date and time of simulation
    target.write('Date of Simulation: '+str(now.month)+'-'+str(now.day)+'-'+str(now.year)+','+str(now.hour)+':'+minute_str+':'+second_str+'\n')
    target.write('Shapefile name = '+Shapefile+"\n")
    target.write('Calibration Period for Current Conditions = '+startMonth+'/'+startYear+' to '+endMonth+'/'+endYear+'\n')
    #target.write('Climate Dataset for Current/Historic Conditions = '+climateDataset+'\n')
    target.close()
    return filename