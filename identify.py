#!/usr/bin/env python

from __future__ import division

import random
import re
import sqlite3

import nltk.classify.util
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy

import ngrams

def words(speaker):
    con = sqlite3.connect('seinfeld.db')
    cur = con.cursor()
    sql = """
          SELECT u.speaker, w.text
          FROM utterance u, sentence s, word w
          ON u.id == s.utterance_id AND s.id = w.sentence_id
          """
    ret = cur.execute(sql)
    words = ret.fetchall()

    cur.close()
    return [str(w[1]) for w in words]

def word_features(word):
    return {'word': word}

def ngram_features(ngram):
    return {'ngram': ngram}

featuresets = []
for name in 'JERRY', 'ELAINE', 'GEORGE', 'KRAMER':
    pairs = ngrams.ngrams(2, name)
    featuresets += [(ngram_features(pair), name) for pair in pairs]
    
random.shuffle(featuresets)


cutoff = int(len(featuresets)) * 3 // 4
trainfeats = featuresets[:cutoff]
testfeats = featuresets[cutoff:]

print 'train on %d instances, test on %d instances' % \
                    (len(trainfeats), len(testfeats))

classifier = NaiveBayesClassifier.train(trainfeats)
classifier.show_most_informative_features(10)
print accuracy(classifier, testfeats)




#jerry = [(word_features(word), 'JERRY') for word in words('JERRY')]
#elaine = [(word_features(word), 'ELAINE') for word in words('ELAINE')]
#featuresets = jerry + elaine
