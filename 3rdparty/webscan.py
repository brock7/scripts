#!/usr/bin/python
#Prints webservers running in an iprange.
#http://darkcode.ath.cx
#d3hydr8[at]gmail[dot]com

import socket, httplib, threading, time, sys

def scan(ip, msg):
	ports = [80,8000,8080]
	for port in ports:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip, port))
			s.close()
			print "[+] Open:",ip+":"+str(port)
			servtest(ip, port)
		except:
			pass
	
	
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
	except: pass

print "\n\t   d3hydr8[at]gmail[dot]com WebServScan v1.1"
print "\t----------------------------------------------\n"
if len(sys.argv) < 2:
	print "Usage: ./webscan.py <ip_range>\n"
	sys.exit(1)
try:
	iplist = getips(sys.argv[1])
except(ValueError):
	print "[-] Incorrect IP-Range\n"
	sys.exit(1)
print "\n[+] Scanning:",len(iplist),"ips\n"
socket.setdefaulttimeout(3)
for ip in iplist:
	time.sleep(1)
	threading.Thread( target=scan, args=(ip, 0) ).start()
print "\n[-] Done\n"

	