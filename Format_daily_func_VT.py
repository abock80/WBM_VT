import os, time, numpy
from calendar import monthrange

# Call function
# three arguments
#   1-numpy module
#   2-Tile
#   3-climate datasset
#   4 - number of hrus

# how to improve the speed
    # 1 - create numpy matrix (# of rows = # of days,
            # of cols = # hrus +3,column[0] = year, column[1]=month, column[2]=day
    # 2 - convert/calculate each row, add to matrix (in a loop)
    # 3 - write out textfile with numpy.writetxt (allows control for formatting i.e.
    #       decimal places, headers, etc.
    # 4 - numpy.savetxt(thisdir+'\gage_params_raw.txt', hru_final, fmt='%1.5f', delimiter='  ')
    #   0 - name/location of file you are writing, 1 - name of numpy matrix, 2 - format, 3 - delimiter
# extra - read data from text right into numpy matrix
    # data2 = numpy.genfromtxt(inputfile, dtype=None,delimiter=",",skip_header=3,usecols = range(1,2000))

global WBM_Files, PORFile
WBM_Files = []

# def add_row_temp(var, current_var_float, newline):
#     # var_units = [x*0.0393 for x in current_var_float]
#     newline += ' ' + str(current_var_float)
#     newline_float = map(float, newline.split())
#     return newline_float
#
# def add_row_pr(var, current_var_float, newline):
#     # var_units = [x*0.0393 for x in current_var_float]
#     newline += ' ' + str(current_var_float)
#     newline_float = map(float, newline.split())
#     return newline_float

#def Format_daily(region, tile, dataset, nhru, WFS_URL, curdir):  # , csvs, data, thisdir):
def Format_daily(climate_dict, gageid, wk_dir):

    os.chdir(wk_dir)

    #assign variables based on climate dataset
    if climate_dict['name'] == 'DAYMET':
        varlist = ['prcp', 'tmax', 'tmin']
    elif climate_dict['name'] == 'Gridded Observed Data(1949-2010)':
        varlist = ['pr', 'tas']

    years_list = []

    #format each variable's csv file
    for var in varlist:
        inputfile = open(var+'.csv', 'r')
        filelines = inputfile.readlines()
        matrix_row = 0
        #write POR file if precipitations
        if var in varlist[0]:
            PORfile = open('POR.txt', 'w')

        # len(filelines[3:]) is number of rows and nhru is number of columns
        matrix = numpy.zeros(shape = (len(filelines[3:]), 4))

        # do we want to write header or not??
        head = 'Dataset = ' + climate_dict['name']  + \
        '\nVariable = ' + var + \
        '\nWsName = ' + gageid + '\n'


        for line in filelines[3:]:

            splitline = line.split(',')
            #print (splitline)
            timestamp = splitline[0].split('T')
            yrmoday = timestamp[0].split('-')
            year = yrmoday[0]
            month = yrmoday[1]
            day = yrmoday[2]
            newline = year + ' ' + month + ' ' + day
            current_var_float = float(splitline[1])

            if var == 'pr' or var == 'prcp' or var == 'Prcp':
                newline += ' ' + str(current_var_float)
                newline_float = map(float, newline.split())
                matrix[matrix_row, ...] = newline_float
                PORfile.writelines(str(year) + '-' + str(month) + '-' + str(day) + '\n')


            elif var == 'tas' or var == 'tmax' or var == 'tmin' or var == 'Tavg':
                newline += ' ' + str(current_var_float)
                newline_float = map(float, newline.split())
                matrix[matrix_row, ...] = newline_float
            else:
                print "You shouldn't enter this else statement"


            if matrix_row == 0:
                start_year = int(year)
                start_date = year + '-' + month + '-' + day
                head += '\n# daily ' + start_date + ' - '

            matrix_row += 1
            if int(year) not in years_list:
                years_list.append(int(year))

            end_year = int(year)
            end_date = year + '-' + month + '-' + day


            head += end_date + '\n######'
            #save daily formatted csv file
            if var == 'pr' or var == 'prcp' or var == 'Prcp':
                numpy.savetxt(var + '_daily.txt', matrix, '%1.5f')#, ' ', header=head)
                WBM_Files.append(var + '_daily.txt')
            elif var == 'tmax':
                tmax = matrix
                numpy.savetxt(var + '_daily.txt', matrix, '%1.5f')#, ' ', header=head)
                WBM_Files.append(var + '_daily.txt')
            elif var == 'tmin':
                tmin = matrix
                numpy.savetxt(var + '_daily.txt', matrix, '%1.5f')#, ' ', header=head)
                WBM_Files.append(var + '_daily.txt')
            elif var == 'tas' or var == 'Tavg':
                numpy.savetxt(var + '_daily.txt', matrix, '%1.5f')#, ' ', header=head)
                WBM_Files.append(var + '_daily.txt')

            WBM_Files.append(var + '_daily.txt')

        inputfile.close()
        print var + '_daily.txt is finished formatting'
        PORfile.close()

    #if a temperature average variable wasn't formatted from csv files, create one
    if 'Tavg' not in varlist and 'tas' not in varlist:
        tave = numpy.add(tmin, tmax) / 2

        numpy.savetxt('tave_daily.txt', tave, '%1.5f')
        WBM_Files.append('tave_daily.txt')
        varlist.append('tave')
        print 'tave_daily.txt is finished formatting'



    #write file that has number of days in each month
    nodays = []
    counter = 0
    outfile_days = open('NoDays.txt','w')
    for i in range(start_year, end_year+1):
        for j in range(1,13):
            nodays.append(str(monthrange(i,j)[1]))
            if i == 2100 and j == 1:
                outfile_days.writelines(nodays[counter]+'\n')
                outfile_days.close()
            else:
                outfile_days.writelines(nodays[counter]+'\n')
            counter += 1
    outfile_days.close()

    #convert daily formatted files to daily
    dailyToMonth(varlist, climate_dict['name'])

def dailyToMonth(varlist, dataset):

    porfile = open('POR.txt', 'r')
    por_lines = porfile.readlines()

    split = por_lines[0].split('-')



    start_year = int(split[0])
    for porLine in por_lines:
        split = porLine.split('-')

    end_year = int(split[0])


    years_list = []
    for i in range(start_year, end_year+1):
        years_list.append(i)

    daysfile = open("Nodays.txt", 'r')
    nodays = []
    for line in daysfile:
        nodays.append(int(line))

    #convert each variable from daily to monthly
    for matrix in varlist:
        filename = open(matrix + '_daily.txt', 'r')
        filelines = filename.readlines()
        #count is the counter that recognizes the index in nodays
        count = 0

        sum_matrix = numpy.zeros(shape = (len(nodays), 3))
        sums = 0
        matrix_row = 0
        for line in filelines:

            days = nodays[count]
            splitline = line.split(' ')
            year = str(splitline[0])
            month = str(splitline[1])
            day = int(float((splitline[2])))
            val = float(splitline[3])

            if matrix in ['pr', 'prcp', 'Prcp']:
                #add the value to itself for each month, so it sums up the precipitation
                if day < days:
                    sums += val
                elif day == days:
                    newline = year + ' ' + month + ' ' + str(sums)
                    newline_float = map(float, newline.split())
                    sum_matrix[matrix_row, ...] = newline_float
                    matrix_row += 1
                    sums = 0
                    count += 1
            elif matrix in ['tas', 'tavg', 'tmin', 'tmax', 'tave']:
                #add the value to itself for each month and divide by number of days, so it averages the temperature
                if day < days:
                    sums += val
                elif day == days:
                    sums += val
                    sums /= days
                    newline = year + ' ' + month + ' ' + str(sums)
                    newline_float = map(float, newline.split())
                    sum_matrix[matrix_row, ...] = newline_float
                    matrix_row += 1
                    sums = 0
                    count += 1

        count = 0
        if matrix in ['pr', 'prcp', 'Prcp']:
            numpy.savetxt('PPT_month.txt', sum_matrix, '%1.5f')
        elif matrix in ['tas', 'tavg', 'tave']:
            numpy.savetxt('TAVE_month.txt', sum_matrix, '%1.5f')
        elif matrix in ['tmin', 'tmax']:
            numpy.savetxt(matrix+'_month.txt', sum_matrix, '%1.5f')

