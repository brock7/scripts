#!/usr/bin/python
#Decodes/Encodes a file with ROT13 encryption.
#d3hydr8[at]gmail[dot]com

import sys, string

if len(sys.argv) != 2:
	print "\nUsage: ./rot13.py <file>\n"
	sys.exit(1)
	
file = sys.argv[1]
try:
	i = open(file, "r")
except(IOError): 
	print "Check your file path."
	sys.exit(1)
	
table = string.maketrans(
	'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM',
	'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

for x in i:
	print string.translate(x, table)