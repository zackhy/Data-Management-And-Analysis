"""
Data pre-processing using nltk Snowball stemmer:
1. Stop words removal
2. Stemming
3. Calculate the badness score for each song
Author: Haoyou Liu
"""
from __future__ import division
import nltk
from nltk.corpus import stopwords as sw
from nltk.stem.snowball import SnowballStemmer
import sqlite3
import math

"""
Calculate the frequency of bad words.
Input must be a list of STEMMED words.
Return a 'badness' score of each song
Bad words source: https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words
"""
def badWordsDetection(sent):
    with open('bad_word_list_en', 'r') as f:
        bad_words = ''
        for word in f:
            if ' ' in word:
                continue
            bad_words += word.strip() + ' '

    # Stemming
    bad_words = nltkStemmer(bad_words)

    badness = 0
    for word in sent:
        if word in bad_words:
            badness += 1

    # Calculate badness score
    try:
        return math.log(badness/len(sent), 10) + 3
    except:
        return 0

"""
Stemmer using SnowballStemmer from nltk
Default: remove stop words
"""
def nltkStemmer(sent, stopwords=True):
    if stopwords:
        words = stopWordsRemoval(sent)
    else:
        words = nltk.word_tokenize(sent)

    sbs = SnowballStemmer("english")
    return [sbs.stem(i) for i in words]

# Remove stop words
def stopWordsRemoval(sent):
    stop_words = set(sw.words('english'))
    return [i.lower() for i in nltk.word_tokenize(sent) if i.lower() not in stop_words]

conn = sqlite3.connect('music.db')
cur = conn.cursor()

# q = 'ALTER TABLE Songs ADD badness_score REAL'
# cur.execute(q)
# conn.commit()

q = 'SELECT song_id, song_lyrics FROM Songs'
rows = cur.execute(q).fetchall()
records = []
for row in rows:
    lyrics = nltkStemmer(row[1])
    badness = badWordsDetection(lyrics)
    records.append((badness, row[0]))

q = 'UPDATE Songs SET badness_score=(?) WHERE song_id=(?)'
cur.executemany(q, records)
conn.commit()

conn.close()
