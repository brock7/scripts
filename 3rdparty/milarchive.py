#!/usr/bin/python
#Extracts exploit archive for remote 
#ports and platforms from milw0rm.

import urllib, tarfile, os

HOME_DIR = "/home/d3hydr8/"

#Make sure HOME_DIR ends with a "/"
if HOME_DIR[-1] != "/":
	HOME_DIR = HOME_DIR+"/"
print "\n[+] Dir:",HOME_DIR,"\n"

try:
	os.chdir(HOME_DIR)
except(OSError):
	os.mkdir(HOME_DIR)
	os.chdir(HOME_DIR)
print "[!] Downloading file..."
page = "http://www.milw0rm.com/sploits/milw0rm.tar.bz2"
urllib.urlretrieve(page, "milw0rm.tar.bz2")
print "[!] Extracting files..."
tar = tarfile.open("milw0rm.tar.bz2")
tar.extractall()
tar.close()
os.remove("milw0rm.tar.bz2")
print "\n[!] Operation Complete\n"

#Or
#wget http://www.milw0rm.com/sploits/milw0rm.tar.bz2
#tar -xjvf milw0rm.tar.bz2
#rm milw0rm.tar.bz2
#:)



