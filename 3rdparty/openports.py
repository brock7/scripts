#!/usr/bin/python
#Takes a list of sites/ips and checks if a port is open.
#If the port is open, saves the site/ip to a file.

#Mozi Project ;)

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import socket, sys

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com PortListScan v1.0"
	print "\t------------------------------------------------"

def write(host):
	file = open(sys.argv[3], "a")
	file.writelines(host+" : "+port+"\n")
	file.close()

def scan(host):
	if host[-1] == "\n":
		host = host[:-1]
	print "[-] Target:",host
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(4)
		s.connect((socket.gethostbyname(host), int(port)))
		print "\n[+] OPEN:",host, port
		print "[+] Response:",s.recvfrom(1024)[0]
		write(host)
		s.close()
	except:
		pass

if len(sys.argv) != 4:
	title()
	print "Usage: ./openports.py <list of sites/ips> <port> <saved file>"
	sys.exit(1)
	
port = sys.argv[2]

try:
  sites = open(sys.argv[1], "r").readlines()
except(IOError): 
  print "\nError: Check your site list path\n"
  sys.exit(1)

title()
print "\n[+] Sites Loaded:",len(sites)
print "[+] Scanning...\n"
for site in sites:
	scan(site)

