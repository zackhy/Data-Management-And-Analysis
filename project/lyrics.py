"""
This program figures out how lyrics changed in past decades by calculating the frequencies and tf-idf weights of words.
"""
# -*- coding: utf-8 -*-
from __future__ import division
import nltk
import re
import csv
import math

def stopwords_removal(lyrics, stopwords):
    result = []

    words = nltk.word_tokenize(lyrics)
    for word in words:
        if word.lower() not in stopwords and not re.match(r'.*\W.*', word):
            result.append(word.lower())

    return result

def frequency_count(lyrics):
    result = {}
    for word in lyrics:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1

    result = sorted(result.items(), key=lambda x: x[1], reverse=True)

    return result

def tf_idf_caculator(word_freq):
    doc_num = len(word_freq)
    doc_freq = {}
    result = {}
    for words_list in word_freq.values():
        for word in words_list:
            if word[0] in doc_freq:
                doc_freq[word[0]] += 1
            else:
                doc_freq[word[0]] = 1

    for key, value in word_freq.items():
        tf_idf = {}
        for word, freq in value:
            tf = math.log(freq + 1)
            idf = math.log(doc_num/doc_freq[word]) + 1
            tf_idf[word] = tf*idf

        tf_idf = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
        result[key] = tf_idf

    return result


def main():
    with open('stopwords_en.txt', 'r') as f:
        stopwords = []
        for word in f:
            stopwords.append(word.strip().encode('utf-8'))

    periods = [1960, 1970, 1980, 1990, 2000, 2010, 2011, 2012, 2013, 2014]
    lyrics_freq_dict = {}

    for year in periods:
        filename = 'data/list_' + str(year) + '.csv'
        with open(filename, 'r') as csvfile:
            next(csvfile)
            csvreader = csv.reader(csvfile)

            lyrics = ''
            for row in csvreader:
                lyr = row[4].replace('\n\n', '. ').replace('\n', '. ').decode('utf-8')
                if lyr.startswith('Exception'):
                    continue
                else:
                    lyrics += lyr

        lyrics = stopwords_removal(lyrics, stopwords)
        lyrics = frequency_count(lyrics)

        lyrics_freq_dict[year] = lyrics

    temp = {}
    for year in periods[5:]:
        for word, freq in lyrics_freq_dict[year]:
            if word in temp:
                temp[word] += freq
            else:
                temp[word] = freq

        del lyrics_freq_dict[year]

    lyrics_freq_dict[2010] = sorted(temp.items(), key=lambda x: x[1], reverse=True)

    lyrics_tf_idf_dict = tf_idf_caculator(lyrics_freq_dict)

    for year in periods[:6]:

        freq_file = 'result/frequency_' + str(year) + '.txt'
        with open(freq_file, 'w') as f:
            f.write('{}\t{}\n'.format('words', 'frequency'))
            count = 1
            for word, freq in lyrics_freq_dict[year]:
                outstr = '{}\t{}\n'.format(word, freq)
                f.write(outstr)

                count += 1
                if count == 100:
                    break

        tfidf_file = 'result/tfidf_' + str(year) + '.txt'
        with open(tfidf_file, 'w') as f:
            f.write('{}\t{}\n'.format('words', 'tf-idf'))
            count = 1
            for word, tfidf in lyrics_tf_idf_dict[year]:
                outstr = '{}\t{}\n'.format(word, tfidf)
                f.write(outstr)

                count += 1
                if count == 100:
                    break

if __name__ == '__main__':
    main()
