#!/usr/bin/python

import commands, sys, getopt, StringIO, re, string, ftplib
from ftplib import *

tmp, args = getopt.getopt(sys.argv[1:],"")
	
def getopen():

	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 '+host)[1]).readlines()
	return nmap
	
def sock(plist):
	
	for port in plist:
		print "\nChecking port:",port
		try:
			import socket, time
		
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(15)
			s.connect((host, int(port)))
			time.sleep(4)
			s.send("\r\n")
			response = s.recvfrom(1024)[0]
			s.close()
			if response:
				print "++[ Response:",host,"on port",port,"\n"
				print "\t",response
		except socket.error, msg:
			s.close()
   			print "An error occurred:", msg
			
def http(p):
	
	import httplib
	try:# make a http HEAD request
		h = httplib.HTTP(host+":"+p)
		h.putrequest("HEAD", "/")
		h.putheader("Host", host)
		h.endheaders()
		status, reason, headers = h.getreply()
		print "\nChecking port:",p
		print "++[ Response:",host,"on port",p,"\n"
		print "\t",headers.get("Server"),"\n"
	except: 
		print "Error: Name or service not known. Check your host."
		pass

def ftp(p):
	
	try:
		print "Checking for anonymous login on",host
		ftp = FTP(host)
		ftp.login()
		ftp.retrlines('LIST')
		print "\t\nAnonymous login successful on",host,"\n"
		ftp.quit()
	except (ftplib.all_errors), msg: print "An error occurred:", msg
	
#................................................
	
if args == []:
	print "Usage: ./ipbanscan.py <host>"
else:
	host = args[0]
	plist = []
	www = ["80","8000","8080"]
	print "\n\t   d3hydr8[at]gmail[dot]com IP BannerScanner v1.0"
	print "\t--------------------------------------------------\n"
	print "\n\t\t.:[ Scanning",args[0],"]:.\n"
	nmap = getopen()
	for tmp in nmap:
		if re.search("\d+/tcp\s+(?=open)", tmp): 
			port = re.findall("\d+", tmp) 
			if port: plist.append(port[0])
	print "Ports open:",len(plist),"\n"
	for p in www:
		if p in plist: 
			http(p)
			plist.remove(p)
	if "21" in plist:
		ftp(21)
	if "23" in plist:
		print "\n\tTelnet server found on port 23. brute?" 
		sock(["23"])
		plist.remove("23")
	sock(plist)
				