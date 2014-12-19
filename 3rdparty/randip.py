#!/usr/bin/python
#d3hydr8[at]gmail[dot]com
#prints random ips
import random, sys

if len(sys.argv) != 2:
	print "\nUsage: ./randip.py <how many you want?>\n"
	sys.exit(1)
		 
num = int(sys.argv[1])
count = 0

while count != num:
	count += 1

	L = random.randrange(255) + 1
	I = random.randrange(255) + 1
	N = random.randrange(255) + 1
	X = random.randrange(255) + 1
	ip = "%d.%d.%d.%d" % (L,I,N,X)
	print ip

		