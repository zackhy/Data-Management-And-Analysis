"""
This program fetches Top 100 songs and their lyrics of each year from 1960 to 2014
Author: Haoyou Liu
"""
# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import csv
import re
import time

"""
CHART_URL: website for extracting lists of top 100 songs
LYRICS_URL: website for extracting lyrics for each song
HEADER: in order to avoid HTTP Error 403
"""
CHART_URL = 'http://tsort.info/music/'
LYRICS_URL = 'http://www.songlyrics.com/'
HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
# PERIODS = [1960, 1970, 1980, 1990, 2000, 2010, 2011, 2012, 2013, 2014, 2015]
start = 1960
end = 2014

"""
Get Top 100 songs using BeautifulSoup
Return a list containing tuples of (position, artist, song title, year, lyrics)

Data source: The world's Music Charts
Link: http://tsort.info/
Data Version: 2.6.0014
"""
def fetch_top_list (year):
    pos_list = []
    art_list = []
    song_list = []
    year_list = []
    top_list = []

    # if year > 2000:
    #     url = CHART_URL + 'yr' + str(year) + '.htm'
    # else:
    #     url = CHART_URL + 'ds' + str(year) + '.htm'
    url = CHART_URL + 'yr' + str(year) + '.htm'

    html_doc = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    raw_pos = soup.find_all('td', class_='pos')
    raw_art = soup.find_all('td', class_='art')
    raw_song = soup.find_all('td', class_='tit')
    raw_year = soup.find_all('td', class_='yer')

    for pos in raw_pos:
         pos_list.append(pos.string)
    for art in raw_art:
        art = art.contents[0].string
        art_list.append(art)
    for song in raw_song:
        song = song.contents[0].string
        song_list.append(song)
    for year in raw_year:
        year = year.contents[0].string
        year_list.append(year)

    for i in range(len(pos_list)):
        # Deal with exceptions
        # if art_list[i].startswith('John Fred'):
        #     art_list[i] = 'John Fred & His Playboy Band'
        # if song_list[i] == 'Those Were the Days':
        #     lyrics = get_lyrics(art_list[i], 'those where the days').encode('utf-8')

        lyrics = get_lyrics(art_list[i], song_list[i]).encode('utf-8')

        top_list.append((pos_list[i], art_list[i], song_list[i], year_list[i], lyrics))
        time.sleep(3)

    return top_list

"""
Get song lyrics using BeautifulSoup
Return the lyrics of the input song

Data source: SONGLYRICS
Link: http://www.songlyrics.com/
"""
def get_lyrics(artist, song):
    artist = artist.lower()
    song = song.lower()

    # Change the two strings to proper format in order to append them to the url
    artist = re.sub('[^A-Za-z0-9 \']+', "", artist)
    song = re.sub('[^A-Za-z0-9 \'!&/]+', "", song)
    artist = artist.replace('  ', '-').replace(' ', '-')
    song = song.replace('  ', '-').replace(' ', '-').replace("'", '-').replace('/', '-').replace('&', 'and')

    url = LYRICS_URL + artist + "/" + song + '-lyrics'

    try:
        req = urllib2.Request(url, headers=HEADER)
        content = urllib2.urlopen(req).read()
        soup = BeautifulSoup(content, 'html.parser')

        # <p> tags with the class of 'songLyricsDiv' contains the lyrics we need
        lyrics = soup.find('p', id='songLyricsDiv')
        lyrics = lyrics.get_text()

        return lyrics

    except Exception as e:
        return "Exception occurred \n" + str(e)

def main():
    # for year in PERIODS:
    #     top_list = fetch_top_list(year)
    #
    #     # Write the data to CSV files
    #     filename = 'data/list_' + str(year) + '.csv'
    #     f = open(filename, 'w')
    #     writer = csv.writer(f, lineterminator='\n')
    #     # Four columns: position, artist, song title, year, lyrics
    #     writer.writerow(['Position', 'Artist', 'Song Title', 'Year', 'Lyrics'])
    #     writer.writerows(top_list)
    #     f.close()
    #
    #     print 'list_%s successfully created' % (year,)
    year = start
    while True:
        top_list = fetch_top_list(year)

        # Write the data to CSV files
        filename = 'data/list_' + str(year) + '.csv'
        f = open(filename, 'w')
        writer = csv.writer(f, lineterminator='\n')
        # Four columns: position, artist, song title, year, lyrics
        writer.writerow(['Position', 'Artist', 'Song Title', 'Year', 'Lyrics'])
        writer.writerows(top_list)
        f.close()

        print 'list_%s successfully created' % (year,)
        year = year + 1
        if year > end:
            break

if __name__ == '__main__':
    main()
