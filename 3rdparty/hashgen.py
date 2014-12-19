#!/usr/bin/python
#Playing around with the new hashlib, generates
#6 different hashes. md5,sha1,sha224,sha256,sha384,sha512

import sys 

try: 
	import hashlib
except(ImportError):
	print "\nYou need the hashlib module installed, try upgrading to python 2.5.\n" 	
	sys.exit(1) 

if len(sys.argv) != 2:
	print "Usage: ./hashgen.py <password>"
	sys.exit(1)
	
pw = sys.argv[1]

hash = hashlib.md5(pw)
print "\nMD5:",hash.hexdigest(),"\n"

hash = hashlib.sha1(pw)
print "SHA1:",hash.hexdigest(),"\n"

hash = hashlib.sha224(pw)
print "SHA224:",hash.hexdigest(),"\n"

hash = hashlib.sha256(pw)
print "SHA256:",hash.hexdigest(),"\n"

hash = hashlib.sha384(pw)
print "SHA384:",hash.hexdigest(),"\n"

hash = hashlib.sha512(pw)
print "SHA512:",hash.hexdigest(),"\n"