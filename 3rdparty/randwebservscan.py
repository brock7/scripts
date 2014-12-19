#!/usr/bin/python
#Uses nmap to search for open webserver port
#in a random ip.
#Then trys to report what servers running if open.
#d3hydr8[at]gmail[dot]com

import commands, sys, getopt, StringIO, re, httplib

tmp, args = getopt.getopt(sys.argv[1:],"")
	
def scan():
	
	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 -iR 1 -p 80 | grep -B 5 open')[1]).readlines()
	
	for tmp in nmap:
		ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ipaddr:
			ip = ipaddr[0]
	    		return ip

def servtest(ip):
	
	try:
		h = httplib.HTTP(ip)
		h.putrequest("HEAD", "/")
		h.putheader("Host", ip)
		h.endheaders()
		status, reason, headers = h.getreply()
		server = headers.get("Server")
		if server:
			print ip,":",server,"\n"
	except: pass
#................................................
	
if args == []:
	print "Usage: ./randwebservscan.py <num ips to scan>"
else:
	print "\n   d3hydr8[at]gmail[dot]com Random WebServScan v1.0"
	print "   ------------------------------------------------"
	print "+ Scanning:",args[0],"servers\n"
	for i in xrange(int(args[0])):
		servtest(scan())
