#!/usr/bin/python
#Takes a wordlist and creates a md5.
#Then creates a database depending on
#the first char the hash begins with.

#pave project

##http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, md5, sets, re

def md5gen(word):
	hash = md5.new(word)
	return hash.hexdigest()

def testdup(hash):
	try:
		db = open(hash[0]+".txt", "r").read()
		if db.find(hash) == -1:
			return None
		else:
			return True
	except(IOError):
		return None
	
	
if len(sys.argv) != 2:
	print "\n\tUsage: ./alphadbgen.py <wordlist>"
	print "\n\tEx: ./alphadbgen.py wordlist.txt\n"
	sys.exit(1)
	
try:
	words = open(sys.argv[1], "r").readlines()
except(IOError), msg: 
 	print "[-] Error:",msg,"\n" 
	sys.exit(1)
words = list(sets.Set(words))
print "\n[+] Length:",len(words),"\n"
for word in words:
	word = word.replace("\n","")
	hash = md5gen(word) 
	if testdup(hash) == None:
		print hash+":"+word
		db = open(hash[0]+".txt", "a")
		print "Writing:",hash[0]+".txt"
		db.writelines(hash+":"+word+"\n")
		db.close()
	else:
		print "Duplicate Found:",hash+":"+word
print "\n[+] Databases Complete\n"


#!/usr/bin/python
#Searches db for matching hash

#www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import sys, os

DB_DIR = "/home/d3hydr8/dbs"

def getwords(db):
	try:
  		file = open(db, "r")
		words = file.readlines()
		file.close()
	except(IOError),msg:
		words = "" 
  		print "Error:",msg
  		pass
	return words

if len(sys.argv) != 2:
	print "Usage: ./hashsearch.py <hash>"
	sys.exit(1)

dbs = os.listdir(DB_DIR)
hash = sys.argv[1]
words = getwords(os.path.join(DB_DIR,hash[0]+".txt"))
print "\n[+] Loaded:",len(words),"hashes"
for word in words:
	word = word.replace("\n","")
	if word.find(hash) != -1:
		print "\n[+] Found:",word
print "\n[-] Done\n"







	