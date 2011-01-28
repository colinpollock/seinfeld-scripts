#!/usr/bin/env python

import sqlite3
import sys
import urllib2

from scrape import scrape_episode


class DatabasePopulator(object):
    def __init__(self, filename):
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()

    def commit(self):
        self.con.commit()


    def _add_episode(self, season_num, episode_num, title, date, writer, 
                                                               director):
        self.cur.execute("""
            INSERT INTO episode 
            (season_number, episode_number, title, the_date, writer, director) 
            VALUES(?, ?, ?, ?, ?, ?)""",
            (season_num, episode_num, title, date, writer, director))

        val = self.cur.execute("""
                               SELECT id
                               FROM episode
                               WHERE season_number = ? AND episode_number = ?
                               """, (season_num, episode_num))
        return val.next()[0]

    def _add_utterance(self, episode_id, utterance_number, speaker):
        self.cur.execute("""
            INSERT INTO utterance 
            (episode_id, utterance_number, speaker)
            VALUES(?, ?, ?)""",
            (episode_id, utterance_number, speaker))

        val = self.cur.execute("""
                               SELECT id
                               FROM utterance
                               WHERE episode_id = ? AND utterance_number = ?
                               """, (episode_id, utterance_number))
        return val.next()[0]


    def _add_sentence(self, utterance_id, sentence_number, text):
        self.cur.execute("""
            INSERT INTO sentence (utterance_id, sentence_number, text)
            VALUES(?, ?, ?)
            """, (utterance_id, sentence_number, text))

    def add_episode(self, html):
        data = scrape_episode(html)
        info, utterances = data

        season_num = info['season_num']
        episode_num = info['episode_num']
        title = info['title']
        date = info['date']
        writer = ', '.join(info['writers'])
        director = info['director']

        # ADD an Episode
        episode_id = self._add_episode(season_num, episode_num, title, date, 
                                       writer, director)

        for utt_num, (speaker, sentences) in enumerate(utterances):
            utterance_id = self._add_utterance(episode_id, utt_num + 1, speaker)

            for sent_num, sentence in enumerate(sentences):
                # Add a Sentence
                self._add_sentence(utterance_id, sent_num + 1, sentence)


if __name__ == '__main__':
    pop = DatabasePopulator('seinfeld.db')
    path = sys.argv[1]
    if path.startswith('http'):
        html = urllib2.urlopen(path).read() 
    else:
        with open(path, 'r') as f:
            html = f.read()
    pop.add_episode(html)
    pop.commit()

