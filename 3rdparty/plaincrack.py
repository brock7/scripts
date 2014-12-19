#!usr/bin/python
#Creates a list of all the cracked md5's 
#from plain-text.info and writes them to a file.

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


print "\n\t   d3hydr8[at]gmail[dot]com PlainCrack v1.0"
print "\t----------------------------------------------\n"

if len(sys.argv) != 2:
	print "\nUsage: ./plaincrack.py <file to save>"
	print "Ex: ./plaincrack.py <md5db.txt>\n"
	sys.exit(1)

start = 1
file = open(sys.argv[1], "a")
site = "http://www.plain-text.info/view/action/viewallhashes/page/"

print "[+] Collecting Database...\n"

while 1:
	
	md5s = []
	
	try:
		time.sleep(5)
		source = urllib2.urlopen(site+str(start), "80").readlines()

		print "\n[+] Page Loaded:",start
		for line in source:
			if re.search("[a-f0-9]"*32,line):
				md5s.append(StripTags(line))
		print "[+] Collected:",len(md5s)
		print "[+] Cracking MD5s\n"
		start +=1
		for md5 in md5s:
			if md5[-2:] == "\r\n":
				md5 = md5[:-2]
			index = [index for index,line in enumerate(source) if md5 in line][0]+1
			passwd = re.sub("\r\n","",StripTags(source[int(index)]))
			if passwd != "": 
				print "[+] Cracked:",md5,"|",passwd
				file.writelines(md5+" : "+passwd+"\n")

		if len(md5s) == 0:
			break
	except(urllib2.URLError):
		pass
	except(KeyboardInterrupt):
		print "\n[-] Cancelled\n"
		sys.exit(1)
	
file.close()
print "\n[+] Finished Collecting"
print "[+] Wrote md5s:",sys.argv[1]
print "\n[-] Done\n"

