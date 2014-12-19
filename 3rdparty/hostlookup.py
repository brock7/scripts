#!/usr/bin/env python
#Retrieves fully-qualified hostnames from ip_range.
#d3hydr8[at]gmail[dot]com

import sys, socket

def getips(ip_range):
	
	lst = []
	ip_range = ip_range.rsplit(".",2)
	if len(ip_range[1].split("-",1)) ==2:
		for i in range(int(ip_range[1].split("-",1)[0]),int(ip_range[1].split("-",1)[1])+1,1):
			lst.append(ip_range[0]+"."+str(i)+".")
		for ip in lst:
			for i in range(int(ip_range[2].split("-",1)[0]),int(ip_range[2].split("-",1)[1])+1,1):
				iplist.append(ip+str(i))
		return iplist
	if len(ip_range[1].split("-",1)) ==1:
		for i in range(int(ip_range[2].split("-",1)[0]),int(ip_range[2].split("-",1)[1])+1,1):
			iplist.append(ip_range[0]+"."+str(ip_range[1].split("-",1)[0])+"."+str(i))
		return iplist
			
def sock(ips):
	
	print "Length:",len(iplist)
	for i in ips:
		
		try:
			#Getting fully-qualified hostname.
			rec = socket.getfqdn(i)
			print "Hostname:",rec
			#Getting the right ip for the hostname.
			ips = socket.getaddrinfo(rec, None, 0, socket.SOCK_STREAM)
			print "\tIP addresses:",ips[0][4][0]
		except (socket.herror,socket.gaierror), msg:
			pass
	
if len(sys.argv) !=2:
	print "Usage: ./hostlookup.py 192.168.1-254.0-255"
	sys.exit(1)
else:
	iplist = []
	sock(getips(sys.argv[1]))
	