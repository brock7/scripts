#!/usr/bin/python
#Reads your apache log file for all ips and prints
#where they are coming from. Use access_log or error_log.
#d3hydr8[at]gmail[dot]com 

import urllib, sys, re, time
 
if len(sys.argv) != 2:
	print "\nUsage: ./logreader.py <full path to apache log file>\n"
	sys.exit(1)

ip_list = []
file = sys.argv[1]

try:
	log = open(file, "r")
except(IOError), msg: 
	print "Check your apache log file path, Do you have permission to read it?"
	print msg
	sys.exit(1)
i = log.readlines()

for line in i:
	ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", line)
	if ipaddr not in ip_list:  
		ip_list.append(ipaddr)
			
print "\nFound",len(ip_list),"ips to search.\n"

for ip in ip_list:
	try:
		url = "http://antionline.com/tools-and-toys/ip-locate/index.php?address="+ip[0]
	except(IndexError): print "Not a real ip address."
	
	time.sleep(3)  #Stops working without a pause.
	
	site = urllib.urlopen(url).readlines()
	
	
	for line in site:
		if re.search("<br><b>", line):
			line = line.replace("</b>","").replace('<br>',"").replace('<b>',"")
			print "\n",line,"\n"