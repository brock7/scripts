#!/usr/bin/python
#Attempts to collect all webapp
#exploits from milw0rms DB.

import urllib2, time, os, re, urllib

HOME_DIR = "/home/d3hydr8/exploits"
site = "http://www.milw0rm.com/webapps.php?start="
#Time to wait between page loads (in secs)
TIME = "3"

#Make sure HOME_DIR ends with a "/"
if HOME_DIR[-1] != "/":
	HOME_DIR = HOME_DIR+"/"
print "\n[+] Dir:",HOME_DIR,"\n"
HOME_DIR = HOME_DIR+"milw0rm/"

try:
	os.chdir(HOME_DIR)
except(OSError):
	os.mkdir(HOME_DIR)
	os.chdir(HOME_DIR)
	
start = 0
error = 0
while error != 3:
	try:
		time.sleep(int(TIME))
		print "[+] Page:",start
		source = urllib2.urlopen(site+str(start), "80").read()
		xplts = re.findall("href=\"/exploits/\d+",source)
		print "[+] Exploits Found:",len(xplts)
	except(urllib2.URLError):
		xplt = []
		pass
	for xplt in xplts:
		time.sleep(0.5)
		xplt = xplt.replace("href=\"","")
		urllib.urlretrieve("http://www.milw0rm.com"+xplt, HOME_DIR+xplt.rsplit("/",1)[1])
	if len(xplt) == 0:
		error +=1
	start +=30
print "\n[!] Operation Complete\n"
