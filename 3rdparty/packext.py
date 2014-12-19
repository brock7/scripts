#!/usr/bin/python
#This script will extract all exploits
#from packetstorm from 2000-previous year.

#http://darkc0de.com
#d3hydr8[at]gmail[dot]com

import urllib, tarfile, os, sys, time

HOME_DIR = "/home/d3hydr8/exploits/"
YEARS = ["00","01","02","03","04","05","06","07"]

#Time check
now = time.strftime("%Y", time.localtime())[2:]
print "\n[+] Checking Years\n"
if now == YEARS[-1]:
	print "[!] The last year in YEARS cannot be the present year.\n"
	sys.exit(1)
else:
	print "Last year:",YEARS[-1],"Current Year:",now
	resp = raw_input("\nIs this correct? Yes or No ").lower()
	if resp == "no":
		print "\n[!] Modify YEARS list correctly.\n"
		sys.exit(1)
	elif resp == "yes":
		print "\n[+] Starting extraction"
	else:
		print "\nHUH?\n"
		sys.exit(1)

#Make sure HOME_DIR ends with a "/"
if HOME_DIR[-1] != "/":
	HOME_DIR = HOME_DIR+"/"
print "[+] Dir:",HOME_DIR,"\n"
try:
	os.chdir(HOME_DIR)
except(OSError):
	os.mkdir(HOME_DIR)
	os.chdir(HOME_DIR)

#Extraction process	
for year in YEARS:
	print "Start: 20"+year
	try:
		os.chdir(HOME_DIR+year+"-exploits")
	except(OSError):
		os.mkdir(HOME_DIR+year+"-exploits")
		os.chdir(HOME_DIR+year+"-exploits")
	page = "http://packetstormsecurity.org/"+year+"12-exploits/20"+year+"-exploits.tgz"
	urllib.urlretrieve(page, "20"+year+"-exploits.tgz")

	tar = tarfile.open("20"+year+"-exploits.tgz")
	tar.extractall()
	tar.close()

	os.remove("20"+year+"-exploits.tgz")
	print "Done: 20"+year
	
print "\n[++] Operation Complete\n"

