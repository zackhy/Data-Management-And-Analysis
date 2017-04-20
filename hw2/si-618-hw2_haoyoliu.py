from bs4 import BeautifulSoup
import json, urllib2
import re
import time
import pydot, itertools
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# Step 1
with open('step1.html', 'w') as f1:
    html_doc = urllib2.urlopen('http://www.imdb.com/search/title?at=0&sort=num_votes&count=100').read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    f1.write(soup.encode('utf-8'))

# Step 2
with open('step2.txt', 'w') as f2:
    f2.write('{}\t{}\t{}\n'.format('IMDB_ID', 'Rank', 'Title'))
    id_list = []
    for movie in soup.findAll('h3', class_='lister-item-header'):
        link = movie.a.get('href')
        id = re.findall(r'(tt\d{7})', link)[0]
        id_list.append(id)
        rank = movie.findAll('span')[0].string.replace('.', '')
        title = movie.a.string
        # Got an UnicodeEncodeError from the line below. Wondering why
        outstr = '{}\t{}\t{}\n'.format(id, rank, title)
        f2.write(outstr)

# Step 3
# with open('step3.txt', 'w') as f3:
#     for item in id_list:
#         url = 'http://www.omdbapi.com/?i=' + item
#         omdb_doc = urllib2.urlopen(url).read().decode('utf-8')
#         f3.write(omdb_doc.encode('utf-8') + '\n')
#         time.sleep(5)

# Step 4
with open('step3.txt', 'rU') as f4:
    with open('step4.txt', 'w') as f5:
        for line in f4:
            json_data = json.loads(line)
            movie_name = json_data['Title']
            json_list = json_data['Actors'].split(', ')[:5]
            actor_list = json.dumps(json_list)
            outstr = '{}\t{}\n'.format(movie_name, str(actor_list))
            f5.write(outstr)

# Step 5
with open('step4.txt', 'rU') as f6:
    graph = pydot.Dot(graph_type='graph', charset="utf8")
    for line in f6:
        # actors = line.split('\t')[1].replace(']','').replace('[','')
        # actors_list = actors.replace('\n', '').split(', ')
        # # print actors_list
        # for i in itertools.combinations(actors_list, 2):
        #     edge = pydot.Edge(i[0], i[1])
        #     graph.add_edge(edge)

        # Why this could not work?
        actors = line.split('\t')[1]
        json_actors = json.loads(actors)
        for i in itertools.combinations(json_actors, 2):
            edge = pydot.Edge(i[0].decode('gbk'), i[1].decode('gbk'))
            graph.add_edge(edge)

graph.write('actors_graph_output.dot')
