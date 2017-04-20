import sys
import sqlite3 as sqlite

# Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

# Take command line arguments
try:
    genre = sys.argv[1]
    k = sys.argv[2]
except:
    print 'Please enter genre and k'

with sqlite.connect(r'hw3_part1_haoyoliu.db') as con:
    cur = con.cursor()
    cur.execute('SELECT a.actor, COUNT(*) as c FROM movie_actor as a INNER JOIN movie_genre as b ON (a.imdb_id = b.imdb_id) WHERE b.genre = "' + genre + '"GROUP BY a.actor ORDER BY c DESC LIMIT ' + k)
    rows = cur.fetchall()
    print 'Top ' + k + ' actors who played in most ' + genre + ' movies:'
    print '{}, {}'.format('Actor', genre + ' Movies Played in')
    for row in rows:
        print '{}, {}'.format(row[0], row[1])
