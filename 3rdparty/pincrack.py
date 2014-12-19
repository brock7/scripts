#!/usr/bin/env python
#This will crack any 4 digit number in 6 different encryptions.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, base64

try: 
	import hashlib
except(ImportError):
	print "\n[-] You need the hashlib module installed, upgrade to python 2.5\n" 	
	sys.exit(1)

def show(first):
	if sys.argv[2] == "md5":
		if sys.argv[1] == hashlib.md5(''.join(first)).hexdigest():
	    		print "\n\t[!] Cracked:",''.join(first),"\n"
	if sys.argv[2] == "sha1":
		if sys.argv[1] == hashlib.sha1(''.join(first)).hexdigest():
	    		print "\n\t[!] Cracked:",''.join(first),"\n"
	if sys.argv[2] == "sha224":
		if sys.argv[1] == hashlib.sha224(''.join(first)).hexdigest():
	    		print "\n\t[!] Cracked:",''.join(first),"\n"
	if sys.argv[2] == "sha256":
		if sys.argv[1] == hashlib.sha256(''.join(first)).hexdigest():
	    		print "\n\t[!] Cracked:",''.join(first),"\n"
	if sys.argv[2] == "sha384":
		if sys.argv[1] == hashlib.sha384(''.join(first)).hexdigest():
	    		print "\n\t[!] Cracked:",''.join(first),"\n"
	if sys.argv[2] == "sha512":
		if sys.argv[1] == hashlib.sha512(''.join(first)).hexdigest():
	    		print "\n\t[!] Cracked:",''.join(first),"\n"

def main(first, start, second=[]):
	if not start: return show(second)
    	for i in range(len(first)):
        	second.append(first.pop(i))
        	main(first, start-1, second)
        	first.insert(i, second.pop())

if len(sys.argv) != 3:
	print "\nUsage: ./pincrack.py <string> <type>\n"
	print "\tTypes: md5, sha1, sha224, sha256, sha384, sha512\n"
	sys.exit(1)
	
print "\n   d3hydr8[at]gmail[dot]com PinCrack v1.0"
print "--------------------------------------------"
	
sys.argv[2] = sys.argv[2].lower()
	
if sys.argv[2] == "md5":
	if len(sys.argv[1]) != 32:
		print "\n[-] Inproper length for md5 hash.\n"
		sys.exit(1)
		
if sys.argv[2] == "sha1":
	if len(sys.argv[1]) != 40:
		print len(sys.argv[1])
		print "\n[-] Inproper length for sha1 hash.\n"
		sys.exit(1)
		
if sys.argv[2] == "sha224":
	if len(sys.argv[1]) != 56:
		print "\n[-] Inproper length for sha224 hash.\n"
		sys.exit(1)
		
if sys.argv[2] == "sha256":
	if len(sys.argv[1]) != 64:
		print "\n[-] Inproper length for sha256 hash.\n"
		sys.exit(1)
		
if sys.argv[2] == "sha384":
	if len(sys.argv[1]) != 96:
		print "\n[-] Inproper length for sha384 hash.\n"
		sys.exit(1)
		
if sys.argv[2] == "sha512":
	if len(sys.argv[1]) != 128:
		print "\n[-] Inproper length for sha512 hash.\n"
		sys.exit(1)

print "\n[+] String:",sys.argv[1]
print "[+] Encryption:",sys.argv[2]
main(list("0123456789"), 4)