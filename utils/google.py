#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# filename: ghack.py
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

#googleHome = 'http://www.google.com.hk/'
googleHome = 'http://64.233.161.104/'
gfsosoHome = 'http://www.gfsoso.com/'
reqTimeout = 15

def _gfsosoPageHandler(opener, url):
	req = urllib2.Request(url)
	webutils.setupUserAgent(req)
	#print url[:-4]
	req.add_header('Referer', url[:-4])

	try:
		response = opener.open(req, timeout = reqTimeout)
		html = response.read()
		print html
	except Exception, e:
	 	print "url: %s - " % url, e
	 	raise StopIteration()
	nodes = re.findall(r' href=\\["\'](.*?)\\["\']', html)
	print len(nodes)
	for node in nodes:
		m = re.search('/url\?q=([^&]+)', node)
		if m == None:
			url = node
		else:
			url = m.group(1)
		if not url_filter(url, host):
			continue
		url = url.replace('\\', '')
		url = url.replace('&amp;', '&')
		yield url

def make_cookie(name, value):
	return cookielib.Cookie(
		version = 0,
		name = name,
		value = value,
		port = None,
		port_specified=False,
		domain = "www.gfsoso.com",
		domain_specified = True,
		domain_initial_dot = False,
		path = "/",
		path_specified = True,
		secure = False,
		expires = 720,
		discard = False,
		comment = None,
		comment_url = None,
		rest = None
		)

def refreshCookie(opener, what):

	req = urllib2.Request(gfsosoHome)
	response = opener.open(req, timeout = reqTimeout)
	print response.read()

	for handler in opener.handlers:
		if hasattr(handler, 'cookiejar'):
			print 'set cookie'
			handler.cookiejar.set_cookie(make_cookie('AJSTAT_ok_pages', '1'))
			handler.cookiejar.set_cookie(make_cookie('AJSTAT_ok_times', '1'))
			for ck in handler.cookiejar:
				#print dir(ck)
				print 'cookie:', ck


	url = gfsosoHome + '?q=%s' % (what)
	req = urllib2.Request(url)
	webutils.setupUserAgent(req)
	req.add_header('Referer', gfsosoHome)
	try:
		response = opener.open(req, timeout = reqTimeout)
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

def gfsosoSearch(opener, what, resultNum = -1):
	
	NUM_PER_PAGE = 10

	what = urllib2.quote(what)
	if resultNum == -1:
		pageCount = -1
	else:
		pageCount = int((resultNum + NUM_PER_PAGE - 1) / NUM_PER_PAGE)

	refreshCookie(opener, what)
	print "pageCount: ", pageCount
	pageNum = 1
	while True:
		if pageCount != -1:
			if pageNum >= pageCount:
				break

		url = gfsosoHome + '?pn=%d&q=%s&t=1' % (pageNum * 10, what)
		print url
		i = 0
		for result in _gfsosoPageHandler(opener, url):
			i += 1
			yield result
		if i == 0:
			raise StopIteration()
		pageNum += 1

google = gfsosoSearch

if __name__ == '__main__':
	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar)) 
	for url in google(opener, 'ext:xls site:letv.com'):
		print url
