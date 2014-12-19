#!/usr/bin/python
#Searches site for scripts.
#d3hydr8[at]gmail[dot]com 

import urllib, sys, re

if len(sys.argv) != 2:
	print "Usage: ./scriptgrab.py <site>"
	sys.exit(1)
	
url = sys.argv[1]

if url[:7] != "http://":
	url = "http://"+url
	
print "\nSearching: ",url,"\n"

site = urllib.urlopen(url).readlines()
#u can add more types to the list below
scripts = ["php","pl","js","py","asp","cgi"]

num = 0
for script in scripts:
	print "\nTrying:",script,"\n"
	for line in site:
		num +=1
		hit = re.findall("/\w+\."+script, line) 
		if hit != []: print "\tFound:",hit[0],"on line",num,"\n"
		
		


	
	



