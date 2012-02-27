PRAGMA foreign_keys = ON;

CREATE TABLE episode(
    id INTEGER PRIMARY KEY,
    season_number INTEGER NOT NULL,
    episode_number INTEGER NOT NULL,
    title TEXT,
    the_date TEXT,
    writer TEXT,
    director TEXT,
    UNIQUE(season_number, episode_number)
);


CREATE TABLE utterance(
    id INTEGER PRIMARY KEY,
    episode_id INTEGER NOT NULL,
    utterance_number INTEGER NOT NULL,

    speaker TEXT NOT NULL,
    UNIQUE(episode_id, utterance_number),
    FOREIGN KEY(episode_id) REFERENCES episode(id)
);


CREATE TABLE sentence(
    id INTEGER PRIMARY KEY,
    utterance_id INTEGER NOT NULL,
    sentence_number INTEGER NOT NULL,
    text TEXT NOT NULL,
    UNIQUE(utterance_id, sentence_number),
    FOREIGN KEY(utterance_id) REFERENCES utterance(id)
);


CREATE TABLE word(
    id INTEGER PRIMARY KEY,
    sentence_id INTEGER NOT NULL,
    word_number INTEGER NOT NULL,
    text TEXT NOT NULL,
    part_of_speech TEXT,
    UNIQUE(sentence_id, word_number),
    FOREIGN KEY(sentence_id) REFERENCES sentence(id)
);

CREATE VIEW bigram AS
SELECT u.speaker, w1.text AS word_one, w2.text AS word_two, 
       w1.part_of_speech AS pos_one, w2.part_of_speech AS pos_two
FROM word w1 JOIN word w2 ON w1.sentence_id == w2.sentence_id AND 
         w1.word_number == w2.word_number - 1
     JOIN sentence s ON s.id == w1.sentence_id JOIN utterance u ON 
         u.id == s.utterance_id
;

CREATE VIEW speaker_sentence AS
    SELECT u.speaker, s.text
    FROM utterance u JOIN sentence s ON u.id == s.utterance_id
;

