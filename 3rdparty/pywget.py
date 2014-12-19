#!/usr/bin/python
#PyWget is wget writting in python with http proxy support.

#Supports: http, https, ftp

##http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, httplib, urllib2, shutil, os, socket, time

def timer():
	return time.strftime("%H:%M:%S", time.localtime())

if len(sys.argv) not in [2,4,6]:
	print "\n\tUsage: ./pywget.py <url> <options>\n"
	print "\t[options]"
	print "\t   -d/-dir <directory> : save files to PREFIX/..."
	print "\t   -p/-proxy <host:port> : Add proxy support"
	print "\nEx. ./pywget.py www.darkc0de.com/index.html -proxy 120.71.68.2:8888 -dir /home/d3hydr8/\n"
	sys.exit(1)

for arg in sys.argv[1:]:
	if arg.lower() == "-d" or arg.lower() == "-dir":
		Dir = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-p" or arg.lower() == "-proxy":
		proxy = sys.argv[int(sys.argv[1:].index(arg))+2]
			
url = sys.argv[1]
proto = url.split(":",1)[0]
try:
	port = socket.getservbyname(url.split(":",1)[0])
except(socket.error):
	port = 80
	proto = "http"
url = url.replace("http://","").replace("https://","").replace("ftp://","")
print "\n--"+timer()+"--",  url
try:
	print "\t=> `",url.rsplit("/",1)[1],"'"
except(IndexError):
	print "[!] Malformed URL\n"
	sys.exit(1)
hostname = url.split("/",1)[0]
try:
	ipaddr = socket.gethostbyname(hostname)
except(socket.gaierror),msg:
	print "\n"+timer(),"ERROR",msg,"\n"
	sys.exit()
print "Resolving",hostname+"...",ipaddr
try:
	if Dir:
		print "Saving to",Dir
except(NameError):
	Dir = os.getcwd()
if Dir[-1] != "/":
	Dir = Dir+"/"
try:
	if proxy:
		print "Testing Proxy..."
		h2 = httplib.HTTPConnection(proxy)
		h2.connect()
		print "Proxy:",proxy
except(socket.timeout):
	print "\n[-] Proxy Timed Out\n"
	sys.exit(1)
except(NameError):
	proxy = 0
	pass
except:
	print "\n[-] Proxy Failed\n"
	sys.exit(1)
print "Connecting to",hostname,"|",ipaddr,"|:"+str(port)+"... connected."
if proxy != 0:
	proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'})
	opener = urllib2.build_opener(proto+"://"+url, proxy_handler)
	try:
		source = opener.open(proto+"://"+url)
	except(urllib2.HTTPError),msg:
		print "\n"+timer(),"ERROR",msg,"\n"
		sys.exit()
else:
	try:
		source = urllib2.urlopen(proto+"://"+url)
	except(urllib2.HTTPError),msg:
		print "\n"+timer(),"ERROR",msg,"\n"
		sys.exit()
pre_size = str(len(str(source)))
print proto.upper(),"request sent, awaiting response..."
print "Length:",pre_size #FD size (not bytes)
num = 1
file = url.rsplit("/",1)[1]
while os.path.isfile(Dir+file) == True:
	file = url.rsplit("/",1)[1]+"."+str(num)
	num+=1
try:
	shutil.copyfileobj(source, open(Dir+file, "w+"))
except(IOError):
	print Dir+file+": Permission denied"
	print "\nCannot write to `"+Dir+file+"' (Permission denied)."
	sys.exit(1)
size = str(os.path.getsize(Dir+file))
print "\n"+timer(),"- `",file,"' saved","["+pre_size+"/"+size+"]\n"