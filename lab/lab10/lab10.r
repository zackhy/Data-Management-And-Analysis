setwd("C:/Users/TF/Desktop/course/SI618/lab/lab10")
pokemon <- read.table("Pokemon.csv", sep = ',', head=TRUE, quote = "\n", comment.char = "")
pokemon <- pokemon[, c("HP", "Attack", "Defense", "Sp..Atk", "Sp..Def", "Speed")]
pokemon <- scale(pokemon)
head(pokemon, 5)

withinss = list()
for (i in 1:15) {
  k = kmeans(pokemon, i)
  withinss[[i]] = k$tot.withinss
}
plot(unlist(withinss), type='b', xlab="Number of Clusters", ylab="Within groups sum of squares")

k = kmeans(pokemon, 3)
plot(Speed~Defense, col=k$cluster, data=pokemon, main="k-means clustering of Pokemon with 3 clusters")
plot(Attack~Defense, col=k$cluster, data=pokemon, main="k-means clustering of Pokemon with 3 clusters")
k = kmeans(pokemon, 2)
plot(Speed~Defense, col=k$cluster, data=pokemon, main="k-means clustering of Pokemon with 2 clusters")
plot(Attack~Defense, col=k$cluster, data=pokemon, main="k-means clustering of Pokemon with 2 clusters")