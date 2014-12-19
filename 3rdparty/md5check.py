#!/usr/bin/python
#Searches hash databases on various sites for a match. I know there
#is a better way of doing this, email me. It works for now.
#d3hydr8[at]gmail[dot]com 

import urllib, sys, re

if len(sys.argv) != 2:
	print "Usage: ./md5check.py <hash>"
	sys.exit(1)
	
hash1 = sys.argv[1]
print "\nSearching for hash",hash1 

url = "http://md5.rednoize.com/?q="+hash1+"&b=MD5-Search"

site = urllib.urlopen(url).readlines()

for line in site:
	if re.search("&nbsp;&nbsp;&nbsp;&nbsp;", line):
		line = line.replace("&nbsp;&nbsp;&nbsp;&nbsp;","").replace('<h3>',"")
		if len(line) != 33:
			print "\n\tPassword is: ",line,"\n"
		else: print "\n\tCouldn't find match.\n"
		
url = "http://gdataonline.com/qkhash.php?mode=txt&hash="+hash1

site = urllib.urlopen(url).readlines()

for line in site:
	if re.search("<!-- splitting... num = 3 --!>", line):
		line = line.replace("<!-- splitting... num = 3 --!>", "").replace('<tr><td width="65%">',"").replace('</td><td width="35%"><b>',"").replace("</b></td></tr>","").replace(hash1,"")
		print "\n\tPassword is: ",line,"\n"


	
	



