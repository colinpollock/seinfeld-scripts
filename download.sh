#!/bin/bash

# Download all the scripts from seinology.com

SCRIPTS_DIR=$1

# Skip clip show:
#  100and101
#  177and178

# Get double episodes:
#  82and83
#  179and180

for i in {1..9}
do
  echo $i
  curl http://www.seinology.com/scripts/script-0$i.shtml > $SCRIPTS_DIR/0$i.shtml
done

for i in {10..81} '82and83' {84..99} {102..176} '179and180'
do
  echo $i
  curl http://www.seinology.com/scripts/script-$i.shtml > $SCRIPTS_DIR/$i.shtml
done

for file in `ls`
do
  mv $file ${file#0}
done
