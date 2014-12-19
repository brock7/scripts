#!/usr/bin/python
#Collects all md5's from a database dump and
#attempts to crack them. If one is cracked
#it will print out the line it was found on. 

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import md5, sys, re

if len(sys.argv) != 3:
	print "Usage: ./dumpcrack.py <database> <wordlist>"
	sys.exit(1)

try:
  database = open(sys.argv[1], "r").readlines()
except(IOError): 
  print "\nError: Check your dump path\n"
  sys.exit(1)

try:
  words = open(sys.argv[2], "r").readlines()
except(IOError): 
  print "\nError: Check your wordlist path\n"
  sys.exit(1)

num = 1
md5s = {}
print "\n[+] Words Loaded:",len(words)
print "[+] Searching Database Dump..."
for line in database:
	try:
		MD5 = re.findall("[a-f0-9]"*32,line)[0]
		md5s[MD5] = num
	except(IndexError):
		pass
	num +=1
print "\n[+] MD5s Found:",len(md5s)
print "[+] Beginning Crack\n"
for k,v in md5s.items():
	for word in words:
		value = md5.new(word[:-1]).hexdigest()
		if k == value: 
			print "MD5:",k,"Line:",v,"Cracked:",word[:-1],"\n"



	
	



