#!/usr/bin/env python
import sys, os
import urllib2
import cookielib
import re
import random
from lxml import etree
import time
import getopt
import errno
#import pdb

config = './config'
wait = 0.0
checkAll = False

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
 	(KHTML, like Gecko) Element Browser 5.0', \
	'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
	'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
	'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
	Version/6.0 Mobile/10A5355d Safari/8536.25', \
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
	Chrome/28.0.1468.0 Safari/537.36', \
	'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0', 
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
	
results = [
	"<b>Fatal error</b>:", 
	"Access Denied",
	"Microsoft OLE DB Provider", 
	"You have an error in your SQL syntax", 
	r'ERROR [0-9]+?:', 
];

class ScanHandler: 

	# return a generator or iterator
	def requests(self):
		return ()
	
	# return (result, response_text)
	def filterResponse(self, request, response):
		return True, ""

class FileScanHandler(ScanHandler):
	def __init__(self, host, fileName):
		self._host = host
		self._lines = open(fileName).readlines();
		
	def requests(self):
		for uri in self._lines:
			if uri[0] != '/':
				uri = '/' + uri
			yield urllib2.Request(self._host + uri)

	def filterResponse(self, request, response):
		respText = response.read()
		if checkAll:
			return True, respText
		for p in results:
			if re.search(p , respText):
				return True, respText
		return False, respText

class WebScanner:

	opener = None

	def __init__(self):
		pass
	
	def sendReq(self, request, data = None, timeout = 15):
		index = random.randint(0, len(user_agents) - 1)
		user_agent = user_agents[index]
		request.add_header('User-agent', user_agent)
		try:
			response = self.opener.open(request, data = data, timeout = timeout)
		except Exception,e:
			#print e
			return None
		return response
	
	def scan(self, hostRoot, uriFile, saveCookie = False):
		#pdb.set_trace()
		print '=' * 60
		if saveCookie:
			cookieJar = cookielib.CookieJar()
			self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		else:
			self.opener = urllib2.build_opener()
		scanHandler = FileScanHandler(hostRoot, uriFile)
		for req in scanHandler.requests():
			response = self.sendReq(req)
			if response:
				result, respText = scanHandler.filterResponse(req, response)
				if result:
					print req.get_full_url()
					print respText[:1024]
				print '=' * 60				

		return True

def usage():
	helpMsg = sys.argv[0] + """ [opt] host			
	
	-a show all exist page
	-e add custom error message
	-f config file. default ./config
	-h show help message
	-w wait time."""	
	print helpMsg 
	sys.exit(0)
	
opts, args = getopt.getopt(sys.argv[1:], "ae:f:hw:")
#print opts
#print args
for op, value in opts:
	if op == '-a':
		checkAll = True
	elif op == "-e":
		results.append(value)	
	elif op == "-f":
		config = value
	elif op == "-h":
		usage()
	elif op == "-w":
		wait = float(value)

host = args[0]
if config[-1] != '/':
	config += '/'

if not re.search(r'^http://', host):
	host = 'http://' + host

scanner = WebScanner()

ls = os.listdir(config)
for path in ls:
	if re.search('\.txt$', path):
		print host, config + path
		scanner.scan(host, config + path)
