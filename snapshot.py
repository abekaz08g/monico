#-*- coding:utf-8 -*-

from treetagger import tag
from pymongo import Connection
from pymongo import ASCENDING

"""
connect to database and use collection "die_zeit"
"""
CON = Connection('localhost', 27017)
DB = CON[u'web']
SRCCOL = DB[u'die_zeit']


def sentence_split(ttdict):
    """
    split ttdict with pos $. into sentences
    """
    sentences = []
    startind = 0
    e_lemma = enumerate(ttdict[u'pos'])
    for item in e_lemma:
        #print item[1]
        if item[1] == u'$.':
            ind = item[0] + 1
            sentences.append({
                u'surface': ttdict[u'surface'][startind:ind],
                u'pos': ttdict[u'pos'][startind:ind],
                u'lemma': ttdict[u'lemma'][startind:ind]})
            startind = ind
        elif item[0] == len(ttdict[u'lemma']) - 1:
            sentences.append({
                u'surface': ttdict[u'surface'][startind:],
                u'pos': ttdict[u'pos'][startind:],
                u'lemma': ttdict[u'lemma'][startind:]})
    return sentences


def run(s_name):
    TRGCOL = DB[s_name]
    res = SRCCOL.find()
    for item in res:
        ttdict = tag(item[u'text'])
        sentences = sentence_split(ttdict)
        for sentence in sentences:
            sentence[u'did'] = item[u'_id']
            TRGCOL.insert(sentence)
    TRGCOL.create_index([(u'lemma', ASCENDING)])


def getSentences(s_name):
    TRGCOL = DB[s_name]
    res = TRGCOL.find({}, {u'_id': 0})
    sentences = [s for s in res]
    return sentences


def getFreqDist(snapshot, tempcol):
    TRGCOL = DB[tempcol]
    res = DB[snapshot].find({}, {u'_id': 0, u'lemma': 1})
    for item in res:
        for lemma in item[u'lemma']:
            #print lemma
            TRGCOL.update(
                {u'lemma': lemma},
                {u'$inc': {u'count': 1}},
                True)


def getFreqDistByPos(snapshot, pos, tempcol):
    TRGCOL = DB[tempcol]
    cond = {u'_id': 0, u'lemma': 1, u'pos': 1, u'surface': 1}
    res = DB[snapshot].find({}, cond)
    for item in res:
        for w in zip(item[u'lemma'], item[u'pos']):
            if w[1] == pos:
                TRGCOL.update(
                    {u'lemma': w[0]},
                    {u'$inc': {u'count': 1}},
                    True)


run('snapshot140331')
#getFreqDist(u'snapshot140331', u'lemmata2')
#getFreqDistByPos(u'snapshot140331', u'NN', u'lemmata2pos')
