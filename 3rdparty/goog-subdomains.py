#!/usr/bin/python
#Another goog-mail.py mod, extracts subdomains from google.
#d3hydr8[at]gmail[dot]com

import sys
import re
import string
import httplib
import urllib2
import re
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
if len(sys.argv) != 2:
        print "\nExtracts subdomains from google results.\n"
        print "\nUsage : ./goog-subdomains.py <domain-name>\n"
        sys.exit(1)

domain_name=sys.argv[1]
print "\nSearching for",domain_name,"\b's subdomains...\n"
d=[]
page_counter = 0
try:
    while page_counter < 50 :
        results = 'http://groups.google.com/groups?q='+str(domain_name)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
        request = urllib2.Request(results)
        request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
        opener = urllib2.build_opener()                           
        text = opener.open(request).read()
        names = (re.findall('(\w+\.'+domain_name+')',StripTags(text)))
        for name in names:
		   if name not in d:
            		d.append(name)
        page_counter +=10
except IOError:
    print "Can't connect to Google Groups!"+""
    
page_counter_web=0
try:

    while page_counter_web < 50 :
        results_web = 'http://www.google.com/search?q='+str(domain_name)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter_web) + '&sa=N'
        request_web = urllib2.Request(results_web)
        request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
        opener_web = urllib2.build_opener()                           
        text = opener_web.open(request_web).read()
        names = (re.findall('(\w+\.'+domain_name+')',StripTags(text)))
        for name in names:
            if name not in d:
			  d.append(name)
        page_counter_web +=10
        
except IOError:
    print "Can't connect to Google Web!"+""
for subdomains in d:
	print subdomains

