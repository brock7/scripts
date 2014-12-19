#!/usr/bin/python
#Decodes a string using Base64. (very basic, just messing around)
#d3hydr8[at]gmail[dot]com
import base64, sys

if len(sys.argv) != 2:
	print "\nUsage: ./decoder.py <file w/ str to decode>\n"
	sys.exit(1)
	
file = sys.argv[1]
try:
	i = open(file, "r")
except(IOError): 
	print "Check your file path."
	sys.exit(1)
lines = i.readlines()
for line in lines:
	try:
		x = base64.b64decode(line[:-1], '-_')
		print x
	except(TypeError): 
		print "\nIncorrect Padding or non-alphabet characters present in the string.\n"
					
"""

sh-3.00$ cat wh.txt
whitehouse.com root password: jackass

sh-3.00$ python encoder.py wh.txt
d2hpdGVob3VzZS5jb20gcm9vdCBwYXNzd29yZDogamFja2FzcyA=

sh-3.00$ cat wh.txt  #copy and pasted encoded to wh.txt
d2hpdGVob3VzZS5jb20gcm9vdCBwYXNzd29yZDogamFja2FzcyA=

sh-3.00$ python decoder.py wh.txt
whitehouse.com root password: jackass """