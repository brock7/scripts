#!/usr/bin/python
#Prints checksum of all files in directory.
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import os, sys, md5

def sumfile(fobj):
	m= md5.new()
	while True:
		d= fobj.read(8096)
		if not d:
			break
		m.update(d)
	return m.hexdigest()

def md5sum(fname):
	if fname == '-':
		ret = sumfile(sys.stdin)
	else:
		try:
			f = open(fname, 'rb')
		except:
			return 'Failed to open file'
		ret = sumfile(f)
		f.close()
	return ret
	
def title():
	print "\n   d3hydr8[at]gmail[dot]com CheckSummer v1.0"
	print "----------------------------------------------\n"

if len(sys.argv) != 2:
	title()
	print "\n[-] Need a directory\n"
	sys.exit(1) 
	
files = os.listdir(sys.argv[1])
title()

for fname in files:
	checks =  md5sum(os.path.join(sys.argv[1],fname))
	if checks != "Failed to open file":
		print fname,"\t\t",checks




