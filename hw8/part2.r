setwd("C:/Users/TF/Desktop/course/SI618/hw8")
library(DBI)
library(RSQLite)
library(data.table)
library(ggplot2)

sqlite <- dbDriver("SQLite")
vehiclesdb <- dbConnect(sqlite, "vehicles.db")
vehicles <- dbGetQuery(vehiclesdb, "select * from vehicles")
head(vehicles, n=10)
summary(vehicles)

vehicles$make <- as.factor(vehicles$make)
vehicles$vclass <- as.factor(vehicles$vclass)
vehicles$cylinders <- as.factor(vehicles$cylinders)
vehicles$trany <- as.factor(vehicles$trany)
summary(vehicles)

vehicles <- data.table(vehicles)
vehicles[, length := .N, by = vclass]
vehicles <- subset(vehicles, length > 40)
print(vehicles)
vehicles[, length := NULL]
print(vehicles)
summary(vehicles)

class = unique(vehicles$vclass)
for (vc in class) {
  sub <- subset(vehicles, vclass==vc)
  data1 <- sub[, mpg := mean(combo08), by = c("year", "make")]
  lineplot <- ggplot(data1, aes(year, mpg), fig.width = 16) + geom_line(aes(colour = make)) + guides(col = guide_legend(ncol=2)) + ggtitle(vc) + labs(x = "Year", y = "Mean combined MPG")
  print(lineplot)

  data2 <- sub[, c("make", "combo08")][, mpg := mean(combo08), by = make][, combo08 := NULL]
  data2 <- unique(data2)
  barplot = ggplot(data2, aes(x = reorder(make, mpg, function(x) -x)), fig.width = 16) + aes(y = mpg) + geom_bar(stat = "identity", alpha = 0.8) + ggtitle(vc) + labs(x = "", y = "Mean combined MPG in All Years") + theme(axis.text.x = element_text(angle = 60,hjust = 1))
  print(barplot)
}