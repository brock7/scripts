#!/usr/bin/python 
#Gets http response from a list of sites (paths). 
 
#mozi project ;) 
 
#http://www.darkc0de.com 
#d3hydr8[at]gmail[dot]com 
 
import sys, httplib 
 
def main(host, path): 
	try:# make a http HEAD request 
		h = httplib.HTTP(host) 
		h.putrequest("HEAD", "/"+path.strip("\n")) 
		h.putheader("Host", host) 
		h.endheaders() 
		status, reason, headers = h.getreply() 
		print "[+]",host+"/"+path.strip("\n"),":",status, reason 
	except: 
		print "[-] Error Occurred" 
		pass 
 
if len(sys.argv) != 2: 
	print "Usage: ./getresp.py <list of sites>" 
	sys.exit(1) 
 
print "\n   d3hydr8[at]gmail[dot]com getResp v1.0" 
print "----------------------------------------------" 
 
try: 
  	list1 = open(sys.argv[1], "r").readlines() 
except(IOError): 
	print "[-] Error: Check your list file.\n" 
  	sys.exit(1) 
 
print "\n[+] Loaded:",len(list1),"sites" 
 
for host in list1: 
	try: 
		main(host.strip("http://").split("/",1)[0], host.strip("http://").split("/",1)[1]) 
	except(IndexError): 
		main(host, "/") 
print "\n[+] Done\n"