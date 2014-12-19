#!usr/bin/python
#Sub-domain collector from ip range.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, socket

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
			
if len(sys.argv) != 2:
	print "Usage: ./subcollect.py <ip_range>"
	sys.exit(1)
	
iplist = getips(sys.argv[1])
print "\n[+] Range Loaded:",len(iplist),"\n"
num = 0
for ip in iplist:
	try:
		hn = socket.gethostbyaddr(ip)[0]
		print "HostIP:",ip
		print "HostName:",hn
		num +=1
	except(socket.herror):
		pass
print "\n[+] Found",num,"possible subdomain(s) for ip range",sys.argv[1],"\n"




