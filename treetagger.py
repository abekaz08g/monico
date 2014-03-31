# -*- coding:utf-8 -*-
import os


def tag(inp):
    fin = u'.tgin'
    fout = open(fin, 'w')
    fout.write(inp.encode('utf-8'))
    fout.close()
    os.popen(u'tree-tagger-german-utf8 .tgin >> .tgout')
    f = open(u'.tgout')
    lines = [l.decode(u'UTF-8') for l in f.readlines()]
    f.close()
    ttdict = {u'surface': [], u'pos': [], u'lemma': []}
    for line in lines:
        line = line.replace(u'\n', '')
        rec = line.split('\t')
        if len(rec) == 3:
            ttdict[u'surface'].append(rec[0])
            ttdict[u'pos'].append(rec[1])
            ttdict[u'lemma'].append(rec[2])
    os.remove(u'.tgin')
    os.remove(u'.tgout')
    return ttdict
