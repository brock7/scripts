#!/usr/bin/python
#Wordlist Splitter

#www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import sys, time

if len(sys.argv) != 3:
	print "\nUsage: ./wordsplit.py <wordlist> <num to split>"
	print "Ex: ./wordsplit.py wordlist.txt 500\n"
	sys.exit(1)

print "\n d3hydr8:darkc0de.com WordSplitter v1.0"
print "----------------------------------------"

TIME_TO_WAIT = 0.5

try:
  	words = open(sys.argv[1], "r").readlines()
except(IOError): 
  	print "\nError: Check your wordlist path\n"
  	pass

print "[+] Wordlist Loaded:",len(words),"words"
print "[+] Splitting Point:",sys.argv[2]
print "[+] Creating:",len(words) / int(sys.argv[2]) + 1,"wordlists"
print "[+] Total Time:",len(words) * TIME_TO_WAIT / 60,"minutes"
print "\n[+] Generating...\n"

num = 1
while len(words) != 0:
	file = open(str(num)+".txt", "a")
	for word in words[:int(sys.argv[2])]:
		#print word.replace("\n","")
		time.sleep(TIME_TO_WAIT)
		file.writelines(word.replace("\n","").replace("\r","")+"\n")
		words.remove(word)
	print "\n[+] List:",str(num)+".txt done"
	num +=1
	file.close()
	print "[+] Words Left:",len(words),"\n"
print "\n[!] Wordlists Created:",num - 1 
print "[-] Done\n"





	
	



