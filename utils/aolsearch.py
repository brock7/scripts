# -*- encoding: utf-8 -*-

import urllib2
from lxml import etree
import re
import webutils
import sys

AOL_SEARCH_URL = 'http://search.aol.com/aol/search?s_it=topsearchbox.search&v_t=na&page=%d&q=%s'
REQ_TIMEOUT = 15
NUM_PER_PAGE = 10
reqDelay = 0.0
#maxResult = 10
totalRecord = sys.maxint

def _aolSearchPageHandler(opener, url):
	#print url
	#response = opener.open(url, data = None, timeout = 10)
	req = urllib2.Request(url)
	webutils.setupRequest(req) 
	req.add_header('Proxy-Connection', 'Keep-Alive')

	try:
		response = opener.open(req, timeout = REQ_TIMEOUT)
		html = response.read()
		#print html
	except Exception, e:
		print "Exception: url: %s - " % url, e
		raise StopIteration()
	if totalRecord == sys.maxint:
		_updateTotalRecord(html)
	#print html
	tree = etree.HTML(html)
	nodes = tree.xpath(r'//a/@href')
	#print "node count: ", len(nodes), " html len: ", len(html)
	for node in nodes:
		#print node
		m = re.search('/url\?q=([^&]+)', node)
		if m == None:
				url = node
		else:
				url = m.group(1)
		#print node, host, url
		if not _urlFilter(url):
				continue
		yield url

_cookieFetched = False

def _refreshCookie(opener, what):
	global _cookieFetched
	_cookieFetched = True

def _urlFilter(url):
	if url.find('http:') == -1 and url.find('ftp:') == -1 and url.find('https:') == -1:
		return False
	if url.find('google.com') != -1:
		return False
	if url.find('.aol.com') != -1:
		return False
	return True

pattern = re.compile(r'About&nbsp;([0-9,]+)&nbsp;results</div>')
pattern2 = re.compile(r'Your search for ".*?" returned no results')

def _updateTotalRecord(html):
	global totalRecord
	m = pattern2.search(html)
	if m != None:
		totalRecord = 0	
		print 'not found'
		return
	m = pattern.search(html)
	if m == None:
		return
	if len(m.groups()) <= 0:
		return
	totalRecord = int(m.group(1))
	print 'totalRecord', totalRecord

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

def _aolSearch(opener, what, resultNum = -1, startNum = 0):
	
	what = urllib2.quote(what)
	if resultNum == -1:
		pageCount = -1
	else:
		pageCount = int((resultNum + NUM_PER_PAGE - 1) / NUM_PER_PAGE)

	startPage = int((startNum + NUM_PER_PAGE - 1) / NUM_PER_PAGE)

	if not _cookieFetched:
		_refreshCookie(opener, what)

	global totalRecord
	pageNum = 1
	resCnt = 0
	while True:
		if pageCount != -1:
			if pageNum > pageCount:
				break

		url = AOL_SEARCH_URL % ((startPage + pageNum) , what)
		#print url
		# i = 0
		for result in _aolSearchPageHandler(opener, url):
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

google = _aolSearch

if __name__ == '__main__':
	opener = urllib2.build_opener() 
	webutils.setupOpener(opener)
	for url in google(opener, 'site:letv.com'):
		print url

