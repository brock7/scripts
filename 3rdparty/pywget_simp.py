#!/usr/bin/python
#PyWget(simple) is pywget shrunk down.

##http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, urllib2, shutil, os

if len(sys.argv) != 2:
	print "\n\tUsage: ./pywget.py <url>\n"
	print "\nEx. ./pywget.py http://www.darkc0de.com/index.html\n"
	sys.exit(1)
url = sys.argv[1]
if url[:7] != "http://":
	url = "http://"+url
try:
	source = urllib2.urlopen(url)
except(urllib2.HTTPError),msg:
	print "\nError:",msg
	sys.exit()
num = 1
file = url.rsplit("/",1)[1]
while os.path.isfile(file) == True:
	file = url.rsplit("/",1)[1]+"."+str(num)
	num+=1
try:
	shutil.copyfileobj(source, open(file, "w+"))
except(IOError):
	print "\nCannot write to `"+file+"' (Permission denied)."
	sys.exit(1)
print "\nFile Created:",file,"\n"