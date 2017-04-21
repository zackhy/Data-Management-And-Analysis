"""
This program finds top nouns, top adjectives and top verbs in lyrics of each decades
Author: Haoyou Liu
"""
import nltk
from nltk.corpus import stopwords as sw

decades = [1960, 1970, 1980, 1990, 2000, 2010]
nouns = ['NN', 'NNS', 'NNP', 'NNPS']
JJ = ['JJ', 'JJR', 'JJS']
verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
stopwords_lst = sw.words('english')

for d in decades:
    pos_tags = {}
    pos_tags['nouns'] = {}
    pos_tags['jj'] = {}
    pos_tags['verbs'] = {}

    fname = 'lyrics/lyrics_' + str(d) + '.txt'
    f = open(fname, 'rU')

    for line in f:
        words = nltk.word_tokenize(line.lower().decode('utf-8'))
        pos = nltk.pos_tag(words)

        for item in pos:
            if item[1] in nouns:
                if item[0] in pos_tags['nouns']:
                    pos_tags['nouns'][item[0]] += 1
                else:
                    pos_tags['nouns'][item[0]] = 1

            if item[1] in JJ:
                if item[0] in pos_tags['jj']:
                    pos_tags['jj'][item[0]] += 1
                else:
                    pos_tags['jj'][item[0]] = 1

            if item[1] in verbs:
                if item[0] in pos_tags['verbs']:
                    pos_tags['verbs'][item[0]] += 1
                else:
                    pos_tags['verbs'][item[0]] = 1

    sorted_dict = {}
    for key in pos_tags.keys():
        sorted_lst = sorted(pos_tags[key].items(), key= lambda x:x[1], reverse=True)
        sorted_lst = [item for item in sorted_lst if item[0] not in stopwords_lst][:50]
        sorted_dict[key] = sorted_lst

    for key in sorted_dict.keys():
        fname = 'lyrics/' + key + '_' + str(d) + '.txt'
        f = open(fname, 'wb')
        for item in sorted_dict[key]:
            f.write(item[0] + '\t' + str(item[1]))
            f.write('\n')
        f.close()
