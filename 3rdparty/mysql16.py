#!/usr/bin/python
#MySQL 64bit Hash DB Generator

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import sys

def mysql323(clear): 
    # Taken almost verbatim from mysql's source 
    nr = 1345345333 
    add = 7 
    nr2 = 0x12345671 
    retval = "" 
    for c in clear: 
	if c == ' ' or c == '\t': 
	    continue 
	tmp = ord(c) 
	nr ^= (((nr & 63) + add) * tmp) + (nr << 8) 
	nr2 += (nr2 << 8) ^ nr 
	add += tmp 
    res1 = nr & ((1 << 31) - 1) 
    res2 = nr2 & ((1 << 31) - 1) 
    return "%08lx%08lx" % (res1, res2)

print "\n   d3hydr8[at]gmail[dot]com mysql16 v1.0"
print "-------------------------------------------"

if len(sys.argv) != 3:
	print "Usage: ./mysql16.py <wordlist> <output file>\n"
	sys.exit(1)

db = open(sys.argv[2], "a")
print "\n[+] Database:",sys.argv[2]


try:
  	words = open(sys.argv[1], "r").readlines()
  	print "[+] Words Loaded:",len(words),"\n"
except(IOError): 
  	print "[-] Error: Check your wordlist path\n"
  	sys.exit(1)

i = 1
for word in words:
	print i,"of",len(words)
	word = word.replace("\r","").replace("\n","")
	hash1 = mysql323(word)
	print word+":"+hash1
	db.writelines(word+":"+hash1+"\n")

db.close()
print "\n[+] Database Finished\n"
