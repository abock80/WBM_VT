from core.modules.vistrails_module import Module
from core.modules.module_registry import get_module_registry

from datetime import date
import os, shutil, subprocess, ctypes,sys
if "D:\\abock\\Water_Balance\\pyGDP\\OWSLib" not in sys.path:
    sys.path.append("D:\\abock\\Water_Balance\\pyGDP\\OWSLib")
if "D:\\abock\\Water_Balance\\pyGDP\\pyGDP-master" not in sys.path:
    sys.path.append("D:\\abock\\Water_Balance\\pyGDP\\pyGDP-master")
##ha=pyGDP.pyGDPwebProcessing()
#************************
import model_run_info
import utils
import vt_gt_Streamflow
import mows_pyGDP_VT
import mows_pyGDP_VT_FC
##import uploadshapefile

class Model_Input(Module):

    _input_ports = [("GageID", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Shapefile", '(edu.utah.sci.vistrails.basic:File)'),
                    ("ID Field", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Calibration Start Date", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Calibration End Date", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Working Directory", '(edu.utah.sci.vistrails.basic:Directory)')]

    #model_info has gagid, climate, shapefile, directory, POR, basin area, latitude
    _output_ports = [("model_info", '(edu.utah.sci.vistrails.basic:Dictionary)')]


    def compute(self):

        model_info = {}
        model_info['GageID'] = self.getInputFromPort("GageID")
        model_info['ID Field'] = self.getInputFromPort("ID Field")

        #define working directory
        wkdir = os.path.join(self.getInputFromPort("Working Directory").name, 'G'+model_info['GageID'])
        model_info['Directory'] = wkdir

        from pyGDP import pyGDP
        pyGDP = pyGDP.pyGDPwebProcessing()

        newdir = os.path.join(model_info['Directory'])
        if not os.path.exists(newdir):
            os.makedirs(newdir)
        os.chdir(newdir)
        for dname in ['BASE', 'CC', 'FC']:
            full_dname = os.path.join(newdir, dname)
            if not os.path.exists(full_dname):
                os.makedirs(full_dname)

        os.chdir(model_info['Directory'])

        #get start date
        start = self.getInputFromPort("Calibration Start Date")
        start_split = start.split('-')
        sm = int(start_split[0])
        sy = int(start_split[1])
        start_date = str(date(sy, sm, 01))

        #get end date
        end = self.getInputFromPort("Calibration End Date")
        end_split = end.split('-')
        em = int(end_split[0])
        ey = int(end_split[1])
        end_date = str(date(ey, em, 28))

        #set period of record
        model_info['POR Calibration'] = {"Start Date": start_date, "End Date": end_date}

        #write file that contains date of simulation, shapefile name, por, climate dataset to BASE
        basedir = os.path.join(model_info["Directory"], "BASE")
        os.chdir(basedir)

        #set shapefile to be a part of model_info
        wkdir = os.path.join(model_info['Directory'],"BASE")
        model_info['Shapefile'] = self.getInputFromPort("Shapefile").name
        shpFile = model_info['Shapefile']
        shpSplt = shpFile.split("/")
        shpName=shpSplt[-1][0:-4]
        shpDir = '/'.join(str(x) for x in shpSplt[0:-1])

        fname = model_run_info.main_func(model_info["GageID"], model_info["Shapefile"], model_info["POR Calibration"])
        model_info['Base File'] = fname

        #add latitude to model info text file
        wkdir = os.path.join(model_info["Directory"],"BASE")
        Rscript = "C:/Users/abock/Documents/R/R-3.0.2/bin/Rscript.exe"
        XLatScript = r'D:/abock/Water_Balance/WBM_Andy/Final_Files/All_Files/Code/nonVT/XLat.R'
        subprocess.call(Rscript+" "+XLatScript+" "+wkdir+" "+shpDir+" "+shpName+" "+fname)

        #read out latitude written to model info text file
        filename = open(fname,'r')
        lines = filename.readlines()
        latline = lines[len(lines)-2].split("  ")
        xlat = float(latline[1])

        shp = model_info['Shapefile']
        field = model_info["ID Field"]
        feature = model_info["GageID"]
        #gets basin area
        area = utils.get_feature_area(shp, field, feature)/1000000

        #add area and latitude to basin dictionary
        basedict = {"name": model_info["GageID"], "area": area, "xlat": xlat, "whc":177}
        model_info["Basin Dict"] = basedict

##        #get zipped shapefile
##        shp = self.getInputFromPort("Shapefile").name
##        print shp
##        wkdir = os.path.join(model_info['Directory'],'BASE')
##        os.chdir(wkdir)
##        try:
##            uploadshapefile.upload_shapefile(shp)
##        except:
##            print(shp_name + " already exists on the GDP")
##        model_info["Zipped Shapefile"] = os.path.join(wkdir,'G'+model_info['GageID']+"_shp.zip")

        self.setResult("model_info", model_info)

class NWIS_Streamflow(Module):

    #model_info has directory, gageid, wkdir, and POR
    _input_ports = [("model_info", '(edu.utah.sci.vistrails.basic:Dictionary)')]


    _output_ports = [("Daily Streamflow", '(edu.utah.sci.vistrails.basic:File)'),
                     ("Monthly Streamflow", '(edu.utah.sci.vistrails.basic:File)'),
                     ("Hydrograph (image)", '(edu.utah.sci.vistrails.basic:File)'),
                     ("Station Name/Attributes", '(edu.utah.sci.vistrails.basic:String)')]

    def compute(self):

        model_info = self.getInputFromPort("model_info")
        gageid = model_info["GageID"]

        #get directory
        os.chdir(model_info['Directory'])

        #get por
        por = model_info["POR Calibration"]
        start_date = por["Start Date"]
        end_date = por["End Date"]
        #get dates into year-mo-da format
        sd = start_date.split("-")
        start = date(int(sd[0]), int(sd[1]), int(sd[2]))
        ed = end_date.split("-")
        end = date(int(ed[0]), int(ed[1]), int(ed[2]))

        pname = os.path.join(os.getcwd(), 'BASE')
        os.chdir(pname)
        area = model_info['Basin Dict']
        vt_gt_Streamflow.main_func(gageid, start, end, area['area'])

        #save popup window as well as txt files to base
        fig1 = os.path.join(os.getcwd(), "figure1.png")
        self.setResult("Hydrograph (image)", fig1)
        daily = os.path.join(os.getcwd(), "Flows_daily.txt")
        self.setResult("Daily Streamflow", daily)
        monthly = os.path.join(os.getcwd(), "Flows_monthly.txt")
        self.setResult("Monthly Streamflow", monthly)

class GDP(Module):

    #model_info contains directory, climate, shapefile, gageid
    _input_ports = [("model_info", '(edu.utah.sci.vistrails.basic:Dictionary)'),
                    ("Scenarios", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Climate Dataset", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Simulation Start Date", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Simulation End Date", '(edu.utah.sci.vistrails.basic:String)')]

    _output_ports = [("model_info", '(edu.utah.sci.vistrails.basic:Dictionary)')]

    def compute(self):

        #get inputs from model_info dictionary
        model_info = self.getInputFromPort("model_info")
        gageid = model_info['GageID']
        shp = model_info['Shapefile']
        idfield = model_info['ID Field']
        os.chdir(model_info["Directory"])
        climate = self.getInputFromPort("Climate Dataset")
        model_info['Climate'] = climate
        curdir = os.getcwd()

        basedir = os.path.join(curdir,"BASE", model_info['Base File'])
        fname = open(basedir, 'a')
        fname.write('Climate Dataset for Current/Historic Conditions = '+climate+'\n')
        fname.close()

        #if specified climate dataset is for CC
        if climate in ['PRISM', 'GSD', 'DAYMET']:
            por_calib = model_info['POR Calibration']
            #create directory for climate dataset if non-exisent
            dname = os.path.join(curdir, 'CC', climate)
            if not os.path.exists(dname):
                os.makedirs(dname)
            curdir = dname
            climdir = ['INPUT', 'OUTPUT']
            for subdir in climdir:
                full_dname = os.path.join(curdir, subdir)
                if not os.path.exists(full_dname):
                    os.makedirs(full_dname)

            #run the gdp for cc
            os.chdir(os.path.join(model_info['Directory'],'CC',climate,'INPUT'))
            climate_dict = mows_pyGDP_VT.main_func(gageid, shp, climate, por_calib, idfield)
            model_info['Climate Dict'] = climate_dict

        #if specified climate dataset for FC
        if climate in ['CMIP3', 'CMIP5']:
            start = self.getInputFromPort("Simulation Start Date")
            start_split = start.split("-")
            sm = int(start_split[0])
            sy = int(start_split[1])
            start_date = str(date(sy,sm,01))
            #end date for simulation period
            end = self.getInputFromPort("Simulation End Date")
            end_split = end.split("-")
            em = int(end_split[0])
            ey = int(end_split[1])
            end_date = str(date(ey,em,01))

            # get GSD data to calibrate MWBM for current conditions
            por_calib = model_info['POR Calibration']
            dname = os.path.join(curdir, 'CC', 'GSD')
            if not os.path.exists(dname):
                os.makedirs(dname)
            curdirCC = dname
            climdir = ['INPUT', 'OUTPUT']
            for subdir in climdir:
                full_dname = os.path.join(curdirCC, subdir)
                if not os.path.exists(full_dname):
                    os.makedirs(full_dname)

            os.chdir(os.path.join(model_info['Directory'],'CC','GSD','INPUT'))
            climate_dict = mows_pyGDP_VT.main_func(gageid, shp, 'GSD', por_calib, idfield)
            model_info['Climate Dict'] = climate_dict

            model_info["POR Simulation"] = {"Start Date": start_date, "End Date": end_date}
            por_sim = model_info['POR Simulation']

            startdate = por_sim["Start Date"].split("-")
            startMonth = startdate[1]
            startYear = startdate[0]
            enddate = por_sim["End Date"].split("-")
            endMonth = enddate[1]
            endYear = enddate[0]
            fname = open(basedir,'a')
            fname.write("Simulation Period for Future Conditions = "+startMonth+'/'+startYear+" to "+endMonth+'/'+endYear+'\n')
            fname.close()

            #create directory for climate dataset if non-existent
            scen = self.getInputFromPort("Scenarios")
            scenarios=scen.split(",")
            dname = os.path.join(curdir, 'FC', 'BCSD_'+climate)
            if not os.path.exists(dname):
                os.makedirs(dname)
            curdir = dname
            for scen in scenarios:
                full_dname = os.path.join(curdir, scen)
                if not os.path.exists(full_dname):
                    os.makedirs(full_dname)

            os.chdir(os.path.join(model_info['Directory'], 'FC', 'BCSD_'+climate))
            mows_pyGDP_VT_FC.main_func(gageid, shp, climate, por_sim, idfield, scenarios)

        os.chdir(model_info['Directory'])
        self.setResult("model_info", model_info)

class WBM_CC(Module):


    _input_ports = [("model_info", '(edu.utah.sci.vistrails.basic:Dictionary)'),
                    ("Calibration POR", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Evaluation POR", '(edu.utah.sci.vistrails.basic:String)')]

    def compute(self):

        model_info = self.getInputFromPort("model_info")
        BasinDict = model_info['Basin Dict']
        CalClimate = model_info['Climate']
        fname = model_info['Base File']
        basin = BasinDict['name']
        xlat = float(BasinDict['xlat'])
        area = float(BasinDict['area'])
        whc = float(BasinDict['whc'])
        print (xlat)
        print (area)
        print(whc)

        calpor = self.getInputFromPort("Calibration POR")
        cal = calpor.split(",")
        calstart = date(int(cal[0]),1,1)
        #calstart = date(1990,1,1)
        calend = date(int(cal[1]),12,31)
        #calend = date(1999,12,31)

        evalpor = self.getInputFromPort("Evaluation POR")
        evals = evalpor.split(",")
        evalstart = date(int(evals[0]),1,1)
        #evalstart = date(1980,1,1)
        evalend = date(int(evals[1]),12,31)
        #evalend = date(1989,12,31)

        yrslist = str(calstart.year)+","+str(calend.year)+","+str(evalstart.year)+","+str(evalend.year)
        wkdir = os.getcwd()

        Rscript="C:/Users/abock/Documents/R/R-2.15.1/bin/Rscript.exe"

        #WBMscript1="D:/abock/Water_Balance/WBM_Andy/Prev/MWBM_clean/sce_tw_calibration.R"
        WBMscript1="C:/Users/abock/VisTrails_SAHM/vistrails/packages/WaterBalanceModel/sce_tw_calibration.R"
        subprocess.call(Rscript+" "+WBMscript1+" "+wkdir+" "+CalClimate+" "+basin+" "+str(xlat)+" "+str(area)+" "+str(whc)+" "+yrslist+" "+fname,shell=False)
        Graphscript="C:/Users/abock/VisTrails_SAHM/vistrails/packages/WaterBalanceModel/CC_mean_monthly.R"
        print wkdir
        subprocess.call(Rscript+" "+Graphscript+" "+wkdir+" "+CalClimate+" "+basin,shell=False)

class WBM_FC(Module):

    _input_ports = [("model_info", '(edu.utah.sci.vistrails.basic:Dictionary)'),
                    ("Calibration POR", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Evaluation POR", '(edu.utah.sci.vistrails.basic:String)')]

    _output_ports = [("model_info", '(edu.utah.sci.vistrails.basic:Dictionary)')]

    def compute(self):

        #Build list of gcm's for where output should be stored
        model_info = self.getInputFromPort("model_info")
        curdir = model_info['Directory']
        os.chdir(curdir)
        wkdir = os.path.join(curdir, 'FC')
        os.listdir(wkdir)
        gcm_list = []
        for climate_data in os.listdir(wkdir):
            clim = os.path.join(wkdir, climate_data)
            if os.path.isdir(clim):
                for scenario in os.listdir(clim):
                    scen = os.path.join(clim, scenario)
                    if os.path.isdir(scen):
                        for gcm_name in os.listdir(scen):
                            gcmdir = os.path.join(scen, gcm_name)
                            if os.path.isdir(gcmdir):
                                for gcm_name_run in os.listdir(gcmdir):
                                    gcmnamedir = os.path.join('FC', climate_data, scenario, gcm_name, gcm_name_run)
                                    gcm_list.append(gcmnamedir)


        print (gcm_list)
        #Define climate
        calClimate = model_info['Climate']
        #BasinDict={'name':'G06746095', 'xlat':'40.53', 'area':'8.12','whc':'80'}
        BasinDict = model_info['Basin Dict']
        basin = BasinDict['name']
        xlat = float(BasinDict['xlat'])
        area= float(BasinDict['area'])
        #is whc used in WBM_FC
        whc= float(BasinDict['whc'])

class WBM_FC(Module):
    _input_ports = [("model_info", '(edu.utah.sci.vistrails.basic:Dictionary)')]

    _output_ports = [("model_info", '(edu.utah.sci.vistrails.basic:Dictionary)')]

    def compute(self):

        #Build list of gcm's for where output should be stored
        model_info = self.getInputFromPort("model_info")
        curdir = model_info['Directory']
        os.chdir(curdir)
        wkdir = os.path.join(curdir, 'FC')
        os.listdir(wkdir)
        gcm_list = []
        for climate_data in os.listdir(wkdir):
            clim = os.path.join(wkdir, climate_data)
            if os.path.isdir(clim):
                for scenario in os.listdir(clim):
                    scen = os.path.join(clim, scenario)
                    if os.path.isdir(scen):
                        for gcm_name in os.listdir(scen):
                            gcmdir = os.path.join(scen, gcm_name)
                            if os.path.isdir(gcmdir):
                                for gcm_name_run in os.listdir(gcmdir):
                                    gcmnamedir = os.path.join('FC', climate_data, scenario, gcm_name, gcm_name_run)
                                    gcm_list.append(gcmnamedir)


        #Define climate
        calClimate = model_info['Climate']
        #BasinDict={'name':'G06746095', 'xlat':'40.53', 'area':'8.12','whc':'80'}
        BasinDict = model_info['Basin Dict']
        basin = BasinDict['name']
        xlat = float(BasinDict['xlat'])
        area= float(BasinDict['area'])
        #is whc used in WBM_FC
        whc= float(BasinDict['whc'])

        print(gcm_list)

def initialize(*args, **keywords):

    modelin = get_module_registry()
    modelin.add_module(Model_Input)

    nwis_stream = get_module_registry()
    nwis_stream.add_module(NWIS_Streamflow)

    gdp = get_module_registry()
    gdp.add_module(GDP)

    wbm_cc = get_module_registry()
    wbm_cc.add_module(WBM_CC)

    wbm_fc = get_module_registry()
    wbm_fc.add_module(WBM_FC)