#!/usr/bin/env python

import re
import sqlite3

con = sqlite3.connect('seinfeld.db')
cur = con.cursor()
sql = """
      SELECT u.speaker, s.text, s.id
      FROM sentence s JOIN utterance u ON u.id == s.utterance_id
      """
res = cur.execute(sql).fetchall()
res.sort(key=lambda item: item[2])
for speaker, sentence, sent_id in res:
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
