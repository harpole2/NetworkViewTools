library(ggplot2)
library(stringr)
library(reshape2)
library(plotly)

#SET YOUR WORKING DIRECTORY
setwd("/home/me/myDirect/")
#Prefix for your files
files<-list.files(pattern=glob2rx("grow*.dat"))

#this is all pretty specific to naming
under<-str_locate_all(files[1], "_")
under<-unlist(under)
base<-substr(files[1],1,max(under))
list2env(
  lapply(setNames(files, make.names(gsub("*.dat$", "", files))), 
         read.table), envir = .GlobalEnv)
for (i in 1:length(files)){
  if (i==1) {
    x<-as.character(i)
    start<-paste(base,x,sep="")
    data<-get(start)
    colnames(data)[1] <- "Residue"
    colnames(data)[2] <- i
  }
  else {
    x<-as.character(i)
    start<-paste(base,x,sep="")
    data_ex<-get(start)
    data<-cbind(data,data_ex[2])
    colnames(data)[i+1]<-i
    
  }
}
#cut data in half
data_half<-data[,1:round(length(data)/2)]
#remove rows that are only zero
red_data<-data[as.logical(rowSums(data[-1]!=0)),]
red_data_half<-data_half[as.logical(rowSums(data_half[-1]!=0)),]
red_data_flip<-t(red_data)
red_data_half_flip <-t(red_data_half)



for (i in 1:nrow(red_data)){
  x<- as.character(red_data[i,1])
  name<-paste("graph_residue",x,sep="_")
  name_save<-paste(name,".pdf",sep="")
  temp_data<-red_data[i,-1]
  temp_data<-melt(temp_data)
  nums<-1:(ncol(red_data)-1)
  temp_data<-cbind(temp_data,nums)
  temp <- ggplot(data=temp_data) +
    theme_bw() +
    theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
    geom_point(aes(x=nums,y=value)) +
    ylab("Betweenness")+
    xlab("Source sphere expansion")+
    scale_x_continuous(breaks = seq(min(temp_data$nums), max(temp_data$nums), by = 2))
  temp <-ggplotly(temp)
  assign(name,temp,envir=.GlobalEnv)
  ggsave(name_save)
}

red_data_long<-melt(red_data, id = "Residue")
all_res <- ggplot(data=red_data_long, aes(variable, value, group=factor(Residue))) +
  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
  geom_point(aes(color=factor(Residue))) +
  geom_line(aes(color=factor(Residue))) +
  ylab("Betweenness")+
  xlab("Source sphere expansion")

all_res <-ggplotly(all_res)

#if you want to write the data
#write.table(res_and_last,file="/data/DEShaw_1/network/communities/test/chain_growth/new/dist_justSource/res_and_last.dat", col.names=F, row.names=F)
