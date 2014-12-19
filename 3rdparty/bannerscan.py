#!/usr/bin/python
#A banner scanner that uses nmap to search for open ports
#then attempts to recieve banner, then checks the banner 
#against a list of vulnerbale servers. I supplied a list
#but feel free to use your own or add to it. Line 58 
#has the location of the vuln_list, so change this if its not 
#in the same dir as this file.

#Changelog: added webserver scan, added more vuln servers to list, better syntax
#Changelog: added update function

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import commands, sys, StringIO, re, string, socket, time, httplib, urllib2

def scan():

	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -T 3 --open --host-timeout 25s -iR 1')[1]).read()
	ip = re.findall("\d*\.\d*\.\d*\.\d*", nmap)
	if ip: 
		ipaddr = ip[0]
		print "[+] Searching:",ipaddr
	
	ports = re.findall("\d+/tcp\s+(?=open)", nmap)
	for port in ports:
		port = port.split("/",1)[0]
		print "[+] Port:",port,"open, checking banner.\n"
		if port != "80" and port != "443":
			banscan(ipaddr, port)
		else:
			servtest(ipaddr, port)
			
def servtest(ip, port):
	
	server = ""
	try:
		h = httplib.HTTP(ip+":"+port)
		h.putrequest("HEAD", "/")
		h.putheader("Host", ip)
		h.endheaders()
		status, reason, headers = h.getreply()
		server = headers.get("Server")
		print server
	except: pass
	
	if server != None and server != "":
		for item in lines:
			if re.search(item[:-1].lower(), server.lower()): 
				print "\n[!] Match:",ipaddr,":",port,item
				print "[+]Response:",response,"\n"
		
				
def banscan(ipaddr, port):

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(15)
		s.connect((ipaddr, int(port)))
		time.sleep(4)
		s.send("\r\n")
		response = s.recvfrom(1024)[0]
		s.close()
		for item in lines:
			  if re.search(item[:-1].lower(), response.lower()): 
					print "\n[!] Match:",ipaddr,":",port,item
					print "[+]Response:",response,"\n"
	except socket.error, msg:
   		print "[-] An error occurred:", msg
		pass
			
def update():
	try:
		lines = open(sys.argv[2], "r").readlines()
	except(IOError): 
 		print "[-] Error: Check your [",sys.argv[2],"] path and permissions"
		print "[-] Update Failed\n"
		sys.exit(1)
	try:
		paths = urllib2.urlopen("http://www.darkc0de.com/scanners/vuln_list.txt").readlines()
	except:
		print "[-] Error: Couldn't connect to remote database"
		print "[-] Update Failed\n"
		sys.exit(1)
	if len(paths) > len(lines):
		dif = int(len(paths)-len(lines))
		print "[+] Found:",dif,"updates"
		print "\n[+] Writing Updates"
		file = open(sys.argv[2], "a")
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
		
#................................................
print "\n   d3hydr8[at]gmail[dot]com BannerScan v1.2"
print "----------------------------------------------"

if len(sys.argv) >= 4 or len(sys.argv) == 1 or len(sys.argv) == 2:
	print "\nUsage: ./banscan.py <how many ips to scan> <path to vuln. server list>"
	print "\t[options]"
	print "\t   -u/-update <path to vuln. server list>: Updates vuln list with the latest"
	print "\n\t[+] Ex. ./banscan.py -update vuln_list.txt"
	print "\t[+] Ex: ./banscan.py 10000 /home/d3hydr8/vuln_list.txt\n"
	sys.exit(1)
	
if sys.argv[1].lower() == "-u" or sys.argv[1].lower() == "-update":
	print "\n[+] Updating Database File"
	update()

print "\n[+] Scanning:",sys.argv[1]

try:
	lines = open(sys.argv[2], "r").readlines()
	print "[+] Loaded:",len(lines),"vulnerable servers\n"
except(IOError): 
 	print "Error: Check your vuln_list path\n"
	sys.exit(1)
for x in xrange(int(sys.argv[1])):
	scan()
print "\n[-] Done\n"
	