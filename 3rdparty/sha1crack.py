#!/usr/bin/python
#Attempts to crack a sha1 encrypted hash against any givin wordlist.
#http://darkcode.ath.cx/
#d3hydr8[at]gmail[dot]com 

import sys

try:
	import hashlib
except(ImportError):
	print "\nYou need the hashlib module installed, try upgrading to python 2.5.\n"
	sys.exit(1)

if len(sys.argv) != 3:
	print "Usage: ./sha1crack.py <hash> <wordlist>"
	sys.exit(1)
	
pw = sys.argv[1]
wordlist = sys.argv[2]
try:
  words = open(wordlist, "r")
except(IOError): 
  print "Error: Check your wordlist path\n"
  sys.exit(1)
words = words.readlines()
print "\n",len(words),"words loaded..."
for word in words:
	if pw == hashlib.sha1(word[:-1]).hexdigest(): 
		print "Password is:",word,"\n"



	
	



