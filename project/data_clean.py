"""
This program deals with missing lyrics
"""
import sqlite3

conn = sqlite3.connect('music.db')
cur = conn.cursor()

q = 'select song_id, song_lyrics FROM Songs'
cur.execute(q)
rows = cur.fetchall()

record = []
for row in rows:
    if row[1].startswith("Exception") or row[1].startswith("We do not have"):
        record.append(('NA', row[0]))

q = 'Update Songs SET song_lyrics=(?) WHERE song_id=(?)'
cur.executemany(q, record)

conn.commit()
conn.close()

