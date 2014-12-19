#!/usr/bin/python
#Searches the internet for email 
#addresses, prints them to a file...

#Changelog: added socket timeout for lag sites 
#and writes to the file as soon as an address is found 
#incase of a crash.

#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com 

import urllib, sys, re, random, socket, time

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com EmailCollecter v1.1"
	print "\t--------------------------------------------------\n"
	
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)
	
def geturls(url):
	
	try:
		print "Collecting:",url
		site = urllib.urlopen(url).read()
		links = re.findall(('http://\w+.\w+\.\w+'), site)
		for link in links:
			if link not in urls:
				urls.append(link)
	except(IOError,TypeError,AttributeError,socket.timeout, socket.gaierror, socket.error): pass
	return urls
		
def getaddress(url):
	
	print "Checking:",url
	try:
		site = urllib.urlopen(url).read()
		emails = re.findall('[\.\w]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}', site)
		for email in emails:
			if email not in addresses:
				addresses.append(email)
				file.writelines(email+"\n")
				print "\nFound:",email,"\nTotal:",len(addresses),"\n"
				
	except(IOError,TypeError,AttributeError,socket.timeout,socket.gaierror,socket.error): pass	
		
	return addresses
	
if len(sys.argv) != 4:
	title()
	print "\nUsage: ./emailcollect.py <starting point> <file to save addreses> <how many>"
	print "Ex: ./emailcollect.py www.busywebsite.com emails.txt 10000\n"
	sys.exit(1)
	
url = sys.argv[1]
length = int(sys.argv[3])
	
if url[:7] != "http://":
	url = "http://"+url

addresses = []
urls = []
socket.setdefaulttimeout(3)

title()
print "[+] Starting:",url
print "[+] File:",sys.argv[2]
print "[+] Collecting:",length
print "[+] Started:",timer(),"\n"

urls = geturls(url)
file = open(sys.argv[2], "a")

while int(len(addresses)) < length:

	addresses = getaddress(random.choice(urls))
	if len(urls) < 1000:
		urls = geturls(random.choice(urls))
	else:
		for url in urls[1:300]:
			urls.remove(url)

print "\n[+] Final Total:",len(addresses)
print "[+] Data:",sys.argv[2]
file.close()
print "[+] Done",timer(),"\n"


	


	
	



