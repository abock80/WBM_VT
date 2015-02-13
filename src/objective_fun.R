# Function to run hydrologic model and compute objective function
#  based on results
#
# Input: tw model initial parameters, basin, xlat, area, weights, 
#        wystart, wyend, src_dir, out_dir, finpt, parameter lower bounds
#        parameter upper bounds
#
# Output: objective function value
#
#---------------------------------------------------------------------

"objective_fun" <- function(params, 
	basin, xlat, whc,area, weights, wystart, wyend, src_dir, out_dir, finpt,
	lower, upper) {
  print (params)

	# functions to be called in this script
	srclist=c("assign_wy2flows_mon.R", "subset_monthly_flows.R", "calcOBJfunc.R", "wb.R","mm2cms.R")
	nsrc=length(paste(dirpath,srclist,sep=""))
	for(i in 1:nsrc){
	  source(file.path(src_dir, srclist[i]))
	}
		
  #translate params to variable names
  #whc		<- params[1]
  rfactor	<- params[1]
  directfac	<- params[2]
  tsnow		<- params[3]
  train		<- params[4]
  xmeltcoeff  <- params[5]
  # run TW model
  # print("   Call TW model...")
  #tw <- wb(xlat,150,rfactor,xmeltcoeff,directfac,tsnow,train,finpt)
  tw <- wb(xlat,whc,rfactor,directfac,tsnow,train,xmeltcoeff,in_dir)

  yr<-tw[,1]
  month<-tw[,2]
  runoff<-tw[,11]
    
  # convert output runoff (mm) to flow (cms)
  simflow <- mm2cms(yr,month,runoff,area)  #reads in year, month, ROtot
  
  # read simulated and observed flows for current simulation and compute objective function
  # obsfl <- paste(out_dir,"streamflow.obs\\",basin,".obs.mon",sep="",collapse=NULL)
  obsfl <- paste(dirpath,"/BASE/Flows_monthly.txt",sep="",collapse=NULL)
  obsflow <- read.table(obsfl)
  
  print("  Computing objective function for current simulation...")
  obj_func <- calcOBJfunc(obsflow,simflow,weights,wystart,wyend)
  
  return(obj_func)
  # end of function
}