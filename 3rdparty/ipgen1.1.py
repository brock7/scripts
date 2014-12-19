#!/usr/bin/env python
#Random IP generater for nmap -DECOY

#Version 1.1 will test ips before printing.

#whoami project

#http://darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, random, re, socket

def randip():
	
	A = random.randrange(255) + 1
	B = random.randrange(255) + 1
	C = random.randrange(255) + 1
	D = random.randrange(255) + 1
	ip = "%d.%d.%d.%d" % (A,B,C,D)
	return ip


print "\n   d3hydr8[at]gmail[dot]com IPgen v1.1"
print "----------------------------------------\n"
if len(sys.argv) < 2:
	print "Usage: ./ipgen.py <how many?>\n"
	sys.exit(1)
	
print "[+] Testing...\n"
	
ips = []
while len(ips) != (int(sys.argv[1])):
	ip = randip()
	try:
		hn = socket.gethostbyaddr(ip)[0]
		print "[+] Found:",hn,"|",ip
		ips.append(ip)
	except(socket.herror):
		pass
	
ips = str(ips)

ips = ips[1:-1].replace("'","")
print "\n"
print re.sub("\s","",ips)
print "\nDone\n"