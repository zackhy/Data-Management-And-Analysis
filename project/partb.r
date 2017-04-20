# Setup
setwd("C:/Users/TF/Desktop/course/SI618/project")
library(DBI)
library(RSQLite)
library(data.table)
library(ggplot2)
library(gridExtra)

sqlite <- dbDriver("SQLite")
musicdb <- dbConnect(sqlite, "music.db")
music <- dbGetQuery(musicdb, "select * from songs")
songs <- na.omit(music)
songs <- data.table(songs)
songs$song_genre <- as.factor(songs$song_genre)

songs[, mean(as.numeric(song_length)), by=year]

avg_length <-songs[, .(mean=mean(as.numeric(song_length))), by=year]
avg_length_genre <- songs[, .(mean=mean(as.numeric(song_length))), by=.(year, song_genre)]
ggplot() + geom_smooth(data=avg_length, aes(x=year, y=mean), colour='blue', size=2) + geom_line(data=subset(avg_length_genre, song_genre==c('Rock', 'Hip-Hop/Rap', 'Country', 'Pop')), aes(x=year, y=mean, col=song_genre), size=1) + labs(x='Year', y='Song Length (Miliseconds)') + ggtitle('Average song length')

songs$count <- sapply(songs$song_lyrics, function(x) length(unlist(strsplit(as.character(x), "\\W+"))))
words_count <- songs[, .(mean=mean(count)), by=year]
words_count_genre <- songs[, .(mean=mean(count)), by=.(year, song_genre)]
ggplot() + geom_smooth(data=words_count, aes(x=year, y=mean), size=2) + geom_line(data=subset(words_count_genre, song_genre==c('Rock', 'Hip-Hop/Rap', 'Country', 'Pop')), aes(x=year, y=mean, col=song_genre), size=1) + labs(x='Year', y='Lyrics Length') + ggtitle('Average lyrics length')

songs$per <- as.numeric(songs$count)/as.numeric(songs$song_length)
words_per_sec <- songs[, .(mean=mean(per)), by=year]
words_per_sec_genre <- songs[, .(mean=mean(per)), by=.(year, song_genre)]
ggplot() + geom_smooth(data=words_per_sec, aes(x=year, y=mean), size=2) + geom_line(data=subset(words_per_sec_genre, song_genre==c('Rock', 'Hip-Hop/Rap', 'Country', 'Pop')), aes(x=year, y=mean, col=song_genre), size=1) + labs(x='Year', y='Average Words per Milisecond') + ggtitle('Average words per miliseconds')

music <- data.table(music)
avg_badness <- music[, .(mean=mean(badness_score)), by=year]
avg_badness_genre <- music[, .(mean=mean(badness_score)), by=.(year, song_genre)]
point = ggplot(data=music, aes(x=year, y=badness_score, col=song_genre, width = 0.25)) + geom_jitter() + ggtitle('Badness Score') + guides(colour=FALSE) + labs(x='Year', y="Badness Score")
line = ggplot(data=avg_badness, aes(x=year, y=mean)) + geom_smooth() + geom_point() + labs(x='Year', y="Average Badness") + ggtitle('Average Badness score')
grid.arrange(point, line, ncol=2, top = "How Badness Changed Over Time")

data <- read.csv('avg_badness.csv')
rnames <- data[,1]
heatmap_data <- data.matrix(data[,2:ncol(data)])
head(heatmap_data)
rownames(heatmap_data) <- rnames
heatmap_data <- heatmap_data[c('Rock', 'Hip-Hop/Rap', 'Country', 'Pop', 'Soundtrack', 'R&B/Soul'), ]

my_palette <- colorRampPalette(c("#0094E5", "#0071C8", "#004CAA", "#00278C", "#01026F"))

library(gplots)
heatmap.2(heatmap_data,
          col=my_palette,
          density.info="none",  
          trace="none",
          dendrogram="none", 
          Colv="NA",
          Rowv="NA",
          labCol=unique(music$year),
          key.par=list(mar=c(5,0,3,0)),
          key.xlab = "badness",
          margins=c(3,0),
          symkey=FALSE,
          symbreaks=FALSE,
          lmat=rbind(c(5, 4, 2), c(6, 1, 3)), lhei=c(1.5, 5), lwid=c(1, 10, 1))

artist <- dbGetQuery(musicdb, "select artist_name, song_name, badness_score from songs JOIN artists ON songs.artist_id=artists.artist_id")
artist = data.table(artist)
head(artist)

badness_artist_mean = artist[, mean(badness_score), by=artist_name]
badness_artist_sum = artist[, sum(badness_score), by=artist_name]
sorted_artist_mean = badness_artist_mean[order(-V1)]
sorted_artist_sum = badness_artist_sum[order(-V1)]
sorted_artist_mean = sorted_artist_mean[c(1:20), ]
sorted_artist_sum = sorted_artist_sum[c(1:20), ]

art_plot_mean = ggplot(sorted_artist_mean, aes(x=reorder(artist_name, V1, function(x) -x), y=V1)) + geom_bar(stat="identity") + labs(x="Artist Name", y="Badness") + theme(axis.text.x = element_text(angle = 60,hjust = 1)) + ggtitle('Mean')
art_plot_sum = ggplot(sorted_artist_sum, aes(x=reorder(artist_name, V1, function(x) -x), y=V1)) + geom_bar(stat="identity") + labs(x="Artist Name", y="Badness") + theme(axis.text.x = element_text(angle = 60,hjust = 1)) + ggtitle('Sum')
grid.arrange(art_plot_mean, art_plot_sum, ncol=2, top = "Bad Artists")

sorted_songs = artist[order(-badness_score)][c(1:20)]
ggplot(sorted_songs, aes(x=reorder(song_name, badness_score, function(x) -x), y=badness_score)) + geom_bar(stat="identity") + labs(x="Song Name", y="Badness") + theme(axis.text.x = element_text(angle = 60,hjust = 1)) + ggtitle('Bad Songs')
