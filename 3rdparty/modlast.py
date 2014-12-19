#!/usr/bin/python
#Watches a log file for modifications and reports a change and how many bytes.
#(This can be used for any file)
#d3hydr8[at]gmail[dot]com

import os, sys, time, pwd

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def gettime():
	clock = time.asctime(time.localtime(os.path.getmtime(logfile)))
	return clock

def getsize():
	size = os.path.getsize(logfile)
	return size
	
def title():
	print "\n   d3hydr8[at]gmail[dot]com ModLast v1.0"
	print "-------------------------------------------"

if len(sys.argv) != 3:
	print "\nUsage: ./modlast.py <log_file> <secs to check>"
	print "ex. ./modlast.py /var/log/apache/access_log 120\n"
	sys.exit(1)

logfile = sys.argv[1]
if os.path.isfile(logfile) == False:
	title()
	print "\n[-] Cannot Open File, Check Full Path!!!\n"
	sys.exit(1)
	
title()
print "[+] Analyzing:",logfile
print "[+] Time:",sys.argv[2],"secs"
print "[+] Owner:",pwd.getpwuid(os.stat(logfile)[4])[0]
print "[+] Size:",getsize(),"bytes"
print "[+] Last Modified:",gettime()
print "[+] Starting:",timer()

old_time = gettime()
while True:
	time.sleep(int(sys.argv[2]))
	new_time = gettime()
	if new_time != old_time:
		print "\n[+] File Modified:",new_time
		print "[+] New Size:",getsize(),"bytes\n"
		old_time = new_time
	#else:    
		#print "\n[-] File Not Modified"
		
		