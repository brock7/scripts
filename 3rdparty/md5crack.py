#!/usr/bin/python
#Attempts to crack hash against any givin wordlist.
#http://darkcode.ath.cx/
#d3hydr8[at]gmail[dot]com 

import md5, sys

if len(sys.argv) != 3:
	print "Usage: ./md5crack.py <hash> <wordlist>"
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
	hash = md5.new(word[:-1])
	value = hash.hexdigest()
	if pw == value: 
		print "Password is:",word,"\n"



	
	



