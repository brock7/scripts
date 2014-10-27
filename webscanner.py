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
import pdb

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

class WebScanner:

	opener = None

	def __init__(self, dictfile = ""):
		self.dictfile = dictfile
	
	results = (
		"<b>Fatal error</b>:", 
		"Access Denied",
		"Fatal", 
		"Error", 
	);

	def defaultHandler(self, request, respText):
		if checkAll:
			return True
		for p in self.results:
			if re.search(p , respText):
				return True
		return False

	
	def sendReq(self, request, data, timeout = 15):
		index = random.randint(0, len(user_agents) - 1)
		user_agent = user_agents[index]
		request.add_header('User-agent', user_agent)
		try:
			response = self.opener.open(request, data = data, timeout = timeout)
		except Exception,e:
			#print e
			return None
		return response

	def scanUrl(self, url, data = None, hdrs = {}):
		#print url
		request = urllib2.Request(url)
		#if data != None:
		#	request.add_data(data)
		for name, val in hdrs:
			request.add_header(name, val)

		response = self.sendReq(request, data)
		if response:
			respText = response.read()
			#print respText
			if self.defaultHandler(request, respText):
				print url
				print respText[:1024]
				print '=' * 60

	def scanHost(self, hostRoot, uris):
		#pdb.set_trace()
		for uri in uris:
			if uri[0] != '/':
				uri = '/' + uri
			url = hostRoot + uri
			self.scanUrl(url)
			global wait
			if wait > 0:
				time.sleep(wait)
	
	def scan(self, hostRoot, uriFile, saveCookie = False):
		#pdb.set_trace()
		print '=' * 60
		if saveCookie:
			cookieJar = cookielib.CookieJar()
			self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		else:
			self.opener = urllib2.build_opener()
		file = open(uriFile)
		if (file == None):
			print file
			return False
		self.scanHost(hostRoot, file.readlines())
		return True

# webscanner.py [opt] host		 
# -w wait time. 
# -f config file. default ./config
opts, args = getopt.getopt(sys.argv[1:], "af:w:")

for op, value in opts:
	if op == '-a':
		checkAll = True
	elif op == "-f":
		config = value
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

