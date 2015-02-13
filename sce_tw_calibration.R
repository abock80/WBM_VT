# R script wrapper to implement SCE-UA (Duan et al 1994) calibration of Thornthwait model (TW).
#
# Script calls: SCEoptim
#
# Created: Bureau of Reclamation   2012-12
#
# DISCLAIMER:
# This code is being made available for the purpose of calibrating the Thornthwaite
# hydrologic model (McCabe and Markstrom, 2007) by interested persons.   The U.S. 
# Department of Interior's Bureau of Reclamation believes the information to be correct 
# representations of published theoretical processes.  However, human 
# and mechanical errors remain possibilities. Therefore, the Bureau of Reclamation does not 
# guarantee the accuracy and robustness of the modeling tools.
# Also, Bureau of Reclamation, nor any of the sources of the information shall be 
# responsible for any errors or omissions, or for the use or results obtained from the use
# of this modeling tool.
#
# References:
# Duan, Q., Sorooshian, S., and Gupta, V.K. (1994). “Optimal use of the SCE-UA global 
#   optimization method for calibrating watershed models,” Journal of Hydrology, 158, 
#   pp 265-284.
# McCabe, G.J., and Markstrom, S.L., 2007, A monthly water-balance model driven by a
#   graphical user interface: U.S. Geological Survey Open-File report 2007-1088, 6 p.
#
####################################################################################
# using R 2.15.1 with hydromad
library(hydromad)

################################################################################################
### USER INPUTS ###
#1 - enter arguments
args <- commandArgs(trailingOnly = TRUE)
dirpath<-args[1]
calClimate<-args[2]
basin<-args[3]
xlat<-as.numeric(args[4])
area<-as.numeric(args[5])
whc<-as.numeric(args[6])
yrs<-args[7]
fname<-args[8]
yrsList<-unlist(strsplit(yrs,","))
wystart<-as.numeric(yrsList[1])
wyend<-as.numeric(yrsList[2])
valWYst<-as.numeric(yrsList[3])
valWYend<-as.numeric(yrsList[4])

argsList<-c(dirpath,calClimate,basin,xlat,area,whc,yrsList,fname)
write.table(argsList,"d:/abock/temp/haha.txt")

print (dirpath)
print (calClimate)
print (basin)
print (xlat)
print (area)
print (whc)
print (yrs)
weights<-c(1,1,1)

# write.table(argsList,"d:/abock/temp/haha2.txt")
# dirpath="D:/abock/temp/G06746095"
# calClimate<-'PRISM'
# basin <-'G06746095'
# xlat = 40.53126
# area<- 8.12
# whc=80
# weights<-c(1,1,1)
# wystart<-1990
# wyend<-1999
# valWYst<-1980
# valWYend<-1989

#**********************************************************
# user defined directories
# where the climate data, parameter ranges are held
in_dir = paste(dirpath,"/CC/",calClimate,"/INPUT",sep="")
# where streamflow and ouput is stored
out_dir = paste(dirpath,"/CC/",calClimate,"/OUTPUT",sep="")
# where scripts are stored 
#src_dir = 'D:/abock/Water_Balance/WBM_Andy/Prev/MWBM_clean/src'
src_dir="C:/Users/abock/VisTrails_SAHM/vistrails/packages/WaterBalanceModel/src"


write.table(argsList,"d:/abock/temp/haha3.txt")
# functions to be called in this script
srclist=c("objective_fun.R", "assign_wy2flows_mon.R", "subset_monthly_flows.R", "wb.R","mm2cms.R")
nsrc=length(paste(src_dir,srclist,sep=""))
for(i in 1:nsrc){
  source(file.path(src_dir, srclist[i]))
}

write.table(argsList,"d:/abock/temp/haha4.txt")
# read parameter range file (in order of rfactor,directfac, tsnow, train,xmeltcoeff)
param_lower <- c(0.1,0.001,-10.0,0.001,0.001)
param_upper <- c(1.0,0.1,-2.0,10.0,1.0)
par<-c(0.5,0.05,-4.0,7.0,0.47)

#translate params to variable names
rfactor  <- par[1]
directfac	<- par[2]
tsnow		<- par[3]
train		<- par[4]
xmeltcoeff  <- par[5]

#tw <- wb(xlat,whc,rfactor,directfac,tsnow,train,xmeltcoeff,in_dir)
write.table(argsList,"d:/abock/temp/haha5.txt")
ob<-objective_fun(par, basin, xlat, whc,area, weights, wystart, wyend, src_dir, in_dir,lower=param_lower, upper=param_upper)

print("  Call SCE...")
ans <-SCEoptim(objective_fun,par,
	basin,xlat,whc,area,weights,wystart,wyend,src_dir,in_dir,
	lower=param_lower,upper=param_upper,
	control=list(fnscale=-1,maxit=10000,tolsteps=10,reltol=0.1,ncomplex=5))

optpar=ans$par	
print("  Optimal parameters:")
print(optpar)

#post-processing with optimal parameters
infofile<-paste(dirpath,'/BASE/',fname,sep="")
write.table(infofile,"d:/abock/temp/haha8.txt")

#write optimal parameters to file
write("Optimal Parameters",infofile,append=T)
write("------------------",infofile,append=T)
line1=paste("Soil moisture storage capacity (mm)   = ",whc,sep="")
line2=paste("Runoff factor                         = ",optpar[1],sep="")
line3=paste("Maximum melt rate                     = ",optpar[2],sep="")
line4=paste("Direct runoff factor                  = ",optpar[3],sep="")
line5=paste("Snow temperature threshold (degree C) = ",optpar[4],sep="")
line6=paste("Rain temperature threshold (degree C) = ",optpar[5],sep="")
modelpar=paste(line1,line2,line3,line4,line5,line6,sep="\n")
write(modelpar,infofile,append=T)

write.table(optpar,"d:/abock/temp/haha9.txt")

#run water balance with optimal parameters
tw <- wb(xlat,whc,optpar[1],optpar[2],optpar[3],optpar[4],optpar[5],in_dir)

write.table(tw,"d:/abock/temp/haha11.txt")
yr<-tw[,1]
month<-tw[,2]
runoff<-tw[,11]
simflow <- mm2cms(yr,month,runoff,area)  #reads in year, month, ROtot
tw<-cbind(tw,simflow[,3])

#write stats
write("Simulation Statistics",infofile,append=T)
write("---------------------",infofile,append=T)

obsfl <- paste(dirpath,"/BASE/Flows_monthly.txt",sep="",collapse=NULL)
obsflow <- read.table(obsfl)
obj_func <- calcOBJfunc(obsflow,simflow,weights,wystart,wyend)
#assign wy to monthly flows
obs_mat_wy <- assign_wy2flows_mon(obsflow)
sim_mat_wy <- assign_wy2flows_mon(simflow)
#subset sim and obs to chosen years
obs_mat_sub <- subset_monthly_flows(obs_mat_wy)
sim_mat_sub <- subset_monthly_flows(sim_mat_wy)
#build data frames
obs_df <- data.frame(wy=obs_mat_sub[,1],mon=obs_mat_sub[,2],obs=obs_mat_sub[,3])
sim_df <- data.frame(wy=sim_mat_sub[,1],mon=sim_mat_sub[,2],sim=sim_mat_sub[,3])
# compute annual ts by water year
obs_wy<-aggregate(obs_df["obs"], by=obs_df[c("wy")], FUN=mean)
sim_wy<-aggregate(sim_df["sim"], by=sim_df[c("wy")], FUN=mean)

write.table(tw,"d:/abock/temp/haha12.txt")

nse_mon <- nseStat(obs_df$obs, sim_df$sim, ref = NULL, p = 2, trans = NULL, negatives.ok = FALSE, na.action = na.pass)
line1=paste("Monthly Nash-Sutcliffe coefficient = ",nse_mon,sep="")

nse_wy <- nseStat(obs_wy$obs, sim_wy$sim, ref = NULL, p = 2, trans = NULL, negatives.ok = FALSE, na.action = na.pass)
line2=paste("Annual Nash-Sutcliffe coefficient = ",nse_wy,sep="")

cor_mon <- cor(obs_df$obs, sim_df$sim, method = "pearson")
line3=paste("Monthly correlation coefficient = ",cor_mon,sep="")
stats=paste(line1,line2,line3,sep="\n")
write(stats,infofile,append=T)

write.table(tw,"d:/abock/temp/haha13.txt")

#write water balance
write("Water Balance",infofile,append=T)
write("-------------",infofile,append=T)
header="Flag Year Month PET P P-PET SoilMoisture AET PET-AET SnowStorage Surplus ROtotalmm ROtotalcms"
write(header,infofile,append=T)

#append flag column indicating whether year is part of calibration period or validation period 
#(0=none,1=cal,2=val)
#ifelse(((month==2 & yr%%4==0 & yr%%100!=0) | (month==2 & yr%%400==0)),29,days[month])
tmp<-cbind(tw[,1],tw[,2],tw[,12])
tmp2<-assign_wy2flows_mon(tmp)
flag<-matrix(0, length(tmp2[,1]))
colnames(flag) <- "Flag"

write.table(tw,"d:/abock/temp/haha14.txt")

# add flag for calibration years
for(i in 1:length(tmp2[,1])){
  ifelse((tmp2[i,1]>=wystart & tmp2[i,1]<=wyend),flag[i]<-1,flag[i]<-0)
}
# add flag for validation years
for(i in 1:length(tmp2[,1])){
  ifelse((tmp2[i,1]>=valWYst & tmp2[i,1]<=valWYend),flag[i]<-2,flag[i])
}
outmat<-cbind(flag,tw)
write.table(outmat,infofile,row.names=F,col.names=F,sep=" ",append=TRUE)
write.table(outmat,paste(out_dir,"/tw.txt",sep=""),row.names=F,col.names=F,quote=FALSE)
            
#make plots
sim_ts<-ts(sim_mat_sub[,3],frequency=12,start=c(head(sim_mat_sub[,1],1),head(sim_mat_sub[,2],1)))
obs_ts<-ts(obs_mat_sub[,3],frequency=12,start=c(head(obs_mat_sub[,1],1),head(obs_mat_sub[,2],1)))

plotMax<-max(max(obs_ts),max(sim_ts))
write.table(plotMax,"d:/abock/temp/haha15.txt")

png(paste(out_dir,"/",basin,"_plot.png",sep="",collapse=NULL),width=11, height=8.5, units="in",res=600)
plot(sim_ts,type="l",xlab="time",ylab="flow (cms)",ylim=c(0,plotMax))
title(main=basin)
lines(obs_ts,col="blue")
legend("topright", c("Natural Flow","Simulated Flow"), lty = 1, col = c("blue","black"))
#dev.print(pdf,paste(out_dir,"/",basin,"_plot.pdf",sep="",collapse=NULL))
#dev.copy(png,file = paste(out_dir,"/",basin,"_plot.png",sep="",collapse=NULL),width = 11, height = 8.5, units = "in", res=600)
dev.off()
