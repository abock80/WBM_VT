 
"wb" <- function(xlat,whc,rfactor,directfac,tsnow,train,xmeltcoeff,in_dir){

#input water balance parameters and monthly prcp and location of input files
#xlat,whc,rfactor,xmeltcoeff,directfac,tsnow,train,in_dir

#constants
day=c(15.,45.,74.,105.,135.,166.,196.,227.,258.,288.,319.,349.)
days=c(31.,28.,31.,30.,31.,30.,31.,31.,30.,31.,30.,31.)

#define variable vectors
t <- p <- ro  <- pmpe <- pe <- sur <- deficit <- ae <- rodirect <- vector()
remain <- snstor <- stor <- snroff <- psnow <- prain <-  vector()

#read monthly input data - year, month, temperature (degree Celsius), precipitation (millimeters)
ppt<-read.table(paste(in_dir,"/PPT_month.txt",sep="",collapse=NULL))
p<-ppt[,3]
nt<-dim(ppt)[1]
yylist<-ppt[,1]
mmlist<-ppt[,2]
t<-read.table(paste(in_dir,"/TAVE_month.txt",sep="",collapse=NULL))[,3]


#initial soil water storage
prestor=150.0 

#loop through monthly time series
for (it in 1:nt){

  print(it)
  month=mmlist[it]
  
  #********************
  #initialize variables
  #********************

  pe[it]=0.0
  pmpe[it]=0.0
  ae[it]=0.0
  deficit[it]=0.0
  sur[it]=0.0
  ro[it]=0.0
  rodirect[it]=0.0

  snroff[it]=0.0
  stor[it]=0.0        
  prain[it]=0.0
  psnow[it]=0.0

  #*********************
  #compute snow and rain
  #*********************

  if(t[it]<=tsnow) psnow[it]=p[it]
  if((t[it] > tsnow)&&(t[it] < train)) psnow[it] = p[it] *((train-t[it])/(train-tsnow))
  if(t[it]>=train) psnow[it]=0.0
  prain[it]=p[it]-psnow[it]
  rodirect[it]=prain[it]*directfac
  prain[it]=prain[it]-rodirect[it]

  if (it==1){
    snstor[it]=psnow[it] #no initial snow storage
  }
  else {
    snstor[it]=snstor[(it-1)]+psnow[it]
  }
  
  #*******************
  #calculate daylength
  #*******************
  dayl=  day[month] - 80.0
  if(dayl < 0.0) dayl=285.0 + day[month]
  decd=23.45*sin(dayl/365.0*6.2832)
  decr=decd*.017453
  alat=xlat*.017453
  sintheta = tan(alat) * tan(decr)
  theta = asin(sintheta)
  dl = 12.0 + (2.0 * theta * 24. / (2.0 * 3.174))
  if(sintheta <= -1.0) dl = 0.0
  if(sintheta >=  1.0) dl= 24.0

  #******************
  #calculate hamon pe
  #******************
  pt=4.95*exp(.062*t[it])/100.
  pe[it]=.55*((dl/12.)**2)*pt*days[month]
  if(pe[it] <= 0.0) pe[it]=0.0
  pe[it]=pe[it]*25.4
  
  #*****************
  #compute snow melt
  #*****************
  snroff[it]=0.0
  if((snstor[it]>0.0)&&(t[it] > tsnow)){
    smf=(t[it]-tsnow)*xmeltcoeff/(train-tsnow)
    if (smf > xmeltcoeff) smf=xmeltcoeff
    snroff[it]=smf*snstor[it]
    snstor[it]=snstor[it]-snroff[it]
    if(snstor[it] < 0.0) snstor[it]=0.0
  } #endif
  
  #**********************
  #add snow melt to prain
  #**********************
  prain[it]=prain[it]+snroff[it]

  #************
  #compute pmpe
  #************
  pmpe[it]=prain[it]-pe[it]
  
  #*******************************************************
  #compute soil-moisture storage, ae, surplus, and deficit
  #*******************************************************
  if(pmpe[it] < 0.0){
    stor[it]=prestor-(abs(pmpe[it]*(prestor/whc)))
    if(stor[it] < 0.0) stor[it]=0.0
    delstor=stor[it]-prestor
    ae[it]=prain[it]+(delstor*(-1.0))
    prestor=stor[it]
    sur[it]=0.0
  }#end if
  if(pmpe[it] >= 0.0){
    ae[it]=pe[it]
    stor[it]=prestor+pmpe[it]
    if(stor[it] > whc){
      sur[it]=stor[it]-whc
      stor[it]=whc
    }#endif
    prestor=stor[it]
  }#endif
  deficit[it]=pe[it]-ae[it]
  
#  #*******************
#  #runoff calculations
#  #*******************

  if (it==1){
    ro[it]=(sur[it]+25.4)* rfactor
    remain[it]=(sur[it]+25.4)-ro[it]
  }
  else {
    ro[it]=(sur[it]+remain[it-1])*rfactor
    remain[it]=(sur[it]+remain[it-1])-ro[it]
  }
  if(remain[it] < 0.0) remain[it] =0.0
  ro[it]=ro[it]+rodirect[it]
} #it


#******
#output
#******
outmat=cbind(yylist,mmlist,pe,p,pmpe,stor,ae,deficit,snstor,sur,ro)
return(outmat)

} #end function


