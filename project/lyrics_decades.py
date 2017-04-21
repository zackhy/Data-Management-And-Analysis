"""
This program group the lyrics data by decades
Output: txt files with all the lyrics for each decade
Author: Haoyou Liu
"""
import sqlite3

conn = sqlite3.connect('music.db')
cur = conn.cursor()

# Extract lyrics from database
def get_lyrics(start_year, end_year):
    q = 'SELECT song_lyrics, year FROM Songs'
    cur.execute(q)
    rows = cur.fetchall()
    result = []
    for row in rows:
        if (int(row[1]) < start_year or int(row[1]) > end_year) \
                or row[0] == 'NA':  # Ignore missing lyrics
            continue
        else:
            result.append(row[0])
    return result

interval = 10
start_year = 1959
lyrics_dic = {}
while True:
    lyrics = get_lyrics(start_year, start_year+interval)
    fname = 'lyrics/lyrics_' + str(start_year + 1) + '.txt'
    f = open(fname, 'wb')
    for line in lyrics:
        f.write(line.replace('\n\n', '. ').replace('\n', '. ').strip().encode('utf-8'))
    f.close()
    start_year += 10
    if start_year >= 2019:
        break
