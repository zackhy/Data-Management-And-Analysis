setwd("C:/Users/TF/Desktop/course/SI618/hw10")

cars <- read.table("cars.tsv", sep = '\t', head=TRUE, quote = "\n", comment.char = "")
cars.data <- cars[, c(3:8)]
rownames(cars.data) <- cars$Car
cars.data <- scale(cars.data)
head(cars.data, 5)

cars.dist = dist(cars.data)
as.matrix(cars.dist)[1:5, 1:5]

cars.hclust <- hclust(cars.dist, method = "average")
plot(cars.hclust,labels=cars$Car,main='Hierarchical cluster analysis using average linkage')
rect.hclust(cars.hclust, k=3)

groups.3 = cutree(cars.hclust, k=3)
groups.3

table(groups.3)
table(groups.3, cars$Country)
aggregate(cars[, c(3:8)], by=list(groups.3), FUN=median)

library(gplots)
heatmap.2(as.matrix(cars.data), 
          hclustfun = function(x) hclust(x, method = "average"),
          dendrogram="row", 
          scale="column", 
          density.info="none", 
          col=redblue(256), 
          trace="none", 
          margins=c(5, 8), 
          cexRow=0.7, 
          cexCol=0.7)

library(cluster)
cars.pam = pam(cars.dist, 3)
all(cars.pam$clustering == groups.3)
cars.pam$medoids

clusplot(cars.pam, labels=2)

si <- silhouette(cars.pam)
plot(si)
