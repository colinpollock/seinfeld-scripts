#!/bin/bash

rm seinfeld.db
sqlite3 seinfeld.db < make.sql

python populatedb.py scripts/$1.shtml

