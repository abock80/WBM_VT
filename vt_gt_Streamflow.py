'''

plotting a matplotlib hydrograph from a nwis data call
Created on Mar 6, 2014

@author: talbertc,abock
'''
import urllib, numpy, os, datetime, ctypes, sys
from datetime import datetime, date, timedelta, time
# need urllib to get streamflow data from NWIS (website parsing module)
import matplotlib.pyplot as plt

def plot_hydrograph(gageid, start_date, end_date, area):
    dates, flows = get_nwis_data(gageid, start_date, end_date, area)

    font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }

    plt.plot([datetime.strptime(d, "%Y-%m-%d") for d in dates], flows, 'k')
    plt.title('Flow at: ' + str(gageid), fontdict=font)
    plt.xlabel('date', fontdict=font)
    plt.ylabel('flow (cm/s)', fontdict=font)

    #  Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    plt.show()
    #pdf = os.path.join(os.getcwd(), gageid+".pdf")
    #plt.savefig(pdf,format='PDF')
    png = os.path.join(os.getcwd(), gageid+".png")
    plt.savefig(png,format='PNG')

# determines number of days between two dates
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

def date_to_urldate(indate):
    '''converts a py date to a string representation needed by
    the nwis site
    '''
    return "-".join([str(indate.year), str(indate.month), str(indate.day)])

def get_nwis_data(gageid, start_date, end_date, areakm2):
    '''
    '''
    years = []
    months = []
    days = []
    end_date_next=end_date
    end_date_next += timedelta(days=1)
    for result in perdelta(start_date, end_date_next, timedelta(days=1)):
        dt = datetime.strptime(str(result), "%Y-%m-%d")
        t = dt.timetuple()
        years.append(t[0])
        months.append(t[1])
        days.append(t[2])

    #  make empty matrix for holding flows

    delta = start_date - end_date_next
    flows = numpy.zeros(shape=(abs(delta.days), 4))
    #flows.fill(NaN)  #  make NaN for all
    flows[:]=numpy.nan
    flows[..., 0] = years
    flows[..., 1] = months
    flows[..., 2] = days

    print "Going to the NWIS web services for each gage."
    # these are codes that explain where there streamgage data did not meet
    # the QA/QC check
    noDataList=['Ice','Eqp','Bkw','Rat','Dis','Ssn','Mnt','***']

    # get streamgage name, can get other station properties this way too.
    gagepage = urllib.urlopen('http://waterdata.usgs.gov/nwis/inventory?search_site_no='+gageid+'&search_site_no_match_type=exact&group_key=NONE&format=sitefile_output&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&list_of_search_criteria=search_site_no')
    for line in gagepage:
        if len(line)>1:
            if line[3:13]=='station_nm':
                line = line.replace(' <station_nm>','')
                line = line.replace('</station_nm>\n','')
                if line !=' ':
                    Sta_name=line

    # codes 0.00_ZFl, Zfl - zero flow
    usock = urllib.urlopen('http://waterdata.usgs.gov/nwis/dv?referred_module=sw&search_site_no='+gageid+'&search_site_no_match_type=exact&site_tp_cd=ST&index_pmcode_30208=1&index_pmcode_00060=1&index_pmcode_99060=1&sort_key=site_no&group_key=NONE&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=date_range&begin_date='+str(start_date)+'&end_date='+str(end_date)+'&format=rdb&date_format=YYYY-MM-DD&rdb_compression=value&list_of_search_criteria=search_site_no%2Csite_tp_cd%2Crealtime_parameter_selection')
    dateList=[]
    flowList=[]
    count=0
    for line in usock:
        if line !='\n':
            items = line.split()
        if items[0]=='USGS':
            dateList.append(items[2])
            if len(items)<4:
                flowList.append(-999)
            else:
                if items[3]=='0.00_ZFl':
                    flowList.append(0)
                if items[3]=='ZFl':
                    print 'ZFl'
                    flowList.append(0)
                elif items[3] in noDataList:
                    flowList.append(-999)
                else:
                    flowList.append(items[3])
    # this may throw an exception if there is a QAQC code (aka line 146) that has slipped through
    if len(flowList)==0:
        msg=ctypes.windll.user32.MessageBoxA(None,"No measured streamflow for period of record entered.  Try again with a different period of record ?",\
        "WARNING",4,uType="MB_SETFOREGROUND")

        if msg==6:
            msg=ctypes.windll.user32.MessageBoxA(None,"Please enter new start and/or end dates for period of record for "+gageid," ",0,uType="MB_SETFOREGROUND | MB_ICONINFORMATION | MB_OK")
            sys.exit("Please Enter new start and/or end dates for period of record for "+gageid )
        else:
            print "measured daily streamflow from NWIS retrieved"

    flowList_float=[float(x) for x in flowList]
    flowListnp=numpy.array(flowList_float)
    flowListnp[flowListnp==-999]=numpy.nan
    numDays=numpy.count_nonzero(~numpy.isnan(flowListnp))

    if numDays < 1825:
        msg=ctypes.windll.user32.MessageBoxA(None,"Less than 5 years of streamflow data retrieved.  At least 5 years of data recommended for streamflow calibration.  Try again with a different period of record ?",\
        "WARNING",4,uType="MB_SETFOREGROUND")
    else:
        msg=ctypes.windll.user32.MessageBoxA(None,str(int(numDays/365))+" years of streamflow data retrieved"," ",0,uType="MB_SETFOREGROUND | MB_ICONINFORMATION | MB_OK")

    if msg==6:
        msg=ctypes.windll.user32.MessageBoxA(None,"Please enter new start and/or end dates for period of record for "+gageid," ",0,uType="MB_SETFOREGROUND | MB_ICONINFORMATION | MB_OK")
        sys.exit("Please Enter new start and/or end dates for period of record for "+gageid )

    # this piece of code places the streamflow data into the matrix
    # this is important because the streamflow data may begin/end inside matrix
    if len(dateList)>0:
        first_day=dateList[0].split('-')
        date_integer=[int(x) for x in first_day]
        date_format = date(date_integer[0],date_integer[1],date_integer[2])
        delta = start_date - date_format
        #print delta.days
        if delta.days!=0:
            placer = abs(delta.days)
        elif delta.days==0:
            placer=0
        len(flowList_float)
        print placer
        flows[placer:len(flowList_float)+placer,3]=flowList_float
    else:
        #i is not defined.
        flows[...,i]=-999
    flows[flows==-999.0]=numpy.nan
    # save to daily textfile
    numpy.savetxt(os.getcwd()+r'/Flows_daily.txt', flows, '%s', ' ')

    #convert from daily cfs to monthly (mm)
    streamflowfile= open(os.getcwd()+r'/Flows_monthly.txt','w')
    for i in range(min(years),max(years)+1):
        for j in range(1,13):
            month=flows[(flows[:,0]==i)&(flows[:,1]==j)]
            #mask nan values from monthly mean calculation
            if month.size !=0:
                mask_month = numpy.ma.masked_array(month[:,3],numpy.isnan(month[:,3]))
                # converts CFS to Cubic centimeters per second
                if (numpy.ma.max(mask_month)is numpy.ma.masked)==False:
                    month_mean=numpy.mean(mask_month)
                    month_mean_cms=(month_mean*.0283168466)
                    month_mean_cms=round(month_mean_cms,6)
            else:
                month_mean_cms='NA'
            newline = str(i) +' '+str(j)+' '+str(month_mean_cms)+'\n'
            streamflowfile.writelines(newline)
    streamflowfile.close()
    return dateList, flowListnp

def main_func(gageid, d0, d1, area):
    plot_hydrograph(gageid, d0, d1,area)

