# option 1
# person passes in CMPI3/5, basin, xlat, area, whc, params (CMIP3 - dataset variable)
# each gcm is run in the R script
# 

###############################################################################################
## USER INPUTS ###
# 1 - enter arguments
args <- commandArgs(trailingOnly = TRUE)
dirpath<-args[1]
basin<-args[2]
xlat<-as.numeric(args[3])
area<-as.numeric(args[4])
whc<-as.numeric(args[5])
params<-args[6]
paramsList<-unlist(strsplit(params,","))
rfactor<-as.numeric(paramsList[1])
directfac<-as.numeric(paramsList[2])
tsnow<-as.numeric(paramsList[3])
train<-as.numeric(paramsList[4])
xmeltcoeff<-as.numeric(paramsList[5])

#dirpath<-'D:/VisTrails/4_WBM_FC'
#basin<-'G01033500'
#xlat<-45.4825167546355
#area<-0.000890536169800689
#whc<-177
#params<-'0.684827295264625,0.0999674191419909,-8.03489623304143,6.43195968375518,0.999967750363658'
#paramsList<-unlist(strsplit(params,","))
#rfactor<-as.numeric(paramsList[1])
#directfac<-as.numeric(paramsList[2])
#tsnow<-as.numeric(paramsList[3])
#train<-as.numeric(paramsList[4])
#xmeltcoeff<-as.numeric(paramsList[5])
#**********************************************************
src_dir = 'C:/Users/abock/VisTrails_SAHM/vistrails/packages/WaterBalanceModel'

# functions to be called in this script
srclist=c("wb.R")
nsrc=length(paste(src_dir,srclist,sep=""))
for(i in 1:nsrc){
  source(file.path(src_dir, srclist[i]))
}

gcms<-list.dirs(paste(dirpath,"/",basin,"/FC/BCSD_CMIP3/b1",sep=""),full.names=TRUE,recursive=FALSE)
runs<-sapply(gcms,list.files,full.names=TRUE)
allRuns<-unlist(runs)

for (run in allRuns){
  print (run)
  #test out WBM code
  tw <- wb(xlat,whc,rfactor,directfac,tsnow,train,xmeltcoeff,paste(run,"/INPUT",sep=""))
  write.table(tw,paste(run,"/OUTPUT/yeppers.txt",sep=""),sep=" ")
}


