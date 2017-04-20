"""
This program extracts topics from lyrics using sklearn
"""
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation
import sqlite3

n_topics = 1
n_top_words = 30
n_features = 2000

conn = sqlite3.connect('music.db')
cur = conn.cursor()

q = 'SELECT song_lyrics, year FROM Songs'
cur.execute(q)
rows = cur.fetchall()

def get_lyrics(rows, start_year, end_year):
    result = []
    for row in rows:
        if int(row[1]) < start_year or int(row[1]) > end_year:
            continue
        else:
            result.append(row[0])
    return result

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

result = get_lyrics(rows, 2009, 2015)

tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features, stop_words='english')
tfidf_vectorizer = TfidfTransformer()
tf = tf_vectorizer.fit_transform(result)
tfidf = tfidf_vectorizer.fit_transform(tf)
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
lda.fit(tfidf)
print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)
