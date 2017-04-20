"""
This program group the lyrics data by genres
Output: .txt file with all the lyrics for each genre
"""
import sqlite3

conn = sqlite3.connect('music.db')
cur = conn.cursor()

# Rock lyrics
q = 'select song_lyrics FROM Songs WHERE song_genre LIKE (?)'
cur.execute(q, ('%Rock%',))
rows = cur.fetchall()
with open('lyrics/rock.txt', 'w') as f:
    for row in rows:
        f.write(row[0].replace('\n\n', '. ').replace('\n', '. ').strip().encode('utf-8'))

# Country lyrics
q = 'select song_lyrics FROM Songs WHERE song_genre LIKE (?)'
cur.execute(q, ('%Country%',))
rows = cur.fetchall()
with open('lyrics/country.txt', 'w') as f:
    for row in rows:
        f.write(row[0].replace('\n\n', '. ').replace('\n', '. ').strip().encode('utf-8'))

# Rap lyrics
q = 'select song_lyrics FROM Songs WHERE song_genre LIKE (?)'
cur.execute(q, ('%Rap%',))
rows = cur.fetchall()
with open('lyrics/rap.txt', 'w') as f:
    for row in rows:
        f.write(row[0].replace('\n\n', '. ').replace('\n', '. ').strip().encode('utf-8'))

# Pop lyrics
q = 'select song_lyrics FROM Songs WHERE song_genre LIKE (?)'
cur.execute(q, ('%Pop%',))
rows = cur.fetchall()
with open('lyrics/pop.txt', 'w') as f:
    for row in rows:
        f.write(row[0].replace('\n\n', '. ').replace('\n', '. ').strip().encode('utf-8'))

conn.close()

