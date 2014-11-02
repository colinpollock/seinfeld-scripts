Seinfeld Scripts
================

I downloaded all of the Seinfeld scripts from 
[seinology.com](http://www.seinology.com/) and wrote scripts to extract the
scripts and put them into a SQLite database.

Feel free to message me if you want the DB file.

Instructions
============

1) `mkdir scripts`
2) `python download.py scripts`
3) Fix any issues in the data (See CHANGES MADE TO DATA)
4) `./run.sh seinfeld.db scripts`


Database Schema
===============

Episode
-------
```sql
sqlite> .schema episode
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

sqlite> select * from episode limit 3;
id	season_number	episode_number	title	the_date	writer	director
1	1	0	Good News, Bad News	July 5, 1989	Larry David, Jerry Seinfeld	Art Wolff
2	2	5	The Apartment	April 4, 1991	Peter Mehlman	Tom Cherones
3	6	16	The Beard	February 9, 1995	Carol Leifer	Andy Ackerman
```


Utterance
---------
```sql
CREATE TABLE utterance(
    id INTEGER PRIMARY KEY,
    episode_id INTEGER NOT NULL,
    utterance_number INTEGER NOT NULL,

    speaker TEXT NOT NULL,
    UNIQUE(episode_id, utterance_number),
    FOREIGN KEY(episode_id) REFERENCES episode(id)
);

sqlite> select * from utterance limit 3;
id	episode_id	utterance_number	speaker
1	1	1	JERRY
2	1	2	GEORGE
3	1	3	JERRY
```


Sentence
--------
```sql
sqlite> .schema sentence
CREATE TABLE sentence(
    id INTEGER PRIMARY KEY,
    utterance_id INTEGER NOT NULL,
    sentence_number INTEGER NOT NULL,
    text TEXT NOT NULL,
    UNIQUE(utterance_id, sentence_number),
    FOREIGN KEY(utterance_id) REFERENCES utterance(id)
);

sqlite> select * from sentence limit 3;
id	utterance_id	sentence_number	text
1	1	1	(pointing at George's shirt) See, to me, that button is in the worst possible spot.
2	1	2	The second button literally makes or breaks the shirt, look at it.
3	1	3	It's too high!
```


Data Issues
===========
* Script transcribers sometimes describe how a line is spoken or what's going on
  in a scene as parentheticals preceding lines. I'd like to remove these and I
  think it may be as easy as looking for a pair of parentheses at the beginning
  of a line.
* A lot of the character names are uses inconsistently.

CHANGES MADE TO DATA
====================
* Changed Pilot from episode 1 to episode 0
  pc: 101, season 1, episode 0 (Pilot)<br>


Stats
=====
####Characters with the most lines
```sql
SELECT speaker, count(*) count
FROM utterance
GROUP BY speaker
ORDER BY count DESC
LIMIT 20;

speaker	count
JERRY	14645
GEORGE	9613
ELAINE	7967
KRAMER	6656
NEWMAN	625
MORTY	502
HELEN	470
FRANK	429
SUSAN	382
ESTELLE	273
MAN	207
PETERMAN	199
WOMAN	199
PUDDY	163
LEO	145
JACK	124
STEINBRENNER	122
MICKEY	118
BANIA	102
ROSS	102
```
