#!/usr/bin/env python
#Random IP generater.

#whoami project

#http://darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, random, re

def randip():
	
	A = random.randrange(255) + 1
	B = random.randrange(255) + 1
	C = random.randrange(255) + 1
	D = random.randrange(255) + 1
	ip = "%d.%d.%d.%d" % (A,B,C,D)
	return ip


print "\n   d3hydr8[at]gmail[dot]com IPgen v1.0"
print "----------------------------------------\n"
if len(sys.argv) < 2:
	print "Usage: ./ipgen.py <how many?>\n"
	sys.exit(1)
	
ips = []
for x in xrange(int(sys.argv[1])):
	ips.append(randip())
	
ips = str(ips)

ips = ips[1:-1].replace("'","")
print re.sub("\s","",ips)