PathDistanceExtraction <- function(directory, filename) {

#libraries
library(plyr)
library(ggplot2)
library(tools)



setwd(directory)
lines<-readLines(filename)
nums=list()

#get distances from parenthesis and put in list
for (i in 1:length(lines)){
  x<-as.integer(gsub("[\\(\\)]", "", regmatches(lines, gregexpr("\\(.*?\\)", lines))[[i]]))

  if (length(x)!=0){
    nums=c(nums,x)
  }
  if (length(x)==0){
      next
    }
  
}

nums=as.numeric(nums)
#nums=as.factor(nums)
#help set plot limits
stats<-count(nums)
top<-max(stats$freq)

plot_hist_allbreaks <- ggplot() +
  aes(nums) +
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
  geom_histogram(binwidth=1, colour="black", fill="red") +
  scale_x_continuous(breaks=min(stats$x):max(stats$x)) +
  scale_y_continuous(expand = c(0, 0),limits=c(0,top+1), breaks=min(stats$freq):max(stats$freq)) +
  ylab("Number of paths")+
  xlab("Path Distances") +
  ggtitle("Optimal Path Histogram") +
  theme(axis.title.x=element_text(size=16),axis.title.y=element_text(size=16),
        plot.title=element_text(size=18))

plot_hist_1 <- ggplot() +
  aes(nums) +
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
  geom_histogram(binwidth=1, colour="black", fill="red") +
  scale_y_continuous(expand = c(0, 0),limits=c(0,top+1)) +
  scale_x_continuous(breaks=min(stats$x):max(stats$x)) +
  ylab("Number of paths")+
  xlab("Path Distances") +
  ggtitle("Optimal Path Histogram") +
  theme(axis.title.x=element_text(size=16),axis.title.y=element_text(size=16),
        plot.title=element_text(size=18))

filenoex <- file_path_sans_ext(filename)
plot1_name <- paste(filenoex,"plot_manyBreaks",sep="_")
plot2_name <- paste(filenoex,"plot_fewBreaks",sep="_")
raw_name <- paste(filenoex,"raw",sep="_") 

assign(plot1_name,plot_hist_allbreaks,envir=.GlobalEnv)
assign(plot2_name,plot_hist_1,envir=.GlobalEnv)
assign(raw_name,nums,envir=.GlobalEnv)



} 
