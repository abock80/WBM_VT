

WBM_Files = []

def add_row_temp(var, current_var_float, newline):
    str1 = ' '.join(str(x) for x in current_var_float)
    newline += ' '+ str1
    newline_float = map(float, newline.split())
    return newline_float

def add_row_pr(var, current_var_float, newline):
    str1 = ' '.join(str(x) for x in current_var_float)
    newline += ' '+ str1
    newline_float = map(float, newline.split())
    return newline_float

def Format_monthly(climate_dict,gageid,wk_dir):
    import os,numpy
    os.chdir(wk_dir)


    if climate_dict['name'] == 'PRISM':
        varlist=climate_dict['Vars']
    years_list = []
    months_list = [1, 2, 3, 4, 5, 6, 7, 8 , 9, 10, 11, 12]

    # format each CSV to WBM
    for var in varlist:
        inputfile = open(var+'.csv', 'r')
        print var
        filelines = inputfile.readlines()
        matrix_row = 0
        if var in varlist[0]:
            PORfile = open('POR.txt','w')
        matrix = numpy.zeros(shape = (len(filelines[3:]),3))

        # do we want to write header or not??
        head = 'Dataset = ' + climate_dict['name']  + \
        '\nVariable = ' + var + \
        '\nWsName = ' + gageid + '\n'

        for line in filelines[3:]:

            splitline = line.split(',')
            timestamp = splitline[0].split('T')
            yrmoday = timestamp[0].split('-')
            year = yrmoday[0]
            month = yrmoday[1]
            #print yrmoday
            newline = year + ' ' + month
            #print 'Year: ' + year + ' Month: ' + month
            print (splitline)
            current_var_float = float(splitline[1])

            if var == 'ppt' or var == 'RT' or var == 'pr' or var == 'Prcp':
                newline += ' ' + str(current_var_float)
                newline_float = map(float, newline.split())
                matrix[matrix_row,...] = newline_float
                PORfile.writelines(str(year)+'-'+str(month)+'-01 \n')
                if int(year) not in years_list:
                    years_list.append(int(year))
            elif var == 'tmin' or var == 'tmax' or var == 'tmn' or var == 'tmx' or var == 'TA' or var == 'tasmin' or var == 'tasmax' or var == 'Tavg':
                newline += ' ' + str(current_var_float)
                newline_float = map(float, newline.split())
                matrix[matrix_row,...] = newline_float
            else:
                print "You shouldn't enter this else statement"

            if matrix_row == 0:
                start_date = str(month) + '-' + str(year)
                head += '\n ' + start_date + ' - '
            matrix_row += 1
        end_date = str(month) + '-' + str(year)
        head += end_date + '\n######'

        if var == 'ppt' or var == 'RT' or var == 'pr' or var =='Prcp':
            numpy.savetxt('PPT_month.txt', matrix, '%1.5f')#, ' ', header = head)
        elif var == 'tmin' or var == 'tmn' or var == 'tasmin':
            tmin = matrix
            numpy.savetxt(var+'_month.txt', matrix, '%1.5f')#, ' ', header = head)

        elif var == 'tmax' or var == 'tmx' or var == 'tasmax':
            tmax = matrix
            numpy.savetxt(var+'_month.txt', matrix, '%1.5f')#, ' ', header = head)

        elif var == 'TA' or var == 'Tavg':
            numpy.savetxt('TAVE_month.txt', matrix, '%1.5f')#, ' ', header = head)

        WBM_Files.append(var+'_month.txt')

        inputfile.close()
        print var+'.txt is finished formatting'
        PORFile = 'POR.txt'
        PORfile.close()

    # remove header lines if we don't want to write header
    if 'TA' not in varlist and 'Tavg' not in varlist:
        tave = numpy.add(tmin, tmax)/2
        head = 'Dataset = ' + climate_dict['name'] + \
        '\nVariable = tave' \
        '\nWsName = ' + gageid + \
        '\n ' + start_date + ' - ' + end_date + \
        '\n######'
        numpy.savetxt('TAVE_month.txt', tave, '%1.5f')#, ' ', header = head)
        WBM_Files.append('TAVE_month.txt')
        print "TAVE.txt is finished formatting"

    # returns WBM files (PPT_month, TAVE_month) I kept this as a list
    return WBM_Files


# climate_dataset = {'url': 'http://cida.usgs.gov/thredds/dodsC/prism', 'timestep': 'Monthly', 'name': 'PRISM', 'Vars': ['ppt', 'tmx', 'tmn']}
# gageid = '06746095'
# wkdir = r'C:\Users\reimandy\Documents\temp'
# Format_monthly(climate_dataset, gageid, wkdir)