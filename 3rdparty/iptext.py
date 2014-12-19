#!/usr/bin/python
#saves random ips to a text file
#d3hydr8[at]gmail[dot]com
import random, sys

if len(sys.argv) != 3:
	print "\nUsage: ./iptext.py <how many> <saved file>\n"
	sys.exit(1)

count = 0

while count != int(sys.argv[1]):
	
	count += 1

	A = random.randrange(255) + 1
	B = random.randrange(255) + 1
	C = random.randrange(255) + 1
	D = random.randrange(255) + 1

	ip = "\n""%d.%d.%d.%d" % (A,B,C,D)

	file = open(sys.argv[2], "a")
	file.writelines(ip)
	file.close()
print "\nALL DONE\n"
