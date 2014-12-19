#!/usr/bin/python
#Proxy tester

#d3hydr8[at]gmail[dot]com
#http://www.darkc0de.com

"""File Format: 
	
82.137.247.62:80
200.150.233.34:8080
220.247.214.178:8080

"""

import sys, urllib, socket
socket.setdefaulttimeout(5) #Set your socket timeout here.

def main(proxy):
	
	try:# make a http HEAD request
		proxies = {'http': "http://"+proxy[:-1]}
		opener = urllib.FancyURLopener(proxies)
		opener.open("http://www.python.org")
		print "\t[+] Alive"
	except(IOError), msg: 
		if verbose == 1:
			print "\t[-] Error:",msg
		pass

if len(sys.argv) not in [2,3]:
	print "\nUsage: ./proxytest.py <file> <option>"
	print "\t[options]"
	print "\t   -v/-verbose : Verbose Mode"
	sys.exit(1)
	
for arg in sys.argv[1:]:
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
	
try:
	lines = open(sys.argv[1], "r").readlines()

	print "\n\td3hydr8[at]gmail[dot]com Proxy Tester v1.1"
	print "\t-------------------------------------------"
	print "\n[+] Proxies loaded:",len(lines)
	try:
		if verbose == 1:
			print "[+] Verbose Mode On\n"
	except(NameError):
		print "[-] Verbose Mode Off\n"
		verbose = 0
		pass
except(IOError): 
 	print "Error: Check your file path.\n" 
	sys.exit(1)
	
for proxy in lines:
	print "[+] Testing:",proxy[:-1]
	main(proxy)
print "\n[-] Done\n"

	