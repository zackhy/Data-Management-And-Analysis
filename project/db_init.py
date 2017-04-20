"""
This program creates an one-to-many database that contains two tables: artists and songs.
Artists: artist_id, artist_name, gender, artist_genre, artist_country
Songs: song_id, song_name, song_lyrics, song_genre, song_length, year, position, artist_id
"""
import sqlite3

conn = sqlite3.connect('music.db')
cur = conn.cursor()

# Database initialization
cur.execute("DROP TABLE IF EXISTS Songs")
cur.execute("DROP TABLE IF EXISTS Artists")

# Table artists
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Artists (' \
             'artist_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
             'artist_name TEXT,' \
             'gender TEXT,' \
             'artist_genre TEXT,' \
             'artist_country TEXT)'
cur.execute(statement)

# Table songs
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Songs (' \
             'song_id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
             'song_name TEXT, ' \
             'song_lyrics TEXT, ' \
             'song_genre TEXT, ' \
             'song_length TEXT, ' \
             'year INTEGER, ' \
             'position INTEGER, ' \
             'artist_id INTEGER, ' \
             'song_country TEXT, ' \
             'FOREIGN KEY (artist_id) REFERENCES Artists(artist_id))'
cur.execute(statement)

conn.commit()
