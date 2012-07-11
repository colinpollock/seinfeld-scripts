#!/usr/bin/env python

from operator import itemgetter
import re
import sqlite3

con = sqlite3.connect('seinfeld.db')
cur = con.cursor()

query = """
        SELECT u.speaker, s.text, s.id
        FROM sentence s JOIN utterance u ON u.id == s.utterance_id
        """
res = sorted(cur.execute(query).fetchall(), key=itemgetter(2))

for speaker, sentence, sent_id in res:
    #TODO: use nltk sentence splitter and tokenizer
    pat = re.compile(r"[A-Za-z']+|\.{3}|[!?.]")
    words = pat.findall(sentence.lower())
    for i, word in enumerate(words):
        sql = """
              INSERT INTO word(sentence_id, word_number, text, part_of_speech)
              VALUES(?, ?, ?, ?)
              """
        cur.execute(sql, (sent_id, i + 1, word, 'POS'))
    

con.commit()
cur.close()
