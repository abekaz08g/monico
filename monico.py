#-*- coding:utf-8 -*-

import feedparser
import urllib
from pymongo import Connection
from bs4 import BeautifulSoup

RSS = {
    """
    list of RSS in "Die Zeit"
    """
    u'Startseite': 'http://newsfeed.zeit.de/index',
    u'Politik': 'http://newsfeed.zeit.de/politik/index',
    u'Wirtschaft': 'http://newsfeed.zeit.de/wirtschaft/index',
    u'Meinung': 'http://newsfeed.zeit.de/meinung/index',
    u'Gesellschaft': 'http://newsfeed.zeit.de/gesellschaft/index',
    u'Kultur': 'http://newsfeed.zeit.de/kultur/index',
    u'Wissen': 'http://newsfeed.zeit.de/wissen/index',
    u'Digital': 'http://newsfeed.zeit.de/digital/index',
    u'Studium': 'http://newsfeed.zeit.de/studium/index',
    u'Karriere': 'http://newsfeed.zeit.de/karriere/index',
    u'Lebensart': 'http://newsfeed.zeit.de/lebensart/index',
    u'Reisen': 'http://newsfeed.zeit.de/reisen/index',
    u'Auto': 'http://newsfeed.zeit.de/auto/index',
    u'Sport': 'http://newsfeed.zeit.de/sport/index',
}

"""
connect to database and use collection "die_zeit"
"""
CON = Connection('localhost', 27017)
DB = CON[u'web']
COL = DB[u'die_zeit']


def parseRss(url):
    """
    using feedparser (https://pypi.python.org/pypi/feedparser)
    extract links from entries

    """
    rss = feedparser.parse(url)
    links = []
    for entry in rss['entries']:
        links.append(entry['link'])
    return links


def parseZeit(artikel):
    """
    is used in dlinks.
    using bs4(http://bit.ly/1h4ptBE)
    extract texts in <div id="main">
    """
    soup = BeautifulSoup(artikel)
    text = ''
    for div in soup.find_all('div'):
        if div.has_attr('class') and div['class'] == [u'article-body']:
            #print div['class']
            #if div.has_attr('class') and div['class'] == u'article-body':
            text += div.get_text()
    return text


def dlLinks(links, labels=[], parser=None, suffix=None):
    """
    links: urls extracted from RSS
    labels: category of the article
    parser: specific parser
    suffix: additional string attached to url
    1) check the url reduplication in db collection
    2) create dictionary type data
    3) store the data into database
    """
    for link in links:
        if COL.find({u'url': link}).count() == 0:
            f = urllib.urlopen(link + suffix)
            cont = f.read()
            f.close()
        if parser is not None:
            param = {}
            param[u'url'] = link
            param[u'labels'] = labels
            param[u'page'] = cont.decode('UTF-8')
            param[u'text'] = parser(cont.decode('UTF-8'))
            COL.insert(param)
        else:
            param = {}
            param[u'url'] = link
            param[u'labels'] = labels
            param[u'page'] = cont.decode('UTF-8')
            COL.insert(param)
    else:
        pass


if __name__ == '__main__':
    """
    main part of the program
    """
    for r in RSS.keys():
        links = parseRss(RSS[r])
        sfx = '/komplettansicht?print=true'
        lbs = [u'die_zeit', r]
        dlLinks(links, labels=lbs, parser=parseZeit, suffix=sfx)
