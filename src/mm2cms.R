# Function to convert runoff depth in mm to flow in cms
# 
#
# Input: year, month, runoff, basin area
#
# Output: streamflow vector in cms
#
#
#------------------------------------------------------------------

"mm2cms" <- function(yr,month,runoff,area){  #units of input runoff are mm
  days = c(31,28,31,30,31,30,31,31,30,31,30,31) 

# Leap year if:   
#  Year Is divisible by 4.
#  Not if it is divissible by 100.
#  But is if it is divisible by 400.
  
  numdays=ifelse(((month==2 & yr%%4==0 & yr%%100!=0) | (month==2 & yr%%400==0)),29,days[month])
    
  m3 <- runoff*area*1000
  cms <- m3/86400/numdays
  simflow<-cbind(yr,month,cms)
  return(simflow)
}