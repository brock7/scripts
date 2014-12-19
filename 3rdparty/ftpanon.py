#!/usr/bin/python
#Uses nmap to scan ip range 
#for port 21(ftp) open then 
#checks for anonymous login.
#d3hydr8[at]gmail[dot]com

import commands, sys, getopt, StringIO, re, ftplib
from ftplib import *

tmp, args = getopt.getopt(sys.argv[1:],"")
	
def scan():

	iprange = args[0]
	ip_list = []
	
	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 '+iprange+' -p 21 | grep open -B 3')[1]).readlines()
	
	for tmp in nmap:
		ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ipaddr:
	    		ip_list.append(ipaddr[0])
	print "Found",len(ip_list),"hosts with ftp port open.\n"
		   

	for ip in ip_list:
		try:
			print "Checking for anonymous login on",ip
			ftp = FTP(ip)
			ftp.login()
			ftp.retrlines('LIST')
			print "\n\tAnonymous login successful on",ip,"\n"
			ftp.quit()
		except (ftplib.all_errors), msg: print "An error occurred:", msg
		
#................................................
	
if args == []:
	print "Usage: ./ftpanon.py <ip range>"
else:
	print "\n\t [ Scanning", args[0],"]\n"
	scan()
