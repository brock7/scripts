#!/bin/bash
SCRIPT=""" "
#echo $*
#echo $0

########## BEGIN BASH SCRIPT ##########
# add your code here
func1() {
	echo "hello"
}


########## END BASH SCRIPT ##########

if [[ $0 == bash ]]; then
	return 0
fi

exec python -E $0 "$@"

SCRIPT=" """

#!/usr/bin/python
import sys
import os

def invokeBash(cmdline):
	#args = 'bash -c "source %s;%s #__INVOKE__;"' % (sys.argv[0], cmdline)
	args = 'bash -c "source %s;%s;"' % (sys.argv[0], cmdline)
	#print args
	os.system(args)

########## BEGIN PYTHON SCRIPT ##########
# add your code here

import re
#print 'Hello'
#for i in range(1,5):
#	print i
invokeBash('func1')
invokeBash('ls')
########## END PYTHON SCRIPT ##########

