#-*- coding:utf-8 -*-

import feedparser
import urllib
from bs4 import BeautifulSoup
import treetagger as tagger


def parseRss(url):
    rss = feedparser.parse(url)
    links = []
    for entry in rss['entries']:
        links.append(entry['link'])
    return links


def getArticle(link):
    suffix = u'/komplettansicht'
    f = urllib.urlopen(link + suffix)
    cont = f.read()
    f.close()
    return cont


def parseArticle(article):
    soup = BeautifulSoup(article)
    text = ''
    for div in soup.find_all('div'):
        if div.has_attr('class') and div['class'] == [u'article-body']:
            text += div.get_text()
    return text


def treetagger(str):
    return tagger.run(str)


def antSentence(sentence):
    antSent = {u'surface': [], u'pos': [], u'lemma': []}
    for w in sentence:
        antSent[u'surface'].append(w[0])
        antSent[u'pos'].append(w[1])
        antSent[u'lemma'].append(w[2])
    return antSent


def textToSentences(antText):
    """
    antText: unicode text annotated by treetagger
    """
    sentences = []
    sentence = []
    for word in antText:
        sentence.append(word)
        if word[1] in [u'$.', u'$?', u'$!']:
            antSent = antSentence(sentence)
            sentences.append(antSent)
            sentence = []
    if len(sentence) > 0:
        antSent = antSentence(sentence)
        sentences.append(antSent)

    return sentences
