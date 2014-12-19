#!/usr/bin/python
#Generates a sha1 encrypted hash from password.
import sys

try:
	import hashlib
except(ImportError):
	print "\nYou need the hashlib module installed, try upgrading to python 2.5.\n"
	sys.exit(1)
if len(sys.argv) != 2:
	print "Usage: ./sha1gen.py <password>"
	sys.exit(1)
	
pw = sys.argv[1]

print "\nPassword:"
print hashlib.sha1(pw).hexdigest()