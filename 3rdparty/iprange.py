#!/usr/bin/env python
#A python function that takes 
#an ip_range ex: (192.168.1-254.0-255) or 
#192.168.1.0-255) and appends every ip
#to a returned list for other uses.
#Use it if you would like or email me with
#a better one.
#d3hydr8[at]gmail[dot]com

import sys

def getips(ip_range):
	
	lst = []
	iplist = []
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
			
iplist = getips(sys.argv[1])
print "Length:",len(iplist)

			
		
	