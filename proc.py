#-*- coding:utf-8 -*-

import xmltodict
from pymongo import MongoClient
import urllib
import tools


def storeRSS(rssurl, category, collection):
    """
    rss: rss string
    collection: pymongo collection
    category: rss article category
    void
    """
    f = urllib.urlopen(rssurl)
    rss = f.read()
    f.close()
    rssdict = xmltodict.parse(rss)
    rssdict[u'category'] = category
    collection.insert(rssdict)


def readRSS(collection):
    """
    collection: pymongo collection
    returns rss string and category tuple list
    """
    res = collection.find()
    rsscol = []
    for item in res:
        rssdict = {u'rss': item[u'rss']}
        rss = xmltodict.unparse(rssdict)
        rsscol.append((item[u'category'], rss))
    return rsscol


def storeDocs(rssurl, category, doccol, sentcol):
    links = tools.parseRss(rssurl)
    for link in links:
        articleHtml = tools.getArticle(link)
        articleText = tools.parseArticle(articleHtml)
        antText = tools.treetagger(articleText)
        sentences = tools.textToSentences(antText)
        if doccol.find({u'url': link}).count() == 1:
            pass
        else:
            for sentence in sentences:
                sentence[u'url'] = link
                sentcol.insert(sentence)
            doccol.update(
                {u'url': link},
                {u'$addToSet': {u'category': category}}
            )


class database:
    def __init__(self, dbconf):
        self.host = dbconf[u'host']
        self.port = dbconf[u'port']
        self.dbname = dbconf[u'dbname']
        self.maincolname = dbconf[u'maincolname']
        self.doccolname = dbconf[u'doccolname']
        self.rsscolname = dbconf[u'rsscolname']
        self.rssdict = dbconf[u'rssdict']

    def connect(self):
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.dbname]
        self.rsscol = self.db[self.rsscolname]
        self.col = self.db[self.maincolname]
        self.doccol = self.db[self.doccolname]

    def disconnect(self):
        self.client.close()

    def fetchArticles(self):
        for category in self.rssdict:
            rssurl = self.rssdict[category]
            storeRSS(rssurl, category, self.rsscol)
            storeDocs(rssurl, category, self.doccol, self.col)
