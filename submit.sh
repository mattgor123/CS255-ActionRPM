#!/bin/bash
echo "$1"
echo rm *.tar.gz
echo find . -name "*.pyc" -print0 | xargs -0 rm -rf
echo find . -name "*.*~" -print0 | xargs -0 rm -rf
mkdir cs255-assignment-$1-actionrpm
cp -r audio cs255-assignment-$1-actionrpm
cp -r states cs255-assignment-$1-actionrpm
cp -r images cs255-assignment-$1-actionrpm
cp -r sprites cs255-assignment-$1-actionrpm
cp -r util cs255-assignment-$1-actionrpm
cp game.py cs255-assignment-$1-actionrpm

cd cs255-assignment-$1-actionrpm

tar -zcvf cs255-assignment-$1-actionrpm.tar.gz *

cp cs255-assignment-$1-actionrpm.tar.gz ..

cd ..

rm -rf cs255-assignment-$1-actionrpm
