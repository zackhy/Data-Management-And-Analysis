"""
This program uses brown corpus from nltk to find which words can best represent each genre
References:
    1. http://www.nltk.org/book/ch02.html
    2. http://www.degeneratestate.org/posts/2016/Apr/20/heavy-metal-and-natural-language-processing-part-1/
Author: Haoyou Liu
"""
from __future__ import division
from nltk.corpus import brown
from nltk.stem.snowball import SnowballStemmer
import nltk
import math

genres = ['rock', 'pop', 'country', 'rap']
brown_text = brown.words()

sbs = SnowballStemmer("english")

# Stemming and counting
brown_text = [sbs.stem(i.lower()) for i in brown_text]
fdist = nltk.FreqDist(w.lower() for w in brown_text)

for genre in genres:
    fname = 'lyrics/' + genre + '.txt'
    f = open(fname, 'rU')

    genre_text = ''
    for line in f:
        genre_text += line.decode('utf-8') + ' '

    genre_words = nltk.word_tokenize(genre_text)

    # Stemming and counting
    genre_words = [sbs.stem(i.lower()) for i in genre_words]
    fgenre = nltk.FreqDist(w.lower() for w in genre_words)
    result = {}
    for word in fgenre.keys():
        try:
            result[word] = math.log(fgenre[word]/fdist[word])
        except:
            pass

    sorted_result_de = sorted(result.items(), key=lambda x: x[1], reverse=True)[:100]
    sorted_result_as = sorted(result.items(), key=lambda x: x[1])[:100]


    outfname = 'lyrics/' + genre + '_rank_de' + '.txt'
    f = open(outfname, 'wb')
    for item in sorted_result_de:
        f.write(item[0] + '\t' + str(item[1]))
        f.write('\n')
    f.close()

    outfname = 'lyrics/' + genre + '_rank_as' + '.txt'
    f = open(outfname, 'wb')
    for item in sorted_result_as:
        f.write(item[0] + '\t' + str(item[1]))
        f.write('\n')

    f.close()
