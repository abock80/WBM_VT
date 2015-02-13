import os, numpy

def Format_monthly(climate_dict, gageid, wkdir, por):
    os.chdir(wkdir)
    
    nodays = []
    counter = 0
    outfile_days = open('NoDays.txt','w')
    
    start = por['Start Date']
    sy = int(start[0:4])
    end = por['End Date']
    ey = int(end[0:4])
    from calendar import monthrange
    for i in range(sy,ey+1): # range accounting = last item +1
        for j in range(1,13):
            nodays.append(str(monthrange(i,j)[1]))
            if i == 2100 and j == 1:
                outfile_days.writelines(nodays[counter]+'\n')
                outfile_days.close()
            else:
                outfile_days.writelines(nodays[counter]+'\n')
            counter += 1
    outfile_days.close()
    
    varlist = climate_dict[0]['Vars']
    years_list = []
    
    WBM_Files = []
    
    for var in varlist:
        inputfile = open(var+'.csv', 'r')
        filelines = inputfile.readlines()
        matrix_row = 0
        if var in varlist[0]:
            PORfile = open('POR.txt', 'w')
        matrix = numpy.zeros(shape = (len(filelines[3:]), 3))
        
        #do we want to write to header or not??
        head = 'Dataset = ' + climate_dict[0]['name'] + \
                '\nVariable = ' + var + \
                '\nWsName = ' + gageid + '\n'
        
        for line in filelines[3:]:
            splitline = line.split(',')
            timestamp = splitline[0].split('T')
            yrmoday = timestamp[0].split('-')
            year = yrmoday[0]
            month = yrmoday[1]
            newline = year +' ' + month
            #print newline
            
            current_var_float = float(splitline[1])
            if var == 'Prcp' or var == 'pr':
                current_var_float *= float(nodays[matrix_row])
                newline += ' ' + str(current_var_float)
                newline_float = map(float, newline.split())
                matrix[matrix_row,...] = newline_float
                PORfile.writelines(str(year) + '-' + str(month) + '-01\n')
                if int(year) not in years_list:
                    years_list.append(int(year))   
            elif var == 'Tavg' or var == 'tas':
                newline += ' ' + str(current_var_float)
                newline_float = map(float, newline.split())
                matrix[matrix_row,...] = newline_float
            else:
                print 'You shouldn\'t enter this else statement\n'
            
            if matrix_row == 0:
                start_date = str(month) + '-' + str(year)
                head += '\n' + start_date + ' - '
            matrix_row += 1
        end_date = str(month) + '-' + str(year)
        end_year = int(year)
        head += end_date + '\n######'
        
        if var == 'Prcp' or var == 'var':
            numpy.savetxt('PPT_month.txt', matrix, '%1.5f')#, ' ', header = head
        elif var == 'Tavg' or var == 'tas':
            numpy.savetxt('TAVE_month.txt', matrix, '%1.5f')
        else:
            print 'Unable to save matrix to file'
            
        inputfile.close()
        print var + '.txt is finished formatting'
        PORFile = 'POR.txt'
        PORfile.close()
        
        WBM_Files.append(var+'_month.txt')

    return WBM_Files