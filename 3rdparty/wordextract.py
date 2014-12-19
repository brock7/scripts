#!/usr/bin/python
#Word Extractor from a site.

import sys, urllib2, re, sets

#Min length of word
MIN_LENGTH = 3
#Max length of word
MAX_LENGTH = 10

def StripTags(text):
	finished = 0
	while not finished:
		finished  =1
		start =  text.find("<")
		if start >= 0:
			stop = text[start:].find(">")
			if stop >= 0:
				text = text[:start] + text[start+stop+1:]
				finished = 0
	return text
			
if len(sys.argv) != 3:
	print "\nUsage: ./wordextract.py <site> <file to save words>"
	print "Ex: ./wordextract.py http://www.test.com wordlist.txt\n"
	sys.exit(1)

site = sys.argv[1]
if site[:7] != "http://":
	site = "http://"+site
	
print "\n[+] Retrieving Source:",site
source = StripTags(urllib2.urlopen(site).read())
words = re.findall("\w+",source)
words = list(sets.Set(words))
l = len(words)
print "[+] Found:",l,"words"
print "[+] Trimming words to length"
for word in words:
	if not MIN_LENGTH <= len(word) <= MAX_LENGTH:
		words.remove(word)
print "\n[+] Removed:",l-len(words),"words"
print "[+] Writing:",len(words),"words to",sys.argv[2]
file = open(sys.argv[2],"a")
for word in words:
	file.writelines(word+"\n")
file.close()
print "\n[-] Complete\n"