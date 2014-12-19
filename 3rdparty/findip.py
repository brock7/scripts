#!/usr/bin/python
#d3hydr8[at]gmail[dot]com
#Utility to find and list ips from a file.

import re, sys

if len(sys.argv) != 2:
	print "\nUsage: ./findip.py <full path to file>\n"
	sys.exit(1)
	
file = sys.argv[1]

text_file = open(file, "r").readlines()

for line in text_file:
	ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", line)
	if ipaddr: print ipaddr[0]
	
	
		
		
	
	
