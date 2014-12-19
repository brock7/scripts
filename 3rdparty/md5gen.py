#!/usr/bin/python

import md5, sys

if len(sys.argv) != 2:
	print "Usage: ./md5gen.py <password>"
	sys.exit(1)
	
pw = sys.argv[1]
hash = md5.new()
hash.update(pw)
print "\nYour password hash:"
print hash.hexdigest()
