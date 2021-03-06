﻿#!/usr/bin/python

# -*- encoding: utf-8 -*-

#
# filename: probe.py
# written by brock
# email: xiaowave@gmail.com
# date: 2014-06-06
#
###############################################################################	

import urllib, urllib2
import re
import sys, getopt
import os
from lxml import etree
import socket
import time
import signal
import cookielib
#from httpshandler import HTTPSHandler
import random
###############################################################################	

outfile = 'output'
os.environ['PATH'] += ';nikto-2.1.5;sqlmap' # FIXME
socket.setdefaulttimeout(20)

addresses = set()
hosts = set()
invIPs = set(["180.168.41.175"])

disableNikto = False
disableSqlmap = False
disableNmap = False
disableGoogleHack = False
level = 2
fixLevel = False
waitTime = 0
dbType = ''
probeType = ''

###############################################################################	

def usage():
	print "probe [-hnms] <host/domain>"
	pass

def createlog(fname):
	global outfile
	outfile = fname
	os.system('echo GENERATED BY PROBE.PY > %s' % (outfile))
	
def log(text):
	os.system('echo [%s] "%s" | tee -a %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), text, outfile));
	
def execute(cmdline):
	os.system("%s | tee -a %s" % (cmdline, outfile))
	
###############################################################################	

def doNmap(host):
	execute("nmap -O -sV %s" % (host))

def doNikto(host):
	if waitTime > 0:
		execute("nikto.pl -Pause %d -h %s" % (waitTime, host))
	else:
		execute("nikto.pl -h %s" % (host))
	
def doSqlmap(host):
	opts = ''
	if dbType != '':
		opts = '--dbms ' + dbType
	
	if waitTime > 0:
		execute('sqlmap.py --random-agent --threads=2 %s --delay %d --batch -g "site:%s"' % (opts, waitTime, host))		
	else:
		execute('sqlmap.py --random-agent --threads=2 %s --batch -g "site:%s"' % (opts, host))

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
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
	
def google(host, what):
	log('* google site:%s %s' % (host, what))
	what = urllib2.quote("site:%s %s" % (host, what))
	#print what
	url = 'https://www.google.com.hk/search?hl=en&q=%s' % what
	request = urllib2.Request(url)
	index = random.randint(0, 9)
	user_agent = user_agents[index]
	request.add_header('User-agent', user_agent)
	#print 'before'
	response = urllib2.urlopen(request, data = None, timeout = 17)
	#print 'after'
	html = response.read()
	#results = self.extractSearchResults(html)
	tree = etree.HTML(html)
	nodes = tree.xpath(r"//a/@href")
	for node in nodes:		
		if node.find(host) == -1 or node.find('google') != -1 or node.find('http') == -1 or node.find('youtube') != -1:
			continue
		log('\tLink: '+ node)
	#print html
	return
	
	#results = self.extractSearchResults(html)
#	cj = cookielib.CookieJar()
#	
#	try:
#		#response = urllib2.urlopen('http://www.google.com/search?q=python', timeout=10)
#		#req = urllib2.Request('http://www.google.com.hk/search?q=ext:xls+site:www.vancl.com')
#			
#		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), HTTPSHandler()) 
#		opener.addheaders.append(("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0"))
#		req = urllib2.Request('http://www.google.com/ncr')
#		print 1
#		response = opener.open(req) 
#		print response.read()
#		req = urllib2.Request('http://www.google.com/search?q=python')
#		print 2
#		response = opener.open(req)
#		#response = urllib2.urlopen('http://www.google.com.hk/search?q=ext:xls+site:www.vancl.com')  
#	except urllib2.HTTPError, e:
#		log("google error: " + e.msg + ' - ' + host)
#		return
#	html = response.read()  
#	print html
	
	#tree = etree.HTML(html)
	#nodes = tree.xpath(r"//a/@href")
	#for node in nodes:
#		print node

hacks = ('ext:xls', 'ext:xlsx', 'ext:doc', 'ext:docx', 'ext:txt', 'ext:zip', 
	'ext:conf', 'ext:rar', 'ext:sh', 'ext:gz', 'ext:bz2', 'ext:tar', 'ext:tgz', 
	'ext:mdb', 'ext:ini', "#", 
	'inurl:filename', 'inurl:upload', 'inurl:profile 管理员', 
	'inurl:file', 'inurl:down', "#", 
	'intitle:"index.of"', 'intitle:管理 ', "#",
	'intext:*@*.com', 'intext:*@*.net', 'intext:*@*.cn', 'intext:ftp://*:* ',  
	'intext:powered by', 
	)

def googleHack(host):
	
	log('******* google hack: ' + host)
	count = 1
	for hack in hacks:
		if hack == '#':
			#time.sleep(5)
			continue
		google(host, hack)
		time.sleep(3 if random.random() > 0.5 else 2)
		if count % 5 == 0:
			time.sleep(5)
		count = count + 1

###############################################################################	

def scanHost(host):
	try:
		result = socket.getaddrinfo(host, None) # FIXME: handle exception
	except:
		log('cannot resolve the ip: ' + host)
		return
		
	ip = result[0][4][0]
	log('******* host: %s(ip: %s) *******' % (host, ip));	

	if ip in invIPs:
		log('invalid host: ' + host + '. skiped')
		return
	if probeType != 'domain' and not disableGoogleHack:
		googleHack(host)
	
	if ip in addresses:
		log('duplication. host: ' + host + '. skip nmap')
	else:
		addresses.add(ip)
		if not disableNmap:
			doNmap(host)
			
	if not disableNikto:
		doNikto(host)
	if not disableSqlmap:
		doSqlmap(host)

def scanDomain(domain):
	global level
	if not fixLevel:
		level = domain.count('.') + 1
	if not disableGoogleHack:
		googleHack(domain)
	req = urllib2.Request('http://i.links.cn/subdomain/')
	data = 'domain=%s&b2=1&b3=1&b4=1' % domain
	#enable cookie  
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
	response = opener.open(req, data)      
	#response = urllib2.urlopen('http://www.baidu.com/')  
	html = response.read()
	#print html
	tree = etree.HTML(html)
	nodes = tree.xpath(r"//a/@href")
	for node in nodes:
		if node.find(domain) == -1:
			continue
		#host, rest = urllib.splithost(node)  
		pos = node.find('//')
		if pos >= 0:
			node = node[pos + 2:]
		
		if node.count('.') > level:
			print node + ' skiped'
			continue

		if node in hosts:
			continue
		hosts.add(node)
		try:
			scanHost(node)
		except:
			log('occurred a exception with ' + node)
		
def scanHostsfile(filename):
	for line in open(filename, "r").readlines():
		line = line.strip()
		#print line
		#if line.count('.') > level:
		#	print line + ' skiped'
		#	continue
		try:
			scanHost(line)
		except:
			log('occurred a exception with ' + node)
		
###############################################################################	

opts, args = getopt.getopt(sys.argv[1:], "h:f:nmsgl:w:t:")
method = ''
host = ""
filename = ""

for op, value in opts:
	if op == "-h":
		host = value
	elif op == "-f":
		filename = value
	elif op == '-m':
		disableNmap = True
	elif op == '-n':
		disableNikto = True
	elif op == '-s':
		disableSqlmap = True
	elif op == '-g':
		disableGoogleHack = True
	elif op == '-l':
		level = int(value)
		fixLevel = True
	elif op == '-w':
		waitTime = int(value)
	elif op == '-t':
		dbType = value
	else:
		usage()
		sys.exit()
	
if host =='' and filename == '' and len(args) < 1:
	usage()
	sys.exit()

if filename != '':
	createlog(filename + '.log')	
	log('* Hosts file: %s' % (filename));
	scanHostsfile(filename)
elif host != '':
	createlog(host + '.log')	
	log('* Host: %s' % (host));
	scanHost(host)	
else:
	probeType = 'domain'
	createlog(args[0] + '.log')
	log('* Domain: %s' % (args[0]));
	scanDomain(args[0])
