#!/usr/bin/python
#Attempts to crack MySQL v5 hash using wordlist.
#http://darkc0de.com/
#d3hydr8[at]gmail[dot]com 

import sys

def c1(word):
	s = hashlib.sha1()
	s.update(word[:-1])
	s2 = hashlib.sha1()
	s2.update(s.digest())
	return s2.hexdigest()

def c2(word):
	s = sha.new()
	s.update(word[:-1])
	s2 = sha.new()
	s2.update(s.digest())
	return s2.hexdigest()
	
if len(sys.argv) != 3:
	print "Usage: ./mysql5crack.py <hash> <wordlist>"
	sys.exit(1)
	
pw = sys.argv[1]
if len(pw) != 40:
	print "Improper hash length\n"
  	sys.exit(1)
try:
  	words = open(sys.argv[2], "r")
except(IOError): 
  	print "Error: Check your wordlist path\n"
  	sys.exit(1)
words = words.readlines()
print "\nWords Loaded:",len(words)

try:
	import hashlib
	for word in words:
		if pw == c1(word): 
			print "\nPassword is:",word
except(ImportError):
	import sha
	for word in words:
		if pw == c2(word): 
			print "\nPassword is:",word


