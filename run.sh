#!/bin/bash

rm seinfeld.db
sqlite3 seinfeld.db < maketables.sql

for file in `ls scripts`
do
  echo PROCESSING $file
  python populatedb.py scripts/$file
done

echo Inserting words
python populatewords.py
