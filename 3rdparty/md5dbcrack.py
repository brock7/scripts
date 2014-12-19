#!usr/bin/python
#Creates a list of all the cracked milw0rm md5's 
#and writes them to a file

#Changelog: added exceptions for errors

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, re, urllib2, time, urllib

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

def milw0rm(md5):
	
	time.sleep(2)
	try:
		site = urllib.urlopen(site1, urllib.urlencode({"hash": md5})).readlines()
		for line in site:
			if re.search(md5, line):
				return StripTags(line).replace(md5,"").replace("md5","").replace("cracked","")
	except:
		pass

print "\n\t   d3hydr8[at]gmail[dot]com MD5DBCrack v1.1"
print "\t----------------------------------------------\n"

if len(sys.argv) != 2:
	print "\nUsage: ./md5dbcrack.py <file to save>"
	print "Ex: ./md5dbcrack.py <md5db.txt>\n"
	sys.exit(1)

start = 0
file = open(sys.argv[1], "a")
site = "http://www.milw0rm.com/cracker/list.php?start="
site1 = "http://www.milw0rm.com/md5/search.php"

print "[+] Collecting Database...\n"

while 1:
	try:
		time.sleep(3)
		source = urllib2.urlopen(site+str(start), "80").read()
	except(urllib2.URLError):
		pass
	md5s = re.findall("[a-f0-9]"*32,source)
	print "\n[+] Collected:",len(md5s)
	print "[+] Cracking MD5s\n"
	start +=30
	for md5 in md5s:
		print "[+] Cracking:",md5
		try:
			crack = milw0rm(md5)
			if crack[-1:] == "\n":
				crack = crack[:-1]
			crack = re.sub("\s","",crack)
			if crack.find("processing") == -1 and crack != "notfound" and crack != "waiting":
				print "\t[+] Password:",crack
				file.writelines(md5+" : "+crack+"\n")
		except(IOError, TypeError):
			pass
	if len(md5s) == 0:
		break
	
file.close()
print "\n[+] Finished Collecting"
print "[+] Wrote md5s:",sys.argv[1]
print "\n[-] Done\n"

