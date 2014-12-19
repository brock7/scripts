#!/usr/bin/python
#Locates where an ip address is using antionline.com.
#I know theres a better way to do this but it works.
#Email me your way and i will post it. 
#subclass str and define .remove that will call .replace (_, "")  ??
#d3hydr8[at]gmail[dot]com 

import urllib, sys, re
 
if len(sys.argv) != 2:
	print "\nUsage: ./iplocate.py <ip>\n"
	sys.exit(1)

ip = sys.argv[1]

url = "http://antionline.com/tools-and-toys/ip-locate/index.php?address="+ip

site = urllib.urlopen(url).readlines()
for line in site:
	if re.search("<br><b>", line):
		line = line.replace("</b>","").replace('<br>',"").replace('<b>',"")
		print "\n",line,"\n"