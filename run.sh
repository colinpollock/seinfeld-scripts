#!/bin/bash

rm seinfeld.db
sqlite3 seinfeld.db < make.sql

for file in `ls scripts`
do
  echo PROCESSING $file
  python populatedb.py scripts/$file
done

