setwd("C:/Users/TF/Desktop/course/SI618/hw7")
library('data.table')
library('ggplot2')

businessdata <- read.table("businessdata_output.tsv", sep = '\t', head=TRUE, quote = "\n", comment.char = "")
businessdata$city <- as.factor(businessdata$city)
businessdata$state <- as.factor(businessdata$state)
businessdata$main_category <- as.factor(businessdata$main_category)
businessdata = na.omit(businessdata)
businessdata = data.table(businessdata)
summary(businessdata)

ggplot(businessdata, aes(x = stars, fill = state)) + geom_histogram(binwidth = 1, alpha = 0.6) + facet_grid(.~state) + ggtitle("Histograms of Star Ratings")
ggplot(businessdata, aes(x = stars, fill = state)) + aes(y = ..density..) + geom_histogram(binwidth = 1, alpha = 0.6) + facet_grid(.~state) + ggtitle("Histograms of Star Ratings")

ggplot(businessdata, aes(x = review_count)) + geom_histogram(binwidth = 10, alpha = 0.6) + ggtitle("Histograms of Review Counts") + labs(x = "Review Counts")
reviews = businessdata[businessdata$review_count <= 200]
ggplot(reviews, aes(x = review_count)) + geom_histogram(binwidth = 1, alpha = 0.6) + ggtitle("Histograms of Review Counts (Filtered)") + labs(x = "Review Counts")

ggplot(businessdata, aes(x = state, y = stars, fill = state, colour = state)) + geom_boxplot(alpha = 0.6) + ggtitle("Star Ratings by States") + labs(x = "", y = "Stars")

ggplot(businessdata, aes(x = state, y = stars, fill = state, colour = state)) + geom_jitter(alpha = 0.6) + ggtitle("Star Ratings by States") + labs(x = "", y = "Stars")

ggplot(businessdata, aes(x = reorder(state, state, function(x) -length(x)))) + geom_bar(alpha = 0.8) + labs(x = "State")

ggplot(businessdata, aes(x = stars, y = review_count, fill = state, colour = state)) + geom_jitter(alpha = 0.6) + ggtitle("Star Ratings by States") + labs(y = "Review Count")

data = businessdata[, rank := rank(-stars, ties.method = 'first'), by = .(city, main_category)]
print (data)

data = data[rank %in% 1:5 & main_category == 'Chinese', .(city, name, rank, stars)]
data = data[order(city, rank)]
print (data)

data = businessdata[, .(mean_count = mean(review_count)), by = .(state)]
ggplot(data, aes(x = reorder(state, mean_count, function(x) -x))) + aes(y = mean_count) + geom_bar(stat = "identity", alpha = 0.8) + labs(x = "State")
