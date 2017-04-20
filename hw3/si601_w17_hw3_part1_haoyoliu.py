import sqlite3 as sqlite
import json, sys

# Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

# Parse input file
with open('movie_actors_data.txt') as f:
    genre_lot = []
    movies_lot = []
    actor_lot = []
    for line in f:
        json_line = json.loads(line)
        if json_line['genres'] == []:
            continue
        for item in json_line['genres']:
            temp = (json_line['imdb_id'], item)
            genre_lot.append(temp)
        temp = (json_line['imdb_id'], json_line['title'], int(json_line['year']), float(json_line['rating']))
        movies_lot.append(temp)
        for item in json_line['actors']:
            temp = (json_line['imdb_id'], item)
            actor_lot.append(temp)

with sqlite.connect(r'hw3_part1_haoyoliu.db') as con:
    cur = con.cursor()

    # Erase existing tables
    cur.execute("DROP TABLE IF EXISTS movie_genre")
    cur.execute("DROP TABLE IF EXISTS movies")
    cur.execute("DROP TABLE IF EXISTS movie_actor")

    # Create three tables
    cur.execute('CREATE TABLE movie_genre (imdb_id text, genre text)')
    cur.executemany('INSERT INTO movie_genre VALUES (?, ?)', genre_lot)
    cur.execute('CREATE TABLE movies (imdb_id text, title text, year integer, rating real)')
    cur.executemany('INSERT INTO movies VALUES (?, ?, ?, ?)', movies_lot)
    cur.execute('CREATE TABLE movie_actor (imdb_id text, actor text)')
    cur.executemany('INSERT INTO movie_actor VALUES (?, ?)', actor_lot)

    # Find top 10 genres
    cur.execute('SELECT movie_genre.genre, Count(*) as c FROM movie_genre, movies WHERE movie_genre.imdb_id = movies.imdb_id GROUP BY movie_genre.genre ORDER BY c DESC LIMIT 0,10')
    rows = cur.fetchall()
    print 'Top 10 genres:'
    print '{}, {}'.format('Genre', 'Movies')
    for row in rows:
        print '{}, {}'.format(row[0], row[1])
    print '\n'

    # Find number of movies broken down by year
    cur.execute('SELECT year, Count(*) as c FROM movies GROUP BY year ORDER BY year')
    rows = cur.fetchall()
    print 'Movies broken down by year:'
    print '{}, {}'.format('Year', 'Movies')
    for row in rows:
        print '{}, {}'.format(row[0], row[1])
    print '\n'

    # Find all Sci-Fi movies
    cur.execute('SELECT movies.title, movies.year, movies.rating FROM movies, movie_genre WHERE movie_genre.imdb_id = movies.imdb_id AND movie_genre.genre = "Sci-Fi" ORDER BY movies.rating DESC, movies.year DESC')
    rows = cur.fetchall()
    print 'Sci-Fi movies:'
    print '{}, {}, {}'.format('Title', 'Year', 'Rating')
    for row in rows:
        print '{}, {}, {}'.format(row[0], row[1], row[2])
    print '\n'

    # Find top 10 actors
    cur.execute('SELECT movie_actor.actor as act, Count(*) as c FROM movie_actor, movies WHERE movie_actor.imdb_id = movies.imdb_id AND movies.year >= 2000 GROUP BY act ORDER BY c DESC, act LIMIT 0,10')
    rows = cur.fetchall()
    print 'In and after year 2000, top 10 actors who played in most movies:'
    print '{}, {}'.format('Actor', 'Movies')
    for row in rows:
        print '{}, {}'.format(row[0], row[1])
    print '\n'

    # Find pairs of actors who co-stared in 3 or more movies
    cur.execute('SELECT a.actor, b.actor, Count(*) as c FROM movie_actor as a INNER JOIN movie_actor as b on (a.imdb_id = b.imdb_id AND a.actor < b.actor) GROUP BY a.actor, b.actor HAVING c >= 3 ORDER BY c DESC')
    rows = cur.fetchall()
    print 'Pairs of actors who co-stared in 3 or more movies:'
    print '{}, {}, {}'.format('Actor A', 'Actor B', 'Co-stared Movies')
    for row in rows:
        print '{}, {}, {}'.format(row[0], row[1], row[2])
