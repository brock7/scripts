#!/usr/bin/python
#Trys to find your wireless config file and extracts 
#the wep key and then decodes it.
#Tested on Suse 10.2, if your distro's wireless config file isn't
#called "wireless". Email me a sample file and type of 
#distro so I can make this more versitile.
#d3hydr8[at]gmail[dot]com
#http://darkcode.ath.cx

import sys, os, re, binascii
	
print "\nSearching for wireless config file...\n"

try:
	file = os.popen("find / -name wireless").readlines()
except(OSError):
	pass
for line in file:
	try:
		text = open(line[:-1], "r").readlines()
		for line in text:
			if re.search("WIRELESS_KEY=", line):
				key = line.lstrip("WIRELESS_KEY=").replace("\"","").replace("-","")
				if key != "\n":
					print "\n\n",key
					print "WEP key:",binascii.a2b_hex(key[:-1]),"\n"
				
	except(IOError):
		pass

#You must be root to use iwconfig
	
file = os.popen("iwconfig").readlines()
for line in file:
	if re.search("Encryption key:", line):
		key = line.lstrip("Encryption key:").replace("-","").split(" ",1)
		if len(key) == 2:
			key = key[0]
		print key
		print "WEP key:",binascii.a2b_hex(key),"\n"

		

