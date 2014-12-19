#!/usr/bin/python
#Uses a list of log files to search
#for existing logs and then checks readability
#with the current user.
#d3hydr8[at]gmail[dot]com 

import sys, os, getpass

if len(sys.argv) != 2:
	print "Usage: ./logfind.py <log list>"
	sys.exit(1)
	
try:
  logs = open(sys.argv[1], "r").readlines()
except(IOError): 
  print "Error: Check your loglist path\n"
  sys.exit(1)

print "\n[+] Log Files Loaded:",len(logs),"\n"

for log in logs:
	if os.path.isfile(log[:-1]) == True:
		print "[+] Found:",log[:-1]," Size:",os.path.getsize(log[:-1])
		try:
			f = open(log[:-1], "r")
		except(IOError):
			print "[-] Not Readable by",getpass.getuser()
print "\n[+] Done\n"



	
	



