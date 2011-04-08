#!/bin/sh
if [ -z "$1" ]
then
        echo "No input file specified"
	echo "USAGE: ./test.sh [FILE]"
else
	python -d ../scenejs-pycollada.py -o htmljs -v -d -p --detailed $1
fi
