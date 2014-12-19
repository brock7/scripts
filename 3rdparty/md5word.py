#!/usr/bin/python
#Uses all wordlists in a dir to crack a hash.
#
#www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import md5, sys, os, time

def getwords(wordlist):
	try:
  		file = open(wordlist, "r")
		words = file.readlines()
		file.close()
	except(IOError),msg:
		words = "" 
  		print "Error:",msg
  		pass
	return words
	
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

if len(sys.argv) != 3:
	print "Usage: ./md5word.py <hash> <wordlist dir>"
	sys.exit(1)
	
pw = sys.argv[1]
wordlists = os.listdir(sys.argv[2])

print "\n   d3hydr8[at]gmail[dot]com md5word v1.0"
print "-----------------------------------------"
print "\n[+] Hash:",pw
print "[+] Wordlists Loaded:",len(wordlists)
print "[+] Started:",timer(),"\n"

for lst in wordlists:
	words = getwords(os.path.join(sys.argv[2],lst))
	print "[+] List:",lst,"  Length:",len(words),"loaded"
	for word in words:
		hash = md5.new(word[:-1]).hexdigest()
		if pw == hash: 
			print "\n[+] Found Password:",os.path.join(sys.argv[2],lst)
			print "[!] Password is:",word
			print "\n[+] Done:",timer()
			sys.exit(1)
print "\n[+] Done:",timer()



	
	



