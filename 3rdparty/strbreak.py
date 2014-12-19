#!/usr/bin/python
#String break, takes a list of sites and splits
#them at the "=" and adds your own extension.

#Can write to a file or print to the screen

#tosin22001 project

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import sys

if len(sys.argv) not in [3,5]:
	print "\nUsage: ./strbreak.py <list> <extension>"
	print "\t[options]"
	print "\t   -f/-file <file to save> : Save generated strings to file\n"
	sys.exit(1)
	

for arg in sys.argv[1:]:
	if arg.lower() == "-f" or arg.lower() == "-file":
		ofile = sys.argv[int(sys.argv[1:].index(arg))+2]

try:
  sites = open(sys.argv[1], "r").readlines()
except(IOError): 
  print "Error: Check your site list path\n"
  sys.exit(1)
  
ext = sys.argv[2]
if ext[0] != "=":
	ext = "="+ext
  
print "\n[+] Sites Loaded:",len(sites)
print "[+] Extension:",ext
  
try:
	if ofile:
		output_file = open(ofile, "a")
		print "[+] Output File:",ofile
except(NameError):
	output_file = None
	print "[+] Output File: None\n"
	pass
	

for site in sites:
	site = site.replace("\n","")
	new = site.split("=",1)[0]+ext
	if output_file != None:
		output_file.writelines(new+"\n")
		print "\n[+] Writing Data...\n"
		print new
	else:
		print new
if output_file != None:
	output_file.close()




	
	



