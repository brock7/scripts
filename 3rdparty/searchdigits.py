#!/usr/bin/python
#Uses google,msn,yahoo and altavista to find phone numbers 
#(don't know why you would need this)

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, re, string, urllib2, sets

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
		  
def getgoog(lang):
	
	page_counter=0
	try:
    		while page_counter < 50:
        		results_web = 'http://www.google.com/search?q='+str(query)+'&hl='+str(lang)+'&lr=&ie=UTF-8&start='+repr(page_counter)+'&sa=N'
        		request_web = urllib2.Request(results_web)
        		request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
        		opener_web = urllib2.build_opener()                           
        		text = opener_web.open(request_web).read()
        		names = re.findall(('\d\d\d\-\d\d\d\-\d\d\d\d'),StripTags(text))
        		for name in names:
				if name not in d:
					d.append(name)
        		page_counter +=10
        
	except IOError:
    		print "[-] Can't connect to Google Web!"+""
		pass
		
def getmsn():
	
	page_counter=0
	try:
    		while page_counter < int(sys.argv[2]):
        		results_web = 'http://search.msn.com/results.aspx?q='+str(query)+'&first='+repr(page_counter)
        		request_web = urllib2.Request(results_web)
        		request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
        		opener_web = urllib2.build_opener()                           
        		text = opener_web.open(request_web).read()
        		names = re.findall(('\d\d\d\-\d\d\d\-\d\d\d\d'),StripTags(text))
			print "[+] Found:",len(names)
        		for name in names:
				if name not in d:
					d.append(name)
        		page_counter +=10
        
	except IOError:
    		print "[-] Can't connect to MSN Web!"+""
		pass
				
def getyahoo():
	
	page_counter=0
	try:
    		while page_counter < int(sys.argv[2]):
        		results_web = 'http://search.yahoo.com/search?p='+str(query)+'&b='+repr(page_counter)
        		request_web = urllib2.Request(results_web)
        		request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
        		opener_web = urllib2.build_opener()                           
        		text = opener_web.open(request_web).read()
        		names = re.findall(('\d\d\d\-\d\d\d\-\d\d\d\d'),StripTags(text))
			print "[+] Found:",len(names)
        		for name in names:
				if name not in d:
					d.append(name)
        		page_counter +=10
        
	except IOError:
    		print "[-] Can't connect to Yahoo Web!"+""
		pass
				
def getalta():
	
	page_counter=0
	try:
    		while page_counter < int(sys.argv[2]):
        		results_web = 'http://www.altavista.com/web/results?q='+str(query)+'&stq=10'+repr(page_counter)
        		request_web = urllib2.Request(results_web)
        		request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
        		opener_web = urllib2.build_opener()                           
        		text = opener_web.open(request_web).read()
        		names = re.findall(('\d\d\d\-\d\d\d\-\d\d\d\d'),StripTags(text))
			print "[+] Found:",len(names)
        		for name in names:
				if name not in d:
					d.append(name)
        		page_counter +=10
        
	except IOError:
    		print "[-] Can't connect to Altavista Web!"+""
		pass
	
		  
if len(sys.argv) != 4:
	print "\n   d3hydr8[at]gmail[dot]com SearchDigits v1.0"
	print "------------------------------------------------"
	print "\nUsage: ./searchdigits.py <query> <how many> <file to save results>"
	print "Ex: ./searchdigits.py \"contact\" 200 results.txt\n"
	sys.exit(1)
	
else:
	print "\n   d3hydr8[at]gmail[dot]com SearchDigits v1.0"
	print "------------------------------------------------"
	print "[+] Searching: Google.com"
	print "[+] Target:",sys.argv[1]
	print "[+] Total:",sys.argv[2]
	print "[+] File:",sys.argv[3]

langs = ["en", "it", "nl", "ru", "ua", "pl", "de", "be", "kr", "fr", "es", "se", "no", "ir", "za"]
print "[+] Languages:",len(langs),"\n"
		
if sys.argv[2].isdigit() == False:
	print "\n[-] Argument [",sys.argv[2],"] must be a number.\n"
	sys.exit(1)
if int(sys.argv[2]) <= 10:
	print "\n[-] Argument [",sys.argv[2],"] must be greater than 10.\n"
	sys.exit(1)

query = re.sub("\s","+",sys.argv[1])	
d=[]

while len(d) < int(sys.argv[2]):
	for lang in langs:
		print "[+] Language:",lang
		getgoog(lang)
		langs.remove(lang)
		d = list(sets.Set(d))
		print "[+] Found:",len(d)
	if len(langs) == 0:
		print "\n[+] Searching: MSN.com"
		getmsn()
		print "\n[+] Searching: Yahoo.com"
		getyahoo()
		print "\n[+] Searching: Altavista.com"
		getalta()
		break
		
file = open(sys.argv[3], "a")
print "\n[+] Found:",len(d)
print "[+] Writing Data:",sys.argv[3]
for number in d:	
	file.writelines(number+"\n")
file.close()
print "[-] Done\n"

