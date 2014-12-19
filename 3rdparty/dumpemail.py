#!/usr/bin/python
#Collects email addr from database
#and writes them to a file.

#added dupe checking

#sh4rpr00ter project

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, re, sets

if len(sys.argv) != 3:
	print "\nUsage: ./dumpemail.py <database> <save file>"
	print "Example:"
	print "\t ./dumpemail.py db.sql emails.txt\n"
	sys.exit(1)

try:
  database = open(sys.argv[1], "r").read()
except(IOError): 
  print "\nError: Check your db path\n"
  sys.exit(1)
  
emails =  list(sets.Set(re.findall('[\.\w]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}', database)))
if len(emails) >= 1:
	ofile = open(sys.argv[2], "a")
	print "\nFound:",len(emails)
	print "Writing to file:",sys.argv[2],"\n\n"
	for e in emails:
		print e
		ofile.writelines(e+"\n")
	ofile.close()
else:
	print "\n[-] No email addresses found\n"
print "\n[+] Done\n"
	





	
	



