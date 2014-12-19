#!/usr/bin/python
#This is a phpBB scanner, searches if vulnerable paths
#exist. Put phpvuln.txt in the dir
#at which you are running this script.
#Every path in phpvuln.txt has a vuln. or an exploit for it.
#(considering its the right version)

#Changelog v1.2 : added update function

#Changelog v1.1 : added verbose mode, changed http 
#response bug, added new vuln. paths

#http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, httplib, time, urllib2

def getserv(path):

	try:
		h = httplib.HTTP(host+":"+port)
		h.putrequest("HEAD", path)
		h.putheader("Host", host)
		h.endheaders()
		status, reason, headers = h.getreply()
	except: 
		print "\n[-] Error: Name or service not known. Check your host.\n"
		sys.exit(1)
	return status, reason, headers.get("Server")

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com PhpBBscanner v1.2"
	print "\t--------------------------------------------------"

def update():
	try:
		lines = open("phpvuln.txt", "r").readlines()
	except(IOError): 
 		print "[-] Error: Check your phpvuln.txt path and permissions"
		print "[-] Update Failed\n"
		sys.exit(1)
	try:
		paths = urllib2.urlopen("http://www.darkc0de.com/scanners/phpvuln.txt").readlines()
	except:
		print "[-] Error: Couldn't connect to remote database"
		print "[-] Update Failed\n"
		sys.exit(1)
	if len(paths) > len(lines):
		dif = int(len(paths)-len(lines))
		print "[+] Found:",dif,"updates"
		print "\n[+] Writing Updates"
		file = open("phpvuln.txt", "a")
		for path in paths[-dif:]:
			if path[-1:] == "\n":
				path = path[:-1]
			print "[+] New:",path
			file.writelines(path+"\n")
		file.close()
		print "\n[+] Update Complete\n"
	else:
		print "[-] No Updates Available\n"
	sys.exit(1)

if len(sys.argv) >= 5 or len(sys.argv) == 1:
	title()
	print "\n\t[+] Usage: ./phpbbscan.py <host> <port>\n"
	print "\t[options]"
	print "\t   -v/-verbose : Shows all http requests and responses"
	print "\t   -u/-update : Updates phpvuln.txt with the latest"
	print "\n\t[+] Ex. ./phpbbscan.py -update"
	print "\t[+] Ex. ./phpbbscan.py google.com 80 -verbose\n"
	sys.exit(1)

title()

if sys.argv[1].lower() == "-u" or sys.argv[1].lower() == "-update":
	print "\n[+] Updating Database File"
	update()
	
host = sys.argv[1]
port = sys.argv[2]

for arg in sys.argv[1:]:
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
	else:
		verbose = 0

if host[:7] == "http://":
	host = host.replace("http://","")
if host[-1] == "/":
	host = host[:-1]
	
print "[+] Getting responses" 
okresp,reason,server = getserv("/")
badresp = getserv("/d3hydr8.html")[:1]

if okresp == badresp[0]:
	print "\n[-] Responses matched, try another host.\n"
	sys.exit(1)
else:
	print "\n[+] Target host:",host
	print "[+] Target port:",port
	print "[+] Target server:",server
	print "[+] Target OK response:",okresp
	print "[+] Target BAD response:",badresp[0], reason
	print "[+] Scan Started at",timer()
	if verbose ==1:
		print "\n[+] Verbose Mode On"

dirs = ["/","/bb/","/phpbb/","/forum/","/forums/","/phpBB2/","/phpbb/phpBB2/"]

try:
	lines = open("phpvuln.txt", "r").readlines()
	print "\n[+]",len(lines)*len(dirs),"paths loaded\n"
except(IOError): 
 	print "[-] Error: Check your vulnerabilities list path\n"
	sys.exit(1)

vulns = []
print "[+] Scanning...\n" 
for d in dirs:
	for line in lines:
		status, reason = getserv(d+line[:-1])[:2]
		if verbose ==1:
			print "[+]",status,reason,":",d+line,"\n"
		if status == okresp:
			vulns.append(d+line)
			print "\t[!]",status,reason,":",d+line,"\n"
		if status == int(401):
			print "\t--",status,reason,":Needs Authentication [",d+line,"]\n"
		
if len(vulns) == 0:
	print "[-] Couldn't find any vuln. paths\n"
else:
	print "[!] Found",len(vulns),"possible vulnerabilities, check manually.\n"
	for vuln in vulns:
		print "\t[+] ",vuln
print "\n[+] Scan completed at", timer(),"\n"