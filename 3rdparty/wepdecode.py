#!/usr/bin/python
#Decodes a WEP key (hex to ascii)
#d3hydr8[at]gmail[dot]com
#http://darkcode.ath.cx

import sys, binascii

if len(sys.argv) != 2:
	print "Usage: ./wepdecode.py <key>"
	sys.exit(1)

key = sys.argv[1].replace("-","")

print "\nWEP key:",binascii.a2b_hex(key),"\n"
