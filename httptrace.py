#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# filename: httptrace.py
# written by 老妖@wooyun
# date: 2014-06-06
#
###############################################################################

import sys, os, getopt, types
import urllib2
import cookielib
from lxml import etree
import sys,socket
import json
import urlparse
import re


def trace(url):
	req = urllib2.Request(url)
	req.add_header('Proxy-Connection', 'Keep-Alive')
	req.add_header('Accept', '*/*')
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0')
	req.get_method = lambda: 'TRACE'
	try:
		response = urllib2.urlopen(req, timeout = 15)
		html = response.read()
		if html.find(r'TRACE / HTTP/') != -1:
			print '* Support TRACE Header'
			print html
	except Exception, e:
		print e

if __name__ == '__main__':
	import locale	
	reload(sys)
	sys.setdefaultencoding(locale.getpreferredencoding())

	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
	urllib2.install_opener(opener)
	
	opts, args = getopt.getopt(sys.argv[1:], "")
	for op, vaule in opts:
		pass

	url = args[0]
	if url[:7] != 'http://' and url[:8] != 'https://':
		url = 'http://' + url

	trace(url)
	
