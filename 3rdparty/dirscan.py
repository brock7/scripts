#!/usr/bin/python
#Takes a list of dir paths and tests http response.
#
##http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, httplib, socket

def main(path):
	
	if path[0] == "/":
		path = path[1:]
	h = httplib.HTTP(host[:-1])
	h.putrequest("HEAD", "/"+path)
	h.putheader("Host", host)
	h.endheaders()
	okresp, reason, headers = h.getreply()
	return okresp, reason, headers.get("Server")

socket.setdefaulttimeout(15)

print "\n\t   d3hydr8[at]gmail[dot]com DirScan v1.0"
print "\t-----------------------------------------"

if len(sys.argv) != 3:
	print "\n\tUsage: ./dirscan.py <host> <path_file>\n"
	print "\nEx. ./dirscan.py google.com paths.txt\n"
	sys.exit(1)

try:
	dirs = open(sys.argv[2], "r").readlines()
except(IOError): 
 	print "[-] Error: Check your file location.\n" 
	sys.exit(1)
	
host = sys.argv[1].replace("http://","")
if host.count("/") >= 1:
	host = host.rsplit("/",1)[0]
if host[-1:] != "/":
	host =  host+"/"

print "\n[+] Target host:",host
print "[+] Target server:",main("/")[2]
print "[+] Paths Loaded:",len(dirs),"\n"

for line in dirs:
	resp, reason = main(line.replace("\n",""))[:2]
	print "[+]",line[:-1]," | ",resp,reason
print "\n[-] Done\n"


	