#!/usr/bin/python
#Attempts to crack hash using random strings from 
#a key length and alpha type. 
#d3hydr8[at]gmail[dot]com 

import md5, sys, random

def passgen(choice, length):
	
	alphanum = ('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
	alpha = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
	alphalower = ('abcdefghijklmnopqrstuvwxyz')
	
	if str(choice).lower() == "alphanum":
		choice = alphanum

	elif str(choice).lower() == "alpha":
		choice = alpha
			
	elif str(choice).lower() == "alphalower":
		choice = alphalower
		
	else: 
		print "Type doesn't match\n"
		sys.exit(3)
		
	passwd = ""
	
	return passwd.join(random.sample(choice, int(length)))

#---------------------------------------------
		
if len(sys.argv) != 5:
	print "\nUsage: ./md5randcrack.py <hash> <type> <length> <number>\n"
	print "ex: ./md5randcrack.py 5f4dcc3b5aa765d61d8327deb882cf99 alphanum 7 10000\n"
	sys.exit(1)

pw = sys.argv[1]

count = 0
print "\n\t-d3hydr8[at]gmail[dot]com Random MD5 Cracker v1.0-" 
print "\n+ hash:",pw
print "+ type:",sys.argv[2]
print "+ key_length:",sys.argv[3]
print "+ attempts:",sys.argv[4],"\n"

if len(pw) != 32:
	print "Hash Incorrect\n" 
	sys.exit(2)

while count != int(sys.argv[4]):
	count +=1
	value = passgen(sys.argv[2], sys.argv[3])
	if pw == md5.new(value).hexdigest():
		print "Password:",value,"\n"
	

	



