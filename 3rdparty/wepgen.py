#!/usr/bin/python
#Generates a wep key from pass phrase or password.
#d3hydr8[at]gmail[dot]com
#http://darkcode.ath.cx

import sys, binascii, re

if len(sys.argv) != 2:
	print "Usage: ./wepgen.py <pass phrase>"
	sys.exit(1)

key = binascii.b2a_hex(sys.argv[1])
finalkey = ""
set = re.findall("\w\w\w\w", key)
num = 0
while len(set) != num:
	if num == 0:
		finalkey = finalkey + set[num]
		key = key.replace(set[num],"")
	else:
		finalkey = finalkey + "-"+set[num]
		key = key.replace(set[num],"")
	num +=1
finalkey = finalkey + "-"+key
print "\nWEP key:",finalkey,"\n"

	



	


	



