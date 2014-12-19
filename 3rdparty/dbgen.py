#!/usr/bin/python
#Takes a wordlist and creates a md5
#database. Format: word:md5

##http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, md5

def md5gen(word):
	hash = md5.new(word)
	return hash.hexdigest()
	
if len(sys.argv) != 3:
	print "\n\tUsage: ./dbgen.py <wordlist> <db_file>"
	print "\n\tEx: ./dbgen.py wordlist.txt md5db.db\n"
	sys.exit(1)
	
try:
	words = open(sys.argv[1], "r").readlines()
	db = open(sys.argv[2], "a")
except(IOError), msg: 
 	print "[-] Error:",msg,"\n" 
	sys.exit(1)
print "\n[+] Length:",len(words),"\n"
for word in words:
	word = word.replace("\n","")
	hash = md5gen(word)
	print word+":"+hash
	db.writelines(word+":"+hash+"\n")
print "\n[+] Database Complete\n"
db.close()






	