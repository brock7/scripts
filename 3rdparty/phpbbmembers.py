#!/usr/bin/python
#Searches phpBB's memberlist.php and extracts users.
#d3hydr8[at]gmail[dot]com 

import urllib, sys, re, time

if len(sys.argv) != 2:
	print "\nUsage: ./phpBBmembers.py <url>"
	print "Ex: ./phpbbmembers.py http://www.site.com/phpbb/memberlist.php\n"
	sys.exit(1)
	
url = sys.argv[1]
if url[:7] != "http://":
	url = "http://"+url
print "\nSearching:",url 

site = urllib.urlopen(url).read()
users = re.findall("u=\d*&amp;sid=\w+\" >\w+</a>", site)
if len(users) >= 1:
	print "\nAttempt failed: Trying another\n"
else:
	users = re.findall("\">\w+</a>", site)
print "Found:",len(users),"\n"
time.sleep(3)
for user in users:
	u = user.split('>') 
	mem = u[1].replace("</a", "")
	#Lets take care of some garbage.
	if mem.isdigit() == False and mem != "Next" and mem != "phpBB": 
		print mem


	
	



