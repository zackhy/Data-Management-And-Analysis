"""
This program insert the data from part-a and iTunes Search API into database.
iTunes Search API rate limit: 20 calls per minute
"""
import sqlite3
import csv
import requests
import json
import time

conn = sqlite3.connect('music.db')
cur = conn.cursor()

HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

cur.execute('DELETE FROM Artists')
cur.execute('DELETE FROM Songs')

# Insert data into Artists
artists = []
for year in range(1960, 2015):
    fname = 'data/list_' + str(year) + '.csv'
    f = open(fname)
    incsv = csv.reader(f)
    next(incsv)

    for line in incsv:
        if (line[1], ) not in artists:
            artists.append((line[1], ))

f.close()

q = 'INSERT INTO Artists (artist_name) Values (?)'
cur.executemany(q, artists)

conn.commit()

# Insert data into Songs
songs = []
for year in range(1960, 2015):
    fname = 'data/list_' + str(year) + '.csv'
    f = open(fname)
    incsv = csv.reader(f)
    next(incsv)

    for line in incsv:
        q = 'SELECT artist_id FROM Artists WHERE artist_name=?'
        cur.execute(q, (line[1], ))
        artist_id = cur.fetchone()[0]
        songs.append((int(line[0]),  # Position
                      line[2],  # Song title
                      int(line[3]),  # Year
                      line[4].decode('utf-8'),  # Lyrics
                      artist_id))  # Artist ID

f.close()

q = 'INSERT INTO Songs (position, song_name, year, song_lyrics, artist_id) VALUES (?, ?, ?, ?, ?)'
cur.executemany(q, songs)

conn.commit()

# Test
# q = 'SELECT artist_name FROM Artists JOIN Songs ON Artists.artist_id = Songs.artist_id WHERE song_name="See You Again"'
# cur.execute(q)
# print cur.fetchone()[0]

q = 'SELECT song_id, song_name, artist_name FROM Songs '
q += 'JOIN Artists ON Songs.artist_id = Artists.artist_id'
cur.execute(q)
rows = cur.fetchall()
# print rows

# Gather data using iTunes search API and insert the data into Songs
# Rate limit: 20 calls per minute
def insert_new(rows):
    base_url = 'https://itunes.apple.com/search'
    records = []
    for row in rows:
        time.sleep(5)
        song_name = row[1].replace(' ', '+')
        parameters = {'term': song_name, 'entity': 'song'}
        try:
            response = requests.get(base_url, params=parameters, headers=HEADER)
            # if response.status_code == 403:
            #     print 'no!!!!!'
            # else:
            #     print 'yes'
            result = json.loads(response.text)
        except:
            continue

        for item in result['results']:
            if row[2] in item['artistName']:
                record = (item['primaryGenreName'],  # Genre
                          item['trackTimeMillis'],  # Song length
                          item['country'],  # Song country
                          row[1])  # Song name
                records.append(record)
                # print record
                break
    q = 'UPDATE Songs SET song_genre=(?), song_length=(?), song_country=(?) WHERE song_name=(?)'
    cur.executemany(q, records)
    conn.commit()

flag = 0
while True:
    insert_new(rows[flag: flag+100])
    flag = flag + 100
    if flag == 5500:
        break

conn.close()
