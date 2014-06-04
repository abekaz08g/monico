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


def run(s_name, label=None):
    TRGCOL = DB[s_name]
    if labels is None:
        print 1
        res = SRCCOL.find()
    else:
        res = SRCCOL.find({u'labels': label})
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


labels = [
    u'Politik',
    u'Wirtschaft',
    u'Meinung',
    u'Gesellschaft',
    u'Kultur',
    u'Wissen',
    u'Digital',
    u'Studium',
    u'Karriere',
    u'Lebensart',
    u'Reisen',
    u'Auto',
    u'Sport'
]

lemmata = []
res = DB[u'Politik.fd'].find({}, {u'_id': 0, u'lemma': 1})
lemmata.extend([item[u'lemma'] for item in res])
lemmata = set(lemmata)
#print lemmata
for la in labels:
    #run(la, label=la)
    #getFreqDist(la, u'%s.fd' % la)
    """
    getFreqDistByPos(la, u'NN', u'%s.fd.NN' % la)
    getFreqDistByPos(la, u'VVFIN', u'%s.fd.VV' % la)
    getFreqDistByPos(la, u'VVPP', u'%s.fd.VV' % la)
    getFreqDistByPos(la, u'VVINF', u'%s.fd.VV' % la)
    getFreqDistByPos(la, u'VVIZU', u'%s.fd.VV' % la)
    getFreqDistByPos(la, u'VVINP', u'%s.fd.VV' % la)
    getFreqDistByPos(la, u'ADJA', u'%s.fd.ADJ' % la)
    getFreqDistByPos(la, u'ADJD', u'%s.fd.ADJ' % la)
    getFreqDistByPos(la, u'ADV', u'%s.fd.ADV' % la)
    """
    curlemmata = []
    res = DB[u'%s.fd' % la].find({}, {u'_id': 0, u'lemma': 1})
    curlemmata.extend([item[u'lemma'] for item in res])
    lemmata = lemmata & set(curlemmata)
    lemmatafd = []
    for lemma in lemmata:
        res = DB[u'fd'].find_one({u'lemma': lemma}, {u'_id': 0, u'count': 1})
        freq = res[u'count']
        lemmatafd.append((freq, lemma))
lemmatafd = sorted(lemmatafd)
lemmatafd.reverse()
fout = open('colemmata.txt', 'w')
cont = [u'%s (%d)' % (l[1], l[0]) for l in lemmatafd]
fout.write(u', '.join(cont).encode('UTF-8'))
fout.close()
pos = [u'NN', u'VV', u'ADJ', u'ADV']
p_lemmata = {}

for p in pos:
    print p
    for la in labels:
        curlemmata = []
        res = DB[u'%s.fd.%s' % (la, p)].find({}, {u'_id': 0, u'lemma': 1})
        curlemmata.extend([item[u'lemma'] for item in res])
        #lemmata = lemmata & set(curlemmata)
        lemmatafd = []
        cond = {u'_id': 0, u'count': 1}
        for lemma in curlemmata:
            res = DB[u'%s.fd.%s' % (la, p)].find_one({u'lemma': lemma}, cond)
            freq = res[u'count']
            lemmatafd.append((freq, lemma))
        lemmatafd = sorted(lemmatafd)
        lemmatafd.reverse()
        fout = open('lemmata_%s_%s.txt' % (p, la), 'w')
        cont = [u'%s (%d)' % (l[1], l[0]) for l in lemmatafd[:100]]
        fout.write(u', '.join(cont).encode('UTF-8'))
        fout.close()



#run('snapshot140331')
#getFreqDist(u'snapshot140331', u'lemmata2')
#getFreqDistByPos(u'snapshot140331', u'NN', u'lemmata2pos')
