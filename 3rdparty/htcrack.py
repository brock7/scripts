#!/usr/bin/python
#Attempts to crack .htpasswd against wordlist
#also cracks FrontPage passwds.

#http://darkc0de.com
#d3hydr8[at]gmail[dot]com

import crypt, sys

if len(sys.argv) != 3:
	print "Usage: ./htcrack.py <password> <wordlist>"
	print "ex: ./htcrack.py user:62P1DYLgPe5S6 /home/d3hydr8/wordlist.txt"
	sys.exit(1)
	
pw = sys.argv[1].split(":",1)
try:
  words = open(sys.argv[2], "r")
except(IOError): 
  print "Error: Check your wordlist path\n"
  sys.exit(1)
wds = words.readlines()
print "\n-d3hydr8[at]gmail[dot]com htcrack v[1.0]-"
print "\n",len(wds),"words loaded..."
for w in wds:
	if crypt.crypt(w[:-1], pw[1][:2]) == pw[1]: 
		print "\nCracked:",pw[0]+":"+w,"\n"
	
		

