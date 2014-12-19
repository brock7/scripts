#!/usr/bin/python
#Password generater that uses type and length.
#There are 4 types to use: alphanum, alpha, alphacap, all
#d3hydr8[at]gmail[dot]com

import random, sys

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com Password Gen v1.1"
	print "\t-----------------------------------------------\n"
	
def passgen(choice, length):
	
	passwd = ""
	
	alphanum = ('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
	alpha = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
	alphacap = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	all = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=~`[]{}|\:;"\'<>,.?/')
	
	if str(choice).lower() == "alphanum":
		choice = alphanum

	elif str(choice).lower() == "alpha":
		choice = alpha
			
	elif str(choice).lower() == "alphacap":
		choice = alphacap
	
	elif str(choice).lower() == "all":
		choice = all
		
	else: 
		print "Type doesn't match\n"
		sys.exit(1)
		
	return passwd.join(random.sample(choice, int(length)))
		
title()
if len(sys.argv) <= 3 or len(sys.argv) == 5:
	print "\nUsage: ./passgen.py <type> <length of password> <how many>"
	print "\t[options]"
	print "\t   -w/-write <file> : Writes passwords to file\n"
	print "There are 4 types to use: alphanum, alpha, alphacap, all\n"
	sys.exit(1)

for arg in sys.argv[1:]:
	if arg.lower() == "-w" or arg.lower() == "-write":
		txt = sys.argv[int(sys.argv[1:].index(arg))+2]

if sys.argv[3].isdigit() == False:
	print sys.argv[3],"must be a number\n"
	sys.exit(1)
if sys.argv[2].isdigit() == False:
	print sys.argv[2],"must be a number\n"
	sys.exit(1)
try:
	if txt:
		print "[+] Writing Data:",txt
		output = open(txt, "a")
except(NameError):
	txt = None
	pass

for x in xrange(int(sys.argv[3])):
	if txt != None:
		output.writelines(passgen(sys.argv[1],sys.argv[2])+"\n")
	else:
		print "Password:",passgen(sys.argv[1],sys.argv[2])
print "\n[-] Done\n"