#!/usr/bin/python
#This is a CGI scanner, searches for common vulnerable 
#dirs and files. 
#
#Update: Faster, 2500 more vuln dir/files,
#saves found vulns to a list and prints them at the end.
#Also fixed some error handling so it shouldn't stop at any time and 
#I had an extra \n newline where it shouldn't be.
#
#Save the bins.txt and save it to the dir your 
#running this.
#
##http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, httplib, time, socket

def main(path):
	try:# make a http HEAD request
		h = httplib.HTTP(host+":"+port)
		h.putrequest("HEAD", path)
		h.putheader("Host", host)
		h.endheaders()
		status, reason, headers = h.getreply()
		return status, reason, headers.get("Server")
	except: 
		print "Error Occurred"
		pass
	
		
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)
	

if len(sys.argv) != 3:
	print "\n\t   d3hydr8[at]gmail[dot]com CGIscanner v1.1"
	print "\t--------------------------------------------------"
	print "\n\tUsage: ./cgiscan.py <host> <port>\n"
	print "\tEx. ./cgiscan.py google.com 80\n"
	sys.exit(1)
	
host = sys.argv[1]
port = sys.argv[2]
socket.setdefaulttimeout(2)

if host[:7] == "http://":
	host = host.replace("http://","")

okresp = main("/")[:1]
badresp,reason,server = main("/d3hydr8.html")

if okresp[0] == badresp:
	print "\nResponses matched, try another host.\n"
	sys.exit(1)
else:
	print "\n   d3hydr8[at]gmail[dot]com CGIscanner v1.1"
	print "--------------------------------------------------"
	print "[+] Target host:",host
	print "[+] Target port:",port
	print "[+] Target server:",server
	print "[+] Target OK response:",okresp[0]
	print "[+] Target BAD response:",badresp, reason
	print "[+] Scan Started at",timer()
	time.sleep(3)

try:
	text = open("bins.txt", "r") #vulerable list, change path/name if necessary
	lines = text.readlines()
	text.close()
	print "\n[--",len(lines),"paths loaded --]\n"
except(IOError): 
 	print "Error: Check your bins.txt path.\n" 
	print "(http://www.darkc0de.com/scanners/bins.txt)\n"
	sys.exit(1)

found_vuln = []
for line in lines:
	print "\nLeft:",len(lines)
	try: 
		time.sleep(1)
		response, reason = main(line[:-1])[:2]
		print "\nTrying:",line,"   Got:",response, reason
		if response == okresp[0]:
			found_vuln.append(host+line)
			print "\n\t[+][+]",response,reason,":",host+line,"\n"
		if response == int(401):
			print "\n\t[-][-]",response,reason,":",host+line,"\tNeeds Authorization\n"
	except(AttributeError, TypeError): 
		pass
	lines.remove(line)

if len(found_vuln) == 0:
	print "\n[-] Couldn't find anything.\n"
else:
	print "\n\t[+] Found",len(found_vuln),"possible vulnerabilities, check manually."
	for x in found_vuln:
		print "\n[!] ",x
print "\n[-] Scan completed at", timer()


	