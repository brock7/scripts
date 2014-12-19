#!/usr/bin/python
#Searches google with a user defined query then writes the results to a file.

#Changelog: added the ability to choose how many.

#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com

import sys, re, string, httplib, urllib2

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
		  
if len(sys.argv) != 4:
	print "\n   d3hydr8[at]gmail[dot]com Goog2Text v1.1"
	print "--------------------------------------------------"
	print "\nUsage: ./goog2text.py <query> <how many> <file to save results>"
	print "Ex: ./goog2text.py \"inurl:/etc/shadow\" 200 results.txt\n"
	sys.exit(1)
	
else:
	print "\n   d3hydr8[at]gmail[dot]com Goog2Text v1.1"
	print "--------------------------------------------------"
	print "[+] Searching: Google.com"
	print "[+] Target:",sys.argv[1]
	print "[+] Total:",sys.argv[2]
	print "[+] File:",sys.argv[3]
	
if sys.argv[2].isdigit() == False:
	print "\n[-] Argument [",sys.argv[2],"] must be a number.\n"
	sys.exit(1)
if int(sys.argv[2]) <= 10:
	print "\n[-] Argument [",sys.argv[2],"] must be greater than 10.\n"
	sys.exit(1)

query=sys.argv[1]
d=[]
    
page_counter=0
try:
	#Change this 50 to search for more sites.(multiples of 10)
    while page_counter < int(sys.argv[2]):
        results_web = 'http://www.google.com/search?q='+str(query)+'&hl=en&lr=&ie=UTF-8&start='+repr(page_counter)+'&sa=N'
        request_web = urllib2.Request(results_web)
        request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
        opener_web = urllib2.build_opener()                           
        text = opener_web.open(request_web).read()
        names = re.findall(('\w+\.\w+.\w+\.\w+'),StripTags(text))
        for name in names:
            if name not in d:
			  d.append(name)
        page_counter +=10
        
except IOError:
    print "[-] Can't connect to Google Web!"+""
file = open(sys.argv[3], "a")
print "[+] Found:",len(d)
print "[+] Writing Data:",sys.argv[3]
for sites in d:	
	file.writelines(sites+"\n")
file.close()
print "[-] Done\n"

