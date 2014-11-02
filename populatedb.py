"""Script for processing Seinfeld scripts and populating a SQLite3 DB. """

import argparse
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
        info, utterances = scrape_episode(html)

        season_num = info['season_num']
        episode_num = info['episode_num']
        title = info['title']
        date = info['date']
        writer = ', '.join(info['writers'])
        director = info['director']

        episode_id = self._add_episode(season_num, episode_num, title, date, 
                                       writer, director)

        for utt_num, (speaker, sentences) in enumerate(utterances):
            utterance_id = self._add_utterance(episode_id, utt_num + 1, speaker)

            for sent_num, sentence in enumerate(sentences):
                self._add_sentence(utterance_id, sent_num + 1, sentence)

def main(args):
    pop = DatabasePopulator(args.db_filepath)
    scripts_path = args.scripts_path

    with open(scripts_path, 'r') as fh:
        html = fh.read()

    pop.add_episode(html)
    pop.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'db_filepath',
        help='Path to SQLite DB file to be created.'
    )

    parser.add_argument(
        'scripts_path',
        help='Path to directory containing scripts files.'
    )

    main(parser.parse_args(sys.argv[1:]))
