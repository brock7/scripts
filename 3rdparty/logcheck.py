#!/usr/bin/python
#Checks access file for new ips.
#I wrote this to tell me if someone was looking at my site.
#d3hydr8[at]gmail[dot]com

import time, re, sys

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def getips(ip):

	log = open(file, "r")
	logs = log.readlines()
	log.close()
	
	new_ip = re.findall("\d*\.\d*\.\d*\.\d*", logs[-3])
	if new_ip != ip:
		print new_ip[0],"\aviewed at:",timer() #edit out \a for no beep
		ip = new_ip
	return ip
		
if len(sys.argv) != 2:
	print "\nUsage: ./logcheck.py <access file>"
	print "ex. ./logcheck.py /var/log/apache/access_log\n"
	sys.exit(1)
	
file = sys.argv[1] 
print "\nStarting logchecker at",timer(),"\n"
ip = ""
while True:
	time.sleep(60)  #time in secs 
	ip = getips(ip)
	getips(ip)
