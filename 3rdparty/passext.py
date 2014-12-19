#!/usr/bin/python
#(2 ways)Saves highlighting & delete time by printing out 
#just the users on a system.
#d3hydr8[at]gmail[dot]com 

import sys 
if len(sys.argv) != 2:
	print "Usage: ./passext.py </etc/passwd file>"
	sys.exit(1)

pwfile = sys.argv[1]
try:
  pws = open(pwfile, "r")
except(IOError): 
  print "Error: Check your file path\n"
  sys.exit(1)
pws = pws.readlines()
print "\n1st Way:\n"
for i in pws:
	print i.split(':',1)[0]
print "\n2nd Way:\n"
try:
	import spwd
except(ImportError):
	print "Missing spwd module the comes with py2.5\n"
	sys.exit(1)
lst = spwd.getspall()
for user in lst: print user[0]
	