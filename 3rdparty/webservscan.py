#!/usr/bin/python
#Uses nmap to search for open webserver ports
#in an ip range.
#Then trys to report what servers running.
#d3hydr8[at]gmail[dot]com

import commands, sys, getopt, StringIO, re, httplib

tmp, args = getopt.getopt(sys.argv[1:],"")
	
def scan():

	iprange = args[0]
	ip_list = []
	
	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 '+iprange+' -p 80,8000,8080 | grep -B 5 open')[1]).readlines()
	
	for tmp in nmap:
		ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ipaddr:
	    		ip_list.append(ipaddr[0])
	print "Found",len(ip_list),"hosts to investigate...\n"
	return ip_list

def servtest(ip_list):
	
	ports = [80,8000,8080]
	for ip in ip_list:
		for port in ports:
			try:
				h = httplib.HTTP(ip+":"+str(port))
				h.putrequest("HEAD", "/")
				h.putheader("Host", ip)
				h.endheaders()
				status, reason, headers = h.getreply()
				server = headers.get("Server")
				if server:
					print ip,":",port,"is running",server,"\n"
			except: pass
#................................................
	
if args == []:
	print "Usage: ./webservscan.py <ip range>"
else:
	print "\n   d3hydr8[at]gmail[dot]com WebServScan v1.0"
	print "--------------------------------------------------"
	print "+ Target range:",args[0]
	print "+ Target ports: 80,8000,8080"
	print "\n\t .:[ Scanning", args[0],"]:.\n"
	servtest(scan())
