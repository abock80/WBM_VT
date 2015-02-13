#Function to assign water years to monthly timeseries
# input is matrix of monthly flows in format:
#     <cal_yr> <mon> <flow>
# output is matrix of monthly flows in format:
#     <water_yr> <mon> <flow>
#
#
#  Created: Bureau of Reclamation December 2012
############################################################


"assign_wy2flows_mon" <- function(timeseries){

  f <- function(x,y){
    if(x>9) {wy <- y+1} else {wy <- y}
    return(wy)
  }

  out=mapply(f,timeseries[,2],timeseries[,1])
  out_mat=cbind(out,timeseries[,2],timeseries[,3])

  return(out_mat)
}

