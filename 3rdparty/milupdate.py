#!/usr/bin/python
#Checks milw0rm.com for exploit updates.

import urllib2, time, os, re, urllib

HOME_DIR = "/home/d3hydr8/exploits"
site = "http://www.milw0rm.com/"
#Time to wait for update checks (in secs)
TIME = "300"

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

done = []
while 1:
	time.sleep(int(TIME))
	try:
		source = urllib2.urlopen(site, "80").readlines()
		for line in source:
			if re.search("class=\"style15", line):
				xplts = re.findall("href=\"/exploits/\d+", line)
	except(urllib2.URLError):
		xplts = []
		pass
	if len(xplts) >=1:
		for xplt in xplts:
			if xplt not in done:
				done.append(xplt)
				xplt = xplt.replace("href=\"","")
				print "[+] Adding: http://www.milw0rm.com"+xplt
				urllib.urlretrieve("http://www.milw0rm.com"+xplt, HOME_DIR+xplt.rsplit("/",1)[1])
		print "[+] Collected:",len(done),"exploits\n"

