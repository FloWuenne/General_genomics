## Plot Superlink results from parsed html output

## Import libraries
library(ggplot2)
library(tidyr)
library(dplyr)

setwd("/media/florian/CCE45F70E45F5C30/Florian_Projects/NEW_Genotyping_Analysis_2015/Family1524/NOTCH1_subpedigree_analysis")

## Import data
superlink_results <- read.table("All_chromosomes_SUPERLINK.cleaned.tab",sep="\t",header=T)

## Restructure data using tidyR
superlink_results <- superlink_results %>%
  spread(variable,value)

superlink_results <- superlink_results %>%
  mutate(LOD = as.numeric(as.character(LOD))) %>%
  mutate(distance = as.numeric(as.character(distance))) %>%
  mutate(NPLALL = as.numeric(as.character(NPLALL))) %>%
  mutate(NPLSPAIR = as.numeric(as.character(NPLSPAIR))) %>%
  mutate(chrom= gsub("_"," ",chrom))


## Subset data
## Get all markers with LOD score > 2
lod_bigger_1.5 <- subset(superlink_results,LOD>1.5)

## Plot data
## LOD score for all chromosomes
LOD_plot <- ggplot(superlink_results,aes(x=distance,y=LOD)) +
  geom_line(aes(group=chrom,color= LOD > 1.5)) +
  scale_y_continuous("LOD score",breaks=c(-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10)) +
  scale_x_continuous("Distance (cM)") +
  geom_hline(yintercept=3,col="red") +
  facet_wrap(~chrom, scales="free") +
  scale_color_manual(values=c("FALSE"="black","TRUE"="red")) +
  theme_Publication()
ggsave(file="LOD_score_plot_Family1524_NOTCH1.svg",plot=LOD_plot,width=30,height=15)


## NPLALL score for all chromosomes
NPLALL_plot <- ggplot(superlink_results,aes(x=distance,y=NPLALL)) +
  geom_line(aes(group=chrom,color= NPLALL > 3)) +
  scale_y_continuous("LOD score",breaks=c(-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10)) +
  scale_x_continuous("Distance (cM)") +
  geom_hline(yintercept=3,col="red") +
  facet_wrap(~chrom, scales="free") +
  scale_color_manual(values=c("FALSE"="black","TRUE"="red")) +
  theme_Publication()
ggsave(file="NPLALL_score_plot_Family1524_NOTCH1.svg",plot=NPLALL_plot,width=30,height=15)

## NPLSPAIR score for all chromosomes
NPLSPAIR_plot <- ggplot(superlink_results,aes(x=distance,y=NPLSPAIR)) +
  geom_line(aes(group=chrom,color= NPLSPAIR > 3)) +
  scale_y_continuous("LOD score",breaks=c(-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10)) +
  scale_x_continuous("Distance (cM)") +
  geom_hline(yintercept=3,col="red") +
  facet_wrap(~chrom, scales="free") +
  scale_color_manual(values=c("FALSE"="black","TRUE"="red")) +
  theme_Publication()
ggsave(file="NPLSPAIR_score_plot_Family1524_NOTCH1.svg",plot=NPLSPAIR_plot,width=30,height=15)

## Genome wide plot in one plot
LOD_plot <- ggplot(superlink_results,aes(x=distance,y=LOD)) +
  geom_line(aes(group=chrom,color= LOD > 1.5)) +
  scale_y_continuous("LOD score",breaks=c(-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10)) +
  scale_x_continuous("Distance (cM)") +
  geom_hline(yintercept=3,col="red") +
  facet_grid(.~chrom) +
  scale_color_manual(values=c("FALSE"="black","TRUE"="red")) +
  theme_Publication()