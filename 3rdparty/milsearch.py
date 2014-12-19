#!/usr/bin/python
#Milw0rm exploits search tool.

import urllib2, re, sys

if len(sys.argv) != 2:
	print "\nUsage: ./milsearch.py "
	print "Ex: ./milsearch.py phpmyadmin\n"
	sys.exit(1)

site = "http://www.milw0rm.com/search.php?dong="

try:
	source = urllib2.urlopen(site+sys.argv[1], "80").read()
	xplts = re.findall("href=\"/exploits/\d+",source)
	print "\n[+] Results Found:",len(xplts),"\n"
except(urllib2.URLError):
	xplts = []
	pass
if len(xplts) >=1:
	for xplt in xplts:
		xplt = xplt.replace("href=\"","")
		print "http://milw0rm.com"+xplt
else:
	print "\nNo Results Found\n"