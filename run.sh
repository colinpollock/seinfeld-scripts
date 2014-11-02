#!/bin/bash

DB_FILENAME=$1
SCRIPTS_DIR=$2


if [ -f $DB_FILENAME ];
  then rm $DB_FILENAME
fi

sqlite3 $DB_FILENAME < maketables.sql

for file in `ls $SCRIPTS_DIR`
do
  echo PROCESSING $file
  python populatedb.py $DB_FILENAME $SCRIPTS_DIR/$file
done
