#!/usr/bin/python
#This utility will check multiple files 
#checksums for changes and log the 
#changes to a log file. Just fill in the
#3 arguments below.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, md5, time

#The list of files to monitor
FILES = ["/home/d3hydr8/test.txt","/home/d3hydr8/test1.txt"]
#Time in seconds to check for change
TIME = "300"
#Logfile to write changes
LOGFILE = "/home/d3hydr8/messages"

def sumfile(fobj):
	m= md5.new()
	while True:
		d= fobj.read(8096)
		if not d:
			break
		m.update(d)
	return m.hexdigest()

def md5sum(fname):
	if fname == '-':
		ret = sumfile(sys.stdin)
	else:
		try:
			f = open(fname, 'rb')
		except:
			return 'Failed to open file'
		ret = sumfile(f)
		f.close()
	return ret

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

filedic = {}
#print "\n[+] Files Loaded:",len(FILES)
for fname in FILES:
	hash =  md5sum(fname)
	filedic[fname] = hash

while 1:
	time.sleep(int(TIME))
	log = open(LOGFILE, "a")
	for k,v in filedic.items():
		hash =  md5sum(k)
		if hash != v:
			#print "\n[-] Found Change:",k
			#print "[-] Time:",timer()
			log.writelines("\n[-] Found a change: "+k+"\n")
			log.writelines("[-] From: "+v+"\n")
			log.writelines("[-] To: "+hash+"\n")
			log.writelines("[-] Time: "+timer()+"\n")
			log.close()
			filedic[k] = hash



