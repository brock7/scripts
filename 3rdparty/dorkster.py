#!/usr/bin/python
#Google Dork creator/verifier
#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com

import re, urllib2, sys, time, sets

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com Dorkster v1.0"
	print "\t-----------------------------------------------"
	
def usage():
	title()
	print "\n  Usage: python dorkster.py <option>\n"
	print "\n  Example: python dorkster.py -a phpBB -f login.php -verbose\n"
	print "\t[options]"
	print "\t   -a/-app <application> : Web app you want to search for."
	print "\t   -f/-file <file> : File you want to search for."	
	print "\t   -v/-verbose : Lists the first 10 sites and unsuccessful dorks"

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

def gethits(dork):
	
	url = 'http://www.google.com/search?hl=en&q='+re.sub("\s","+",dork)+'&hl=en&lr=&start=10&sa=N'
	opener = urllib2.build_opener(url)
	opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
	data = opener.open(url).read()
	hits = re.findall('of about <b>[\d+,]*<',data)
	hosts = re.findall(('www\.[\w\.\-/]*\.\w+'),StripTags(data))
	if len(hits) >=1:
		hits = hits[0].split(">",1)[1].replace("<","")
		print "\n[+] Dork:",dork
		print "\tHits:",hits
		hosts = list(sets.Set(hosts))
		if verbose == 1 and len(hosts) >=1:
			for host in hosts[:10]:
				print "\t\t[-]",host
	else:
		if verbose == 1:
			print "\n[-] Dork:",dork

if len(sys.argv) <= 2:
	usage()
	sys.exit(1)
else:
	title()
print "[+] Dorkster_Loaded"
for arg in sys.argv[1:]:
	if arg.lower() == "-a" or arg.lower() == "-app":
		app = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-f" or arg.lower() == "-file":
		vfile = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
try:
	if app:
		print "[+] Application:",app
except(NameError):
	app = None
	pass	
try:
	if vfile:
		print "[+] Vulnerable File:",vfile
except(NameError):
	vfile = None
	pass
try:
	if verbose ==1:
		print "[+] Verbose Mode On"
except(NameError):
	verbose = 0
	print "[-] Verbose Mode Off"
print "[+] Started:",timer(),"\n"
try:
	dorks_both = ["filetype:"+vfile.rsplit(".",1)[1]+" intext:"+app, 
			"intitle:"+app+" ext:"+vfile.rsplit(".",1)[1],
			"intitle:"+app+" inurl:"+vfile,
			app+" inurl:"+vfile,
			"inurl:"+vfile+ "intext:"+app,
			"intitle:"+app+" allinurl:"+vfile]
except(NameError, AttributeError, TypeError):
	pass
try:
	vfile_dorks = ["inurl:"+vfile+" filetype:"+vfile.rsplit(".",1)[1],
				"inurl:"+vfile,
				"allinurl:"+vfile]
except(NameError, AttributeError, TypeError):
	pass
try:
	app_dorks = ["Powered by "+app,
				"intitle:"+app,
				"allintitle:"+app,
				"\""+app+"\" intitle:index.of",
				"allintext:\""+app+"\"",
				"intitle:"+app+" intitle:login"]
except(NameError, AttributeError, TypeError):
	pass

if vfile != None and app != None:
	for dork in dorks_both:
		gethits(dork)
if app != None:
	for dork in app_dorks:
		gethits(dork)
if vfile != None:
	for dork in vfile_dorks:
		gethits(dork)
print "\n[-] Done -",timer(),"\n"

	
	
	
	
	
	