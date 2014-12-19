#!usr/bin/python
#Sub-domain searcher will search hostnames for keywords.
#There are 2 ways to scan, ip-range or random ips.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, socket, re, random

#Change this to what your searching for
hits = ["admin","mail","secure","secret","login"]

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
			
def randip():
	
	A = random.randrange(255) + 1
	B = random.randrange(255) + 1
	C = random.randrange(255) + 1
	D = random.randrange(255) + 1
	ip = "%d.%d.%d.%d" % (A,B,C,D)
	return ip

if len(sys.argv) != 2:
	print "Usage: ./subsearch.py <option>"
	print "\t[options]" 
	print "\t   <number> : Random Scan" 
	print "\t   <ip_range> : Searches ip_range"
	print "ex: ./subsearch.py 1000" 
	print "ex: ./subsearch.py 198.162.1.1-100" 
	sys.exit(1)
	
num = 0
print "\n[+] Loaded:",len(hits),"searches"
if sys.argv[1].isdigit() == False:
	print "[+] Searching:",sys.argv[1]
	try:
		iplist = getips(sys.argv[1])
	except(IndexError):
		print "\n[-] Incorrect ip_range format\n"
		sys.exit(1)
	print "\n[+] Range Loaded:",len(iplist),"ips\n"
	for ip in iplist:
		try:
			for h in hits:
				hn = socket.gethostbyaddr(ip)[0]
				if re.search(h,hn):
					print "HostIP:",ip
					print "HostName:",hn
					num +=1
		except(socket.herror):
			pass
	print "\n[+] Found",num,"matches for ip range",sys.argv[1],"\n"
else:
	print "[+] Searching:",sys.argv[1],"ips\n"
	for x in xrange(int(sys.argv[1])):
		try:
			ip = randip()
			for h in hits:
				hn = socket.gethostbyaddr(ip)[0]
				if re.search(h,hn):
					print "HostIP:",ip
					print "HostName:",hn
					num +=1
		except(socket.herror):
			pass
	print "\n[+] Found",num,"matches found from",sys.argv[1],"ips\n"
	




