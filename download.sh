#!/bin/bash

# Download all the scripts from seinology.com

# Skip clip show:
#  100and101
#  177and178

# Get double episodes:
#  82and83
#  179and180

for i in {01..81} '82and83' {84..99} {102..176} '179and180'
do
  echo $i
  curl http://www.seinology.com/scripts/script-$i.shtml > $i.shtml
done

for file in `ls`
do
  mv $file ${file#0}
done
