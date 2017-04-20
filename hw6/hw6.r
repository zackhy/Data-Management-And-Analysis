setwd("C:/Users/TF/Desktop/course/SI618/hw6")
countrydata <- read.table("countrydata_withregion.tsv", sep="\t", header=TRUE, quote="\"")
head(countrydata, 15)
qplot(log(countrydata$area), log(countrydata$population))
aggarea <- aggregate(countrydata$area, by=list(countrydata$region), FUN=sum)
countrydata$population <- as.numeric(countrydata$population)
aggpopu <- aggregate(countrydata$population, by=list(countrydata$region), FUN=sum)
pie(aggarea$x, labels=aggarea$Group.1, main="Area of Regions")
pie(aggpopu$x, labels=aggpopu$Group.1, main="Population of Regions")
popu_per_sqkm <- aggpopu$x/aggarea$x
popu_df <- data.frame(aggpopu$Group.1, popu_per_sqkm)
popu_df = popu_df[order(popu_df$popu_per_sqkm, decreasing=TRUE), ]
qplot(reorder(popu_df$aggpopu.Group.1, popu_df$popu_per_sqkm, function(x) -x), popu_df$popu_per_sqkm, xlab = "Region", ylab = "Population per sq km of regions") + geom_bar(stat = "identity") + theme(axis.text.x = element_text(angle = 60,hjust = 1))
Sys.getenv("PATH")
