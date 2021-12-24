#!/bin/sh

BASEDIR="$( dirname "$0" )"
cd "$BASEDIR"

for directory in *; do
    
    if [ -d "${directory}" ]; then

        pythonTestScript="$(basename "${directory}")"/test.py

        if [ -f "${pythonTestScript}" ]; then

    	    /usr/bin/python "${pythonTestScript}"

        fi

        runAllTestsScript="$(basename "${directory}")"/run_all_tests.sh

        if [ -f "${runAllTestsScript}" ]; then

            /bin/sh "${runAllTestsScript}"

        fi
    fi
    
done

exit 0
