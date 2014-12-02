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

#GOOGLE_HOME = 'http://www.google.com.hk/'
GOOGLE_HOME = 'http://64.233.161.104/'
GFSOSO_HOME = 'http://www.gfsoso.com/'
REQ_TIMEOUT = 15
NUM_PER_PAGE = 10

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

def _gfsosoPageHandler(opener, url):
	req = urllib2.Request(url)
	webutils.setupRequest(req)
	#print url[:-4]
	req.add_header('Referer', url[:-4])

	try:
		response = opener.open(req, timeout = REQ_TIMEOUT)
		html = response.read()
		#print html
	except Exception, e:
	 	print "Exception: url: %s - " % url, e
	 	raise StopIteration()
	nodes = re.findall(r' href=\\["\'](.*?)\\["\']', html)
	# print len(nodes)
	for node in nodes:
		m = re.search('/url\?q=([^&]+)', node)
		if m == None:
			url = node
		else:
			url = m.group(1)
		if not _urlFilter(url):
			continue
			
		url = url.replace('\\', '')
		url = url.replace('&amp;', '&')
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

def _refreshCookie(opener, what):

	#req = urllib2.Request(GFSOSO_HOME)
	#webutils.setupRequest(req)

	#response = opener.open(req, timeout = REQ_TIMEOUT)
	#response.read()
	url = GFSOSO_HOME + '?q=%s' % (what)
	req = urllib2.Request(url)
	webutils.setupRequest(req)
	req.add_header('Referer', GFSOSO_HOME)
	try:
		response = opener.open(req, timeout = REQ_TIMEOUT)
		html = response.read()
		#print html
	except Exception, e:
	 	print "Exception: url: %s - " % url, e
		return
	m = re.search(r"_GFTOKEN','([0-9a-f]+)'", html)
	#print m, m.group(1)
	
	webutils.cookieJar.set_cookie(_makeCookie('AJSTAT_ok_pages', '1'))
	webutils.cookieJar.set_cookie(_makeCookie('AJSTAT_ok_times', '1'))
	webutils.cookieJar.set_cookie(_makeCookie('_GFTOKEN', m.group(1)))
	#for ck in webutils.cookieJar:
	#	print 'cookie:', ck

	"""
	cj = cookielib.CookieJar() 
	cj.set_cookie(make_cookie('AJSTAT_ok_pages', '1'))
	cj.set_cookie(make_cookie('AJSTAT_ok_times', '1'))
	cj.set_cookie(make_cookie('_GFTOKEN', m.group(1)))
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
	req = urllib2.Request(GFSOSO_HOME)
	webutils.setupRequest(req)
	urllib2.install_opener(opener) 
	response = urllib2.urlopen(GFSOSO_HOME, timeout = REQ_TIMEOUT)
	print response.read()
	sys.exit(-1)
	"""

	"""
	for handler in opener.handlers:
		if hasattr(handler, 'cookiejar'):
			print 'set cookie'
			handler.cookiejar.set_cookie(make_cookie('AJSTAT_ok_pages', '1'))
			handler.cookiejar.set_cookie(make_cookie('AJSTAT_ok_times', '1'))
			for ck in handler.cookiejar:
				#print dir(ck)
				print 'cookie:', ck


	url = GFSOSO_HOME + '?q=%s' % (what)
	req = urllib2.Request(url)
	webutils.setupRequest(req)
	req.add_header('Referer', GFSOSO_HOME)
	try:
		response = opener.open(req, timeout = REQ_TIMEOUT)
		html = response.read()
		print html
	except Exception, e:
	 	print "url: %s - " % url, e
		return
	m = re.search(r"_GFTOKEN','([0-9a-f]+)'", html)
	print m
	print m.group(1)
	for handler in opener.handlers:
		if hasattr(handler, 'cookiejar'):
			print 'set cookie'
			handler.cookiejar.set_cookie(make_cookie('_GFTOKEN', m.group(1)))

			for ck in handler.cookiejar:
				print dir(ck)
				print 'cookie:', ck
	"""

def _gfsosoSearch(opener, what, resultNum = -1):
	

	what = urllib2.quote(what)
	if resultNum == -1:
		pageCount = -1
	else:
		pageCount = int((resultNum + NUM_PER_PAGE - 1) / NUM_PER_PAGE)

	_refreshCookie(opener, what)
	#print "pageCount: ", pageCount
	pageNum = 1
	while True:
		if pageCount != -1:
			if pageNum >= pageCount:
				break

		url = GFSOSO_HOME + '?pn=%d&q=%s&t=1' % (pageNum * 10, what)
		#print url
		i = 0
		for result in _gfsosoPageHandler(opener, url):
			i += 1
			yield result
		if i < NUM_PER_PAGE:
			raise StopIteration()
		pageNum += 1

google = _gfsosoSearch

if __name__ == '__main__':
	opener = urllib2.build_opener() 
	webutils.setupOpener(opener)
	for url in google(opener, 'site:letv.com'):
		print url
