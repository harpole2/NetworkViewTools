PathDistanceExtraction <- function(directory, filename, residue1, residue2) {

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

end<-grepl("Number", lines)
start<-grepl("The final", lines)

for (i in 1:length(lines)) {
  if (start[i]==TRUE){
    start_num=i
  }
  if (end[i]==TRUE){
    end_num=i
  }
}

lines_cut <-lines[(start_num+1):(end_num-1)]

pair_1<-residue1
pair_2<-residue2

matches1 <- grepl(pair_1,lines_cut)
matches2 <- grepl(pair_2,lines_cut)

nums=as.numeric(nums)
#nums=as.factor(nums)
#help set plot limits and total number of paths at each distance
stats<-count(nums)
top<-max(stats$freq)

#get pair freqency in each path
pair_length<-nums[matches1==TRUE&matches2==TRUE]
stats_pairs<-count(pair_length)

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
all_paths<- paste(filenoex,"all_paths", sep="_")
pairs <- paste(filenoex,pair_1,pair_2,"content",sep="_") 

assign(plot1_name,plot_hist_allbreaks,envir=.GlobalEnv)
assign(plot2_name,plot_hist_1,envir=.GlobalEnv)
assign(raw_name,nums,envir=.GlobalEnv)
assign(all_paths,stats,envir=.GlobalEnv)
assign(pairs,stats_pairs,envir=.GlobalEnv)






} 
