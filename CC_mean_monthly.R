library(zoo)

#####################################
args<-commandArgs(trailingOnly = TRUE)
print (args)
gage<-args[3]
#gage<-"G01411300"
dirpath<-args[1]
#setwd(paste("D:/abock/Water_Balance/WBM_Andy/VT_Testing","/",gage,sep=""))
setwd(dirpath)
#dataset<-"PRISM"
dataset<-args[2]

print (dirpath)
print(dataset)

wkdir<-getwd()
month_obs<-paste(wkdir,"/BASE/Flows_monthly.txt",sep="")
obs_sf<-read.table(month_obs,header=FALSE)
colnames(obs_sf)<-c("year","month","cms")
# create monthly - first step
day="01"
date=c(paste(obs_sf$year,"-",obs_sf$month,"-",day,sep=""))
dates<-as.character(date)
dates1<-as.Date(dates)
obsTs<-zoo(obs_sf$cms,dates1)

#working directory of scenarios
wkdir<-paste(wkdir,"/CC/",dataset,sep="")
#loop through scenarios
outfile<-paste(wkdir,"/OUTPUT/tw.txt",sep="")
output<-read.table(outfile)
colnames(output)<-c("Flag","Year","Month","PET","P","P-PET","SoilMoisture","AET","PET-AET","SnowStorage","Surplus","ROtotalmm","ROtotalcms")
year<-output$Year
month<-output$Month
day="01"
date=c(paste(year,"-",month,"-",day,sep=""))
dates<-as.character(date)
dates1<-as.Date(dates)
simTs<-zoo(output$ROtotalcms,dates1)

# combine observed and sim into one timeseries, 
Final<-merge(obsTs,simTs)
FinalDates<-time(Final)
start<-min(format.Date(FinalDates,"%Y"))
end<-max(format.Date(FinalDates,"%Y"))

annualSF<-aggregate(Final,as.integer(format(index(Final),"%Y")),mean)
#plot data for POR
a<-max(annualSF,na.rm=TRUE)
jpeg(paste(wkdir,"/OUTPUT/",gage,"_",dataset,"_annual.jpg",sep=""),width=1200,height=1200,res=50)
par(mfrow=c(1,1), mar=c(9,9,6,6))
plot(annualSF, col=c("blue","red"),type="l",ylim=c(0,a+(a*.1)),xlab="Year",ylab="Streamflow (CMS)",plot.type="single",
     main=paste("Annual Streamflow for",gage,start,"to",end,sep=" "),cex.lab=2.5,cex.axis=2,lwd=5.0,cex.main=3)
legend("topright", c("Measured Streamflow","Simulated Streamflow"), cex=3,lty = 1, col = c("blue","red"),lwd=5.0)
dev.off()

#sim_months<-aggregate(Var_mat,by=list(Month=Var_mat[,2]),FUN=mean,na.rm=TRUE)
#********************************************************************************
# make mean monthly plot
mmSF<-aggregate(Final,as.integer(format(index(Final),"%m")),mean,na.rm=TRUE)
#plot data for POR
a<-max(mmSF,na.rm=TRUE)
jpeg(paste(wkdir,"/OUTPUT/",gage,"_",dataset,"_mm.jpg",sep=""),width=1200,height=1200,res=50)
par(mfrow=c(1,1), mar=c(9,9,6,6))
plot(mmSF, col=c("blue","red"),type="l",ylim=c(0,a+(a*.1)),xlab="Mont",ylab="Streamflow (CMS)",plot.type="single",
     main=paste("Mean Monthly Streamflow for",gage,start,"to",end,sep=" "),cex.lab=2.5,cex.axis=2,lwd=5.0,cex.main=3)
legend("topright", c("Measured Streamflow","Simulated Streamflow"), cex=3,lty = 1, col = c("blue","red"),lwd=5.0)
dev.off()

#*********************************************************************************
# make a boxplot#
#cmonth<-format(time(Final),"%b")
#months<-factor(cmonth,levels=unique(cmonth),ordered=TRUE)
#boxplot(coredata(Final$obsTs)~months,col=c("blue","red"))
#z.winter <- z[months(time(z), TRUE) %in% c("Dec", "Jan", "Feb")]

# subset to make vector of eah month
#sim_jan<-subset(Final$obsTs,subset= (months(time(Final)=="January")))
sim_jan<-coredata(Final$simTs[months(time(Final,TRUE)) =="January"])
obs_jan<-coredata(Final$obsTs[months(time(Final,TRUE)) =="January"])

sim_feb<-coredata(Final$simTs[months(time(Final,TRUE)) =="February"])
obs_feb<-coredata(Final$obsTs[months(time(Final,TRUE)) =="February"])

sim_mar<-coredata(Final$simTs[months(time(Final,TRUE)) =="March"])
obs_mar<-coredata(Final$obsTs[months(time(Final,TRUE)) =="March"])

sim_apr<-coredata(Final$simTs[months(time(Final,TRUE)) =="April"])
obs_apr<-coredata(Final$obsTs[months(time(Final,TRUE)) =="April"])

sim_may<-coredata(Final$simTs[months(time(Final,TRUE)) =="May"])
obs_may<-coredata(Final$obsTs[months(time(Final,TRUE)) =="May"])

sim_jun<-coredata(Final$simTs[months(time(Final,TRUE)) =="June"])
obs_jun<-coredata(Final$obsTs[months(time(Final,TRUE)) =="June"])

sim_jul<-coredata(Final$simTs[months(time(Final,TRUE)) =="July"])
obs_jul<-coredata(Final$obsTs[months(time(Final,TRUE)) =="July"])

sim_aug<-coredata(Final$simTs[months(time(Final,TRUE)) =="August"])
obs_aug<-coredata(Final$obsTs[months(time(Final,TRUE)) =="August"])

sim_sep<-coredata(Final$simTs[months(time(Final,TRUE)) =="September"])
obs_sep<-coredata(Final$obsTs[months(time(Final,TRUE)) =="September"])

sim_oct<-coredata(Final$simTs[months(time(Final,TRUE)) =="October"])
obs_oct<-coredata(Final$obsTs[months(time(Final,TRUE)) =="October"])

sim_nov<-coredata(Final$simTs[months(time(Final,TRUE)) =="November"])
obs_nov<-coredata(Final$obsTs[months(time(Final,TRUE)) =="November"])

sim_dec<-coredata(Final$simTs[months(time(Final,TRUE)) =="December"])
obs_dec<-coredata(Final$obsTs[months(time(Final,TRUE)) =="December"])

# bind the month data into a matrix
month_data<-cbind(sim_jan,obs_jan,sim_feb,obs_feb,sim_mar,obs_mar,
                  sim_apr,obs_apr,sim_may,obs_may,sim_jun,obs_jun,
                  sim_jul,obs_jul,sim_aug,obs_aug,sim_sep,obs_sep,
                  sim_oct,obs_oct,sim_nov,obs_nov,sim_dec,obs_dec)

# creates jpeg to write output too 
# make sure you specificy work dir (getwd())

jpeg(paste(wkdir,"/OUTPUT/",gage,"_MBoxPlot.jpg",sep=""),width=1500,height=800,res=150)

# turns clippint off
par(xpd=FALSE,oma=c(0,0,0,5)) 

# create boxplot
boxplot(month_data,col=c("red","blue","red","blue","red","blue","red","blue","red","blue","red","blue",
                         "red","blue","red","blue","red","blue","red","blue","red","blue","red","blue"),
                         main=paste("Variability in Streamflow,",gage,start,"to",end,sep=" "),cex.main=1.5,
                         notch=FALSE,ylab="Streamflow (cms)",xaxt="n",ann=FALSE,boxwex=0.5)
# set x-axis labels
axis(1, at=c(1.5,3.5,5.5,7.5,9.5,11.5,13.5,15.5,17.5,19.5,21.5,23.5),
     labels=c("Jan","Feb","Mar","Apr","May","June",
              "July","Aug","Sep","Oct","Nov","Dec"))

# put in lines to separate months
abline(v=c(2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5),lwd=2)

# turn clipping off
par(xpd=NA)
dev.off()
#******************************************************************
sim_winter<-coredata(Final$simTs[months(time(Final,TRUE)) %in% c("December","January","February")])
sim_spring<-coredata(Final$simTs[months(time(Final,TRUE)) %in% c("March","April","May")])
sim_summer<-coredata(Final$simTs[months(time(Final,TRUE)) %in% c("June","July","August")])
sim_fall<-coredata(Final$simTs[months(time(Final,TRUE)) %in% c("September","October","November")])

obs_winter<-coredata(Final$obsTs[months(time(Final,TRUE)) %in% c("December","January","February")])
obs_spring<-coredata(Final$obsTs[months(time(Final,TRUE)) %in% c("March","April","May")])
obs_summer<-coredata(Final$obsTs[months(time(Final,TRUE)) %in% c("June","July","August")])
obs_fall<-coredata(Final$obsTs[months(time(Final,TRUE)) %in% c("September","October","November")])

# bind the month data into a matrix
month_data<-cbind(sim_winter,obs_winter,sim_spring,obs_spring,
                  sim_summer,obs_summer,sim_fall,obs_fall)

# creates jpeg to write output too 
# make sure you specificy work dir (getwd())

jpeg(paste(wkdir,"/OUTPUT/",gage,"_SeasBoxPlot.jpg",sep=""),width=1500,height=800,res=150)

# turns clippint off
par(xpd=FALSE,oma=c(0,0,0,5)) 

# create boxplot
boxplot(month_data,col=c("red","blue","red","blue","red","blue","red","blue"),
        main=paste("Variability in Streamflow,",gage,start,"to",end,sep=" "),cex.main=1.5,
        notch=FALSE,ylab="Streamflow (cms)",xaxt="n",ann=FALSE,boxwex=0.5)
# set x-axis labels
axis(1, at=c(1.5,3.5,5.5,7.5),
     labels=c("Winter","Spring","Summer","Fall"))

# put in lines to separate months
abline(v=c(2.5,4.5,6.5),lwd=2)

# turn clipping off
par(xpd=NA)
dev.off()


# sim_feb<-subset(Var_mat[,3],subset= Var_mat[,2] ==2)
# obs_feb<-subset(Var_mat[,4],subset= Var_mat[,2] ==2)
