#Function to compute weighted objective function for SCE-UA
#
# Input: observed flow <yr mon cms>, simulated flow <yr mon cms>,
#        weights, wystart, wyend
#
# Output: objective function value
#
#---------------------------------------------------------------------

"calcOBJfunc" <- function(obs_mat,sim_mat,weights,wystart,wyend){
  print(summary(obs_mat))
  print(summary(sim_mat))

   #assign wy to monthly flows
  obs_mat_wy <- assign_wy2flows_mon(obs_mat)
  sim_mat_wy <- assign_wy2flows_mon(sim_mat)
  print(summary(obs_mat_wy))
  print(summary(sim_mat_wy))
  
  #subset sim and obs to chosen years
  obs_mat_sub <- subset_monthly_flows(obs_mat_wy)
  sim_mat_sub <- subset_monthly_flows(sim_mat_wy)
  print(summary(obs_mat_sub))
  print(summary(sim_mat_sub))
  
  #build data frames
  obs_df <- data.frame(wy=obs_mat_sub[,1],mon=obs_mat_sub[,2],obs=obs_mat_sub[,3])
  sim_df <- data.frame(wy=sim_mat_sub[,1],mon=sim_mat_sub[,2],sim=sim_mat_sub[,3])
  
  print(summary(obs_df))
  print(summary(sim_df))
  # compute annual ts by water year
  obs_wy<-aggregate(obs_df["obs"], by=obs_df[c("wy")], FUN=mean)
  sim_wy<-aggregate(sim_df["sim"], by=sim_df[c("wy")], FUN=mean)
  
  # calculate monthly NSE for chosen water years  
   if(weights[1]!=0)
     nse_mon <- nseStat(obs_df$obs, sim_df$sim, ref = NULL, p = 2, trans = NULL, negatives.ok = FALSE, na.action = na.pass)
   else
     nse_mon <- 0
	
	 # calculate annual NSE
   if(weights[2]!=0)
     nse_wy <- nseStat(obs_wy$obs, sim_wy$sim, ref = NULL, p = 2, trans = NULL, negatives.ok = FALSE, na.action = na.pass)
  else
     nse_wy <- 0

   # calculate monthly correlations (mm)
   if(weights[3]!=0)
     cor_mon <- abs(cor(obs_df$obs, sim_df$sim, method = "pearson"))
   else
     cor_mon <- 0
	 
   # compute weighted objective function
   obj_value <- nse_mon*weights[1] + nse_wy*weights[2] + cor_mon*weights[3]
   
   print(c(nse_mon,nse_wy,cor_mon))
   return(obj_value)
} #end function