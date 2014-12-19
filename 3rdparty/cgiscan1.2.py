#!/usr/bin/python
#This is a CGI scanner, searches for common vulnerable 
#dirs and files. 
#Save the bins.txt to the dir your 
#running this. http://www.darkc0de.com/scanners/bins.txt
#Or use your own list and save it bins.txt.
#
#Changelog v1.2: Added proxy support, verbose mode, and fixed 
# minor syntax problems
#
#
#Changelog v1.1: Update: Faster, 2500 more vuln dir/files,
# saves found vulns to a list and prints them at the end.
# Also fixed some error handling so it shouldn't stop at any time and 
# I had an extra \n newline where it shouldn't be.
#

#
##http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, httplib, time, socket

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com CGIscanner v1.2"
	print "\t--------------------------------------------------"

def main(path):
	
	if path[0] == "/":
		path = path[1:]
	if proxy != 0:
		h = httplib.HTTP(proxy)
		h.putrequest("GET", "http://"+host+path)
	else:
		h = httplib.HTTP(host[:-1])
		h.putrequest("HEAD", "/"+path)
	h.putheader("Host", host)
	h.endheaders()
	okresp, reason, headers = h.getreply()
	return okresp, reason, headers.get("Server")
		
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)
	
title()
socket.setdefaulttimeout(15)

if len(sys.argv) not in [3,4,5,6]:
	print "\n\tUsage: ./cgiscan.py <host> <port> <options>\n"
	print "\t[options]"
	print "\t   -p/-proxy <host:port> : Add proxy support"
	print "\t   -v/-verbose : Verbose Mode"
	print "\nEx. ./cgiscan.py google.com 80 -proxy 120.71.68.2:8888 -v\n"
	sys.exit(1)
	
host = sys.argv[1]
port = sys.argv[2]

for arg in sys.argv[1:]:
	if arg.lower() == "-p" or arg.lower() == "-proxy":
		proxy = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1

try:
	if proxy:
		print "\n[+] Testing Proxy..."
		h2 = httplib.HTTPConnection(proxy)
		h2.connect()
		print "[+] Proxy:",proxy
except(socket.timeout):
	print "\n[-] Proxy Timed Out"
	proxy = 0
	pass
except(NameError):
	print "\n[-] Proxy Not Given"
	proxy = 0
	pass
except:
	print "\n[-] Proxy Failed"
	proxy = 0
	pass

try:
	if verbose == 1:
		print "[+] Verbose Mode On\n"
except(NameError):
	print "[-] Verbose Mode Off\n"
	verbose = 0
	pass
	
host = host.replace("http://","")
if host.count("/") >= 1:
	host = host.rsplit("/",1)[0]
if host[-1:] != "/":
	host =  host+"/"

okresp = main(" ")[:1]

badresp,reason,server = main("/d3hydr8.html")

if okresp[0] == badresp:
	print "\nResponses matched, try another host.\n"
	sys.exit(1)
else:
	print "\n[+] Target host:",host
	print "[+] Target port:",port
	print "[+] Target server:",server
	print "[+] Target OK response:",okresp[0]
	print "[+] Target BAD response:",badresp, reason
	print "[+] Scan Started at",timer()
	time.sleep(3)

try:
	text = open("bins.txt", "r") #vulerable list, change path/name if necessary
	lines = text.readlines()
	text.close()
	print "\n[--",len(lines),"paths loaded --]\n"
except(IOError): 
 	print "[-] Error: Check your bins.txt path.\n" 
	print "[-] (http://www.darkc0de.com/scanners/bins.txt)\n"
	sys.exit(1)

found_vuln = []
for line in lines:
	if verbose == 1:
		print "\n[-] Left:",len(lines)
	try: 
		time.sleep(1)
		response, reason = main(line.strip("\n"))[:2]
		if verbose == 1:
			print "\n[+] Trying:",line,"   Got:",response, reason
		if response == okresp[0]:
			found_vuln.append(host+line)
			print "\n\t[+]",response,reason,":",host+line
		if response == int(401):
			print "\n\t[-]",response,reason,":",host+line,"\tNeeds Authorization"
	except(AttributeError, TypeError): 
		pass
	lines.remove(line)

if len(found_vuln) == 0:
	print "\n[-] Couldn't find anything.\n"
else:
	print "\n\t[+] Found",len(found_vuln),"possible vulnerabilities, check manually."
	for x in found_vuln:
		print "\n[!] ",x
print "\n[-] Scan completed at", timer()


	