#!/usr/bin/env python

from __future__ import division

from collections import defaultdict
import re
import sqlite3


def words(speaker):
    con = sqlite3.connect('seinfeld.db')
    cur = con.cursor()
    sql = """SELECT text 
             FROM speaker_sentences
             WHERE speaker == ?
          """
    res = cur.execute(sql, (speaker,))
    sentences = [tup[0] for tup in res.fetchall()]
    for sent in sentences:
        words = sentence.lower()
        pat = re.compile(r'\w+|\.{3}|[!?.]')
        words = pat.findall(words)




def ngrams(n, speaker=None):
    con = sqlite3.connect('seinfeld.db')
    cur = con.cursor()
    sql = """SELECT s.text 
             FROM utterance u JOIN sentence s on s.utterance_id == u.id
             WHERE speaker = ?
          """
    ret = cur.execute(sql, (speaker,))
    sentences = [str(r[0]) for r in ret.fetchall()]


    ngrams = []
    for sentence in sentences:
        words = sentence.lower()
        pat = re.compile(r'\w+|\.{3}|[!?.]')
        words = pat.findall(words)
        for i in range(len(words) - n + 1):
            ngram = tuple(words[i: i + n])
            ngrams.append(ngram)

    return ngrams



