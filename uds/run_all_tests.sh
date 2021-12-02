#!/bin/sh

BASEDIR="$( dirname "$0" )"
cd "$BASEDIR"

for directory in *; do
    
    if [ -d "${directory}" ]; then
    
    	/usr/bin/python "$(basename "${directory}")"/test.py
    fi
    
done

exit 0