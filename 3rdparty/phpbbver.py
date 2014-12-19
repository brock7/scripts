#!/usr/bin/python
#Searches google for phpBB versions using the 
#/docs/CHANGELOG.html.
#d3hydr8[at]gmail[dot]com

import urllib2, sys, re, string, urllib

def gethosts(q):
	
	counter =  10
	hits = []
	
	while counter < num:
		url = 'http://www.google.com/search?hl=en&q=%22'+q+'%22&hl=en&lr=&start='+repr(counter)+'&sa=N'
		opener = urllib2.build_opener(url)
		opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
		data = opener.open(url).readlines()
		for line in data:
			hit = re.findall("\w+\.\w+\.?\w+./?\w+./?\w+./", line)
			for x in hit:
				if x != []:
					#Lets get rid of the nonsense and google hosts..this could
					#be done with a better regex but i havn't recieved one yet
					if re.search(r'\(', x) or re.search("<", x) or re.search("google", x): pass
					else: 
						if x not in hits: hits.append(x)
													
		counter += 10
	print "\n\tLoaded",len(hits),"hosts...\n"
	return hits
			
def scanner(hits):
	
	#add more directorys here
	dirs = ["/","/bb/","/phpbb/","/forum/","/forums/","/phpBB2/","/phpbb/phpBB2/"]
	
	for url in hits:
		for d in dirs:
			if url[:7] != "http://":
				url = "http://"+url
			host = url[:-1]+d+"docs/CHANGELOG.html"
			try:
				print "Trying -",host
				site = urllib.urlopen(host).readlines()
			except(urllib2.HTTPError,IOError):
				pass
			for line in site:
				hit = re.findall("<title>phpBB", line)
				if hit != []:
					print "\n\tFound:",line.replace("<title>","").replace("</title>",""),"\n"
	
#................................................
	
if len(sys.argv) != 2:
	print "Usage ./phpbbver.py <num of hosts>"
	sys.exit(1)
else:
	#add more querys here
	query = ["Powered+by+phpBB", "inurl:/phpbb/", "inurl:/phpBB2/"]
	num = int(sys.argv[1])
	for q in query:
		print "\nQuery:",q
		scanner(gethosts(q))
