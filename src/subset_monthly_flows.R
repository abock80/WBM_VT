#Function to subset monthly timeseries to chosen years
# input is matrix of monthly flows in format:
#     <cal_yr or water_yr> <mon> <flow>
# output is matrix of monthly flows in same format
#
#
#
#  Created: Marketa M. Elsner December 2012
############################################################


"subset_monthly_flows" <- function(timeseries){

  newdata <- timeseries[ which(timeseries[,1]>=wystart & timeseries[,1]<=wyend), ]
  return(newdata)
}

