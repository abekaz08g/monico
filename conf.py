#-*- coding:utf-8 -*-


RSSDICT = {
    """
    list of RSS in "Die Zeit"
    """
    u'Startseite': 'http://newsfeed.zeit.de/index',
    u'Politik': 'http://newsfeed.zeit.de/politik/index',
    u'Wirtschaft': 'http://newsfeed.zeit.de/wirtschaft/index'
}


DBCONF = {
    u'host': u'localhost',
    u'port': 27017,
    u'dbname': u'web',
    u'maincolname': u'dzeit',
    u'doccolname': u'dzeit.docs',
    u'rsscolname': u'dzeit.rss',
    u'rssdict': RSSDICT
}
