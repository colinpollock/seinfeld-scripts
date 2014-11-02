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



CREATE VIEW speaker_sentence AS
    SELECT u.speaker, s.text
    FROM utterance u JOIN sentence s ON u.id == s.utterance_id
;

