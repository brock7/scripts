#!usr/bin/python 
#Smtp Open Relay Finder 
#http://www.darkc0de.com 
#d3hydr8[at]gmail[dot]com 
 
import threading, time, random, sys, smtplib, socket 
from smtplib import SMTP 
 
#Setup from address 
fromaddr = "abc@abc.com" 
#Setup receiving address 
toaddr = "abc@abc.com" 
#Setup message to be sent. 
message = """To: %s 
From: %s 
Subject: Test Message 
 
Put messsage here!!! 
 
""" % (toaddr,fromaddr) 
 
#Choose maximum amount of threads. 
MAX_THREADS = 3 
#Set socket timeout default 
socket.setdefaulttimeout(10) 
 
def randip(): 
	A = random.randrange(255) + 1 
	B = random.randrange(255) + 1 
	C = random.randrange(255) + 1 
	D = random.randrange(255) + 1 
	return "%d.%d.%d.%d" % (A,B,C,D) 
 
def getips(ip_range): 
 
	lst = [] 
	iplist = [] 
	ip_range = ip_range.rsplit(".",2) 
	if len(ip_range[1].split("-",1)) ==2: 
		for i in range(int(ip_range[1].split("-",1)[0]),int(ip_range[1].split("-",1)[1])+1,1): 
			lst.append(ip_range[0]+"."+str(i)+".") 
		for ip in lst: 
			for i in range(int(ip_range[2].split("-",1)[0]),int(ip_range[2].split("-",1)[1])+1,1): 
				iplist.append(ip+str(i)) 
		return iplist 
	if len(ip_range[1].split("-",1)) ==1: 
		for i in range(int(ip_range[2].split("-",1)[0]),int(ip_range[2].split("-",1)[1])+1,1): 
			iplist.append(ip_range[0]+"."+str(ip_range[1].split("-",1)[0])+"."+str(i)) 
		return iplist 
 
def check(lock ,ip): 
	try: 
		if random != 0: 
			lock.acquire() 
		s = smtplib.SMTP(ip) 
		code = s.ehlo()[0] 
		if not (200 <= code <= 299): 
			code = s.helo()[0] 
			if not (200 <= code <= 299): 
				raise SMTPHeloError(code, resp) 
		s.sendmail(fromaddr, toaddr, message) 
		print "\n[!] Message Sent Successfully" 
		print "[+] SMTP Server:",ip,"\n" 
		smtp.quit() 
	except(socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), msg: 
		#print "An error occurred:", msg 
		pass 
	if random != 0: 
		lock.release() 
 
print "\n\tsmtpReleyFinder v1.0" 
print "\t--------------------\n" 
if len(sys.argv) not in [3,4]: 
	print "\n\tUsage: ./relayfind.py <options>\n" 
	print "\t[options]" 
	print "\t   -i/-iprange <ip_range> : IP Range to scan (nmap format)." 
	print "\t   -r/-random <how many> : How many ips to scan" 
	print "\t   -v/-verbose : Verbose Mode" 
	print "\nEx. ./relayfind.py -iprange 192.168.1.1-255 -v\n" 
	sys.exit(1) 
 
for arg in sys.argv[1:]: 
	if arg.lower() == "-i" or arg.lower() == "-iprange": 
		iprange = sys.argv[int(sys.argv[1:].index(arg))+2] 
	if arg.lower() == "-r" or arg.lower() == "-random": 
		num = sys.argv[int(sys.argv[1:].index(arg))+2] 
	if arg.lower() == "-v" or arg.lower() == "-verbose": 
		verbose = 1 
 
try: 
	if iprange: 
		iplist = getips(iprange) 
		print "[+] Range Loaded:",len(iplist) 
except(NameError): 
	iprange = 0 
	pass 
except(IndexError): 
	print "[-] Misconfigured IpRange\n" 
	sys.exit(1) 
 
try: 
	if num: 
		print "[+] Random Scan:",num 
		num = int(num) 
except(NameError): 
	num = 0 
	pass 
 
print "From Address:",fromaddr 
print "Reveiving Address:",toaddr 
print "Message:",message 
 
try: 
	if verbose == 1: 
		print "[+] Verbose Mode On\n" 
except(NameError): 
	print "[-] Verbose Mode Off\n" 
	verbose = 0 
	pass 
 
if iprange != 0: 
	for ip in iplist: 
		if verbose == 1: 
			print "Testing:",ip 
		lock = threading.Lock() 
		check(lock, ip) 
	sys.exit(1) 
 
if random != 0: 
	while num >= 0: 
		print num 
		for x in xrange(MAX_THREADS): 
			ip = randip() 
			if verbose == 1: 
				print "Testing:",ip 
			lock = threading.Lock() 
			work = threading.Thread(target = check, args=(lock,ip)).start() 
			time.sleep(1) 
			num -=1 
	time.sleep(5) 
	sys.exit(1) 

