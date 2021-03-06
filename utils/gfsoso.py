#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# filename: google.py
# written by 老妖@wooyun
# date: 2014-06-06
#
###############################################################################	

import urllib, urllib2
import cookielib
import re
import sys, getopt
import os
import random
from lxml import etree
import time
import locale
import webutils
import googlesearch

#GOOGLE_HOME = 'http://www.google.com.hk/'
GOOGLE_HOME = 'http://64.233.161.104/'
GFSOSO_HOME = 'http://www.gfsoso.com/'
REQ_TIMEOUT = 15
NUM_PER_PAGE = 10
reqDelay = 0.0
#maxResult = 10
totalRecord = sys.maxint
RedirectedUrl = GFSOSO_HOME
_cookieFetched = False

def _refreshCookie(opener, what):

	what = urllib2.quote(what)
	url = GFSOSO_HOME + '?q=%s' % (what)
	req = urllib2.Request(url)
	webutils.setupRequest(req)
	req.add_header('Referer', GFSOSO_HOME)
	try:
		response = opener.open(req, timeout = REQ_TIMEOUT)
		# print response.geturl()
		if response.geturl().find(GFSOSO_HOME) == -1:
			global RedirectedUrl
			RedirectedUrl = response.geturl()
			RedirectedUrl = RedirectedUrl[0 : RedirectedUrl.find('/', 7) + 1]
			# print 'Redirect', RedirectedUrl
			return False

		html = response.read()
	except Exception, e:
		print e
		html = ''
		if e.code == 301: # moved
			# html = reduce(lambda x,y: x + y, e.readlines())
			for line in e.readlines():
				html += line
		else:
			print "Exception: url: %s - " % url, e
			return False

	m = re.search(r"_GFTOKEN','([0-9a-f]+)'", html)
	
	# print m, m.group(1)
	webutils.cookieJar.set_cookie(_makeCookie('AJSTAT_ok_pages', '1'))
	webutils.cookieJar.set_cookie(_makeCookie('AJSTAT_ok_times', '1'))
	if m:
		webutils.cookieJar.set_cookie(_makeCookie('_GFTOKEN', m.group(1)))
	else:
		return False
	global _cookieFetched
	_cookieFetched = True
	return True

def _urlFilter(url):
	if url.find('http:') == -1 and url.find('ftp:') == -1 and url.find('https:') == -1:
		return False
	if url.find('google.com') != -1:
		return False
	if url.find('gfsoso.com') != -1:
		return False
	if url.find('gfsoso.org') != -1:
		return False
	return True

pattern = re.compile(r'<span>约有([0-9,]+)项结果')
pattern2 = re.compile(r'抱歉，没有找到与“.*?”相关的网页')

def _updateTotalRecord(html):
	global totalRecord
	m = pattern2.search(html)
	if m != None:
		totalRecord = 0	
		#print 'not found'
		return
	m = pattern.search(html)
	if m == None:
		return
	if len(m.groups()) <= 0:
		return
	totalRecord = int(m.group(1).replace(',', ''))
	print 'Total: ', totalRecord

def _gfsosoPageHandler(opener, url):
	req = urllib2.Request(url)
	webutils.setupRequest(req)
	req.add_header('Referer', url[:-4])

	try:
		response = opener.open(req, timeout = REQ_TIMEOUT)
		html = response.read()
		#print html
	except Exception, e:
		print "Exception: url: %s - " % url, e
		raise StopIteration()
	if totalRecord == sys.maxint:
		_updateTotalRecord(html)

	nodes = re.findall(r' href=\\["\'](.*?)\\["\']', html)
	#print nodes
	for node in nodes:
		m = re.search('/url\?q=([^&]+)', node)
		if m == None:
			url = node
		else:
			url = m.group(1)
		if not _urlFilter(url):
			continue
			
		url = url.replace('\\', '')
		# url = url.replace('&amp;', '&')
		url = webutils.escapeHtml(url)
		yield url

def _makeCookie(name, value):
	return cookielib.Cookie(
		version = 0,
		name = name,
		value = value,
		port = None,
		port_specified = False,
		domain = 'www.gfsoso.com',
		domain_specified = True,
		domain_initial_dot = False,
		path = '/',
		path_specified = True,
		secure = False,
		expires = int(time.time()) + 365 * 24 * 3600,
		discard = False,
		comment = None,
		comment_url = None,
		rest = None)

def _gfsosoSearch(opener, what, resultNum = -1, startNum = 0):
	
	#import pdb
	#pdb.set_trace()

	if resultNum == -1:
		pageCount = -1
	else:
		pageCount = int((resultNum + NUM_PER_PAGE - 1) / NUM_PER_PAGE)

	startPage = int((startNum + NUM_PER_PAGE - 1) / NUM_PER_PAGE)

	if not _cookieFetched:
		if not _refreshCookie(opener, what):
			print 'abcd'
			#global _gfsosoPageHandler
			googlesearch.GOOGLE_HOME = RedirectedUrl
			#print RedirectedUrl
			for url in googlesearch.google(opener, what, resultNum, startNum):
				yield url
			return

	global totalRecord
	totalRecord = sys.maxint

	what = urllib2.quote(what)

	pageNum = 1
	resCnt = 0
	while True:
		if pageCount != -1:
			if pageNum > pageCount:
				break

		url = GFSOSO_HOME + '?pn=%d&q=%s&t=1' % ((startPage + pageNum) * 10, what)
		#print url
		# i = 0
		for result in _gfsosoPageHandler(opener, url):
			# i += 1
			resCnt += 1
			yield result
			if resultNum != -1 and resCnt >= resultNum:
				raise StopIteration()
			if resCnt >= totalRecord:
				raise StopIteration()

		if totalRecord == sys.maxint:
			if resultNum == -1:
				totalRecord = sys.maxint - 1
			else:
				totalRecord = resultNum			

		if resCnt >= totalRecord:
			raise StopIteration()
		#if i < NUM_PER_PAGE: # FIXME: if the result total is 10... :(
		#	raise StopIteration()
		#	break
		pageNum += 1
		if reqDelay > 0:
		 	time.sleep(reqDelay)

google = _gfsosoSearch

if __name__ == '__main__':
	opener = urllib2.build_opener() 
	webutils.setupOpener(opener)
	for url in google(opener, 'site:letv.com'):
		print url

