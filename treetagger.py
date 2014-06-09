# -*- coding:utf-8 -*-

from subprocess import PIPE, Popen
import platform


def winproc(input):
    fout = open('.trin', 'w')
    fout.write(input.encode('utf-8'))
    fout.close()
    CMD = 'tag-german .trin .trout'
    p = Popen(CMD, shell=True)
    p.communicate()
    f = open('.trout')
    cont = f.read()
    f.close()
    return cont.decode('UTF-8')


def proc(input):
    CMD = 'tree-tagger-german-utf8'
    p = Popen(CMD, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (outp, err) = p.communicate(input.encode('UTF-8'))
    outp = outp.decode('UTF-8')
    return outp


def run(input):
    if platform.system() == 'Windows':
        outp = winproc(input)
    else:
        outp = proc(input)
    wordLines = outp.split(u'\n')
    words = []
    for line in wordLines:
        rec = line.split(u'\t')
        if len(rec) == 3:
            words.append(rec)
        else:
            print line
    return words
