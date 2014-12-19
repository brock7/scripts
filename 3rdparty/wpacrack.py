#!/usr/bin/python
#Cracks a 256-bit WPA-PSK hash (64 char) using wpa_passphrase
#and a wordlist.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import md5, sys, commands, getopt, StringIO, re

def gethash(word):
	cmd = "wpa_passphrase "+sys.argv[2]+" "+word
	out = StringIO.StringIO(commands.getstatusoutput(cmd)[1]).read()
	hash = re.findall("[a-f0-9]"*64,out)
	if len(hash) > 0:
		return hash[0]

if len(sys.argv) != 4:
	print "Usage: ./wpacrack.py <hash> <ssid> <wordlist>"
	sys.exit(1)

if len(sys.argv[1]) != 64:
  print "\nError: Hash length incorrect (64 char)\n"
  sys.exit(1)
	
try:
  words = open(sys.argv[3], "r").readlines()
except(IOError): 
  print "\nError: Check your wordlist path\n"
  sys.exit(1)

print "\n",len(words),"words loaded..."
for word in words:
	hash = gethash(word.replace("\n",""))
	if sys.argv[1] == hash: 
		print "Password is:",word

	
	



