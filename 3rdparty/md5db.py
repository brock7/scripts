#!usr/bin/python
#Creates a list of all the cracked milw0rm md5's 
#and writes them to a file

#Changelog: Writes md5s as it collects, added exception and time.sleep(x)

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, re, urllib2, time

print "\n\t   d3hydr8[at]gmail[dot]com MD5-Collect v1.1"
print "\t----------------------------------------------\n"

if len(sys.argv) != 2:
	print "\nUsage: ./md5collect.py <file to save>"
	print "Ex: ./md5collect.py <md5db.txt>\n"
	sys.exit(1)

start = 0
file = open(sys.argv[1], "a")
site = "http://www.milw0rm.com/cracker/list.php?start="

print "[+] Collecting Database...\n"

while 1:
	try:
		time.sleep(3)
		source = urllib2.urlopen(site+str(start), "80").read()
	except(urllib2.URLError):
		pass
	md5s = re.findall("[a-f0-9]"*32,source)
	start +=30
	for md5 in md5s:
		file.writelines(md5+"\n")
	print "[+] Collected:",len(md5s)
	if len(md5s) == 0:
		break
	
file.close()
print "\n[+] Finished Collecting"
print "[+] Wrote md5s:",sys.argv[1]
print "\n[-] Done\n"

