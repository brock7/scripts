#!/usr/bin/python
#Searches the internet for email 
#addresses, prints them to a file...

#Changelog v1.3: added finding tricky addresses like d3hydr8[at]gmail[dot]com
#and addresses like d3hydr8[at]gmail.com

#Changelog v1.2: adding the ability to search for a specific
#domain (ex: gmail.com / yahoo.com). It also uses google first to 
#find addresses. Also added "verbose mode" which will show the sites
#your collecting from or not. Also fixed a regex problem.


#Changelog v1.1: added socket timeout for lag sites 
#and writes to the file as soon as an address is found 
#incase of a crash.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import urllib, sys, re, random, socket, time, urllib2, string, sets

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com EmailCollecter v1.3"
	print "\t--------------------------------------------------\n"
	
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def StripTags(text):
    finished = 0
    while not finished:
        finished = 1
        start = text.find("<")
        if start >= 0:
            stop = text[start:].find(">")
            if stop >= 0:
                text = text[:start] + text[start+stop+1:]
                finished = 0
    return text
 
def getgoog(domain):
	counter = 0
	goog_emails = []
	try:
		while counter < 100:
			results = 'http://groups.google.com/groups?q='+str(domain)+'&hl=en&lr=&ie=UTF-8&start=' + repr(counter) + '&sa=N'
			request = urllib2.Request(results)
			request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
			opener = urllib2.build_opener()  
			text = opener.open(request).read()
			emails = (re.findall('([\w\.\-]+@'+domain+')',StripTags(text)))
			for email in emails:
				goog_emails.append(email)
			counter += 10
		page_counter = 0
		while page_counter < 100 :
			results_web = 'http://www.google.com/search?q=%40'+str(domain)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
			request_web = urllib2.Request(results_web)
			request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
			opener_web = urllib2.build_opener()  
			text = opener_web.open(request_web).read()
			emails_web = (re.findall('([\w\.\-]+@'+domain+')',StripTags(text)))
			for email_web in emails_web:
				goog_emails.append(email_web)
			page_counter += 10
	
		goog_emails = list(sets.Set(goog_emails))
		return goog_emails
	except(IndexError):
		pass
	
def geturls(url):
	
	try:
		if verbose == 1:
			print "Collecting:",url
		site = urllib.urlopen(url).read()
		links = re.findall(('http://[\w\.\-]*'), site)
		for link in links:
			if link not in urls:
				urls.append(link)
	except(IOError,TypeError,AttributeError,socket.timeout, socket.gaierror, socket.error): pass
	return urls
		
def getaddress(url):
	
	if verbose == 1:
		print "Checking:",url
	try:
		emails = []
		site = urllib.urlopen(url).read()
		try:
			if domain:
				emails = re.findall('[\w\.\-]+@'+domain, site)
				t1 = re.findall('[\w\.\-]+\[at\]'+domain, site)
				t2 = re.findall('[\w\.\-]+\[at\]'+re.sub("\.","\[dot\]",domain), site)
				if len(t1) >= 1:
					for addr in t1:
						emails.append(addr.replace("[at]","."))
				if len(t2) >= 1:
					for addr in t2:
						emails.append(addr.replace("[at]",".").replace("[dot]","."))
		except(NameError):
			emails = re.findall('[\.\w]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}', site)
			t1 = re.findall('[\w\.\-]+\[at\][\w\.\-]+\.\w\w\w', site)
			t2 = re.findall('[\w\.\-]+\[at\][\w\.\-]+\[dot\]\w\w\w', site)
			if len(t1) >= 1:
				for addr in t1:
					emails.append(addr.replace("[at]","@"))
			if len(t2) >= 1:
				for addr in t2:
					emails.append(addr.replace("[at]",".").replace("[dot]","."))
			pass
		if len(emails) >=1:
			data = open(sys.argv[2], "a")
			for email in emails:
				if email not in addresses:
					addresses.append(email)
					data.writelines(email+"\n")
					print "\nFound:",email,"\nTotal:",len(addresses),"\n"
			data.close()
				
	except(IOError,TypeError,AttributeError,socket.timeout,socket.gaierror,socket.error): 
		pass
	except(KeyboardInterrupt):
		pass	
	return addresses
			
if len(sys.argv) < 4 or len(sys.argv) > 7:
	title()
	print "\nUsage: ./emailcollect.py <starting point> <file to save addreses> <how many> <options>"
	print "Ex: ./emailcollect.py www.busywebsite.com emails.txt 10000 -domain gmail.com -verbose\n"
	print "\t[options]"
	print "\t   -d/-domain <domain> : Only searches for that domain (ex: gmail.com, yahoo.com)"
	print "\t   -v/-verbose : Verbose Mode\n"
	sys.exit(1)
	
url = sys.argv[1]
length = int(sys.argv[3])

for arg in sys.argv[1:]:
	if arg.lower() == "-d" or arg.lower() == "-domain":
		domain = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
	
if url[:7] != "http://":
	url = "http://"+url

addresses = []
urls = []
socket.setdefaulttimeout(3)

title()
print "[+] Starting:",url
print "[+] File:",sys.argv[2]
try:
	if domain:
		domain = re.sub("@","",domain)
		print "[+] Domain:",domain
except(NameError):
	print "[+] Searching: all domains"
	pass
print "[+] Collecting:",length
try:
	if verbose ==1:
		print "[+] Verbose Mode On"
except(NameError):
	verbose = 0
	print "[-] Verbose Mode Off"
print "[+] Started:",timer(),"\n"

try:
	if domain:
		print "[+] Getting addresses from google...\n"
		goog_emails = getgoog(domain)
		print "[+] Found:",len(goog_emails),"from google."
		if len(goog_emails) >= 1:
			file = open(sys.argv[2], "a")
			for e in goog_emails:
				file.writelines(e+"\n")
				addresses.append(e)
		file.close()
except(NameError):
	pass

if int(len(addresses)) < length: 
	urls = geturls(url)

while int(len(addresses)) < length:
	
	try:
		addresses = getaddress(random.choice(urls))
	except(IndexError):
		print "[-] Ran out of links, try another start site\n"
		sys.exit(1)
	if len(urls) < 1000:
		urls = geturls(random.choice(urls))
	else:
		for url in urls[1:300]:
			urls.remove(url)

print "\n[+] Final Total:",len(addresses)
print "[+] Data:",sys.argv[2]
print "[+] Done",timer(),"\n"