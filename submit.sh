#!/bin/bash
echo "$1"
echo ls

find . -name "*.tar.gz" -print0 | xargs -0 rm -rf
find . -name "*.pyc" -print0 | xargs -0 rm -rf
find . -name "*.*~" -print0 | xargs -0 rm -rf
find . -name "*~" -print0 | xargs -0 rm -rf

mkdir cs255-assignment-$1-actionrpm
cp -r audio cs255-assignment-$1-actionrpm
cp -r map cs255-assignment-$1-actionrpm
cp -r states cs255-assignment-$1-actionrpm
cp -r images cs255-assignment-$1-actionrpm
cp -r sprites cs255-assignment-$1-actionrpm
cp -r util cs255-assignment-$1-actionrpm
cp -r levels cs255-assignment-$1-actionrpm
cp game.py cs255-assignment-$1-actionrpm
cp README cs255-assignment-$1-actionrpm

tar -zcvf cs255-assignment-$1-actionrpm.tar.gz cs255-assignment-$1-actionrpm

rm -rf cs255-assignment-$1-actionrpm
