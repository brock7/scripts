#!/usr/bin/python
#Decodes base64 string into hex.
#like t6vC0NdNP0+BmXa1XfI4QQ==

import sys, base64, binascii

if len(sys.argv) != 2:
	print "Usage: ./base64tohex.py <string>"
	sys.exit(1)

b = base64.b64decode(sys.argv[1])
print "\nBinary value:",b,"\n"

print "Hex value:",binascii.b2a_hex(b)
print "Length:",len(binascii.b2a_hex(b))

"""
Example:
	
python base64tohex.py t6vC0NdNP0+BmXa1XfI4QQ==

Binary value:  #^&v0!*

Hex value: b7abc2d0d74d3f4f819976b55df23841
Length: 32

"""