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

googleHome = 'http://www.google.com.hk/'
gfsosoHome = 'http://www.gfsoso.com/'
reqTimeout = 15
opener = None
verbose = True
waitForPerReq = 0.0
searchPage = 1

hacks = ('ext:xls', 'ext:xlsx', 'ext:doc', 'ext:docx', 'ext:txt', 'ext:zip', 
	'ext:conf', 'ext:rar', 'ext:sh', 'ext:gz', 'ext:bz2', 'ext:tar', 'ext:tgz', 
	'ext:mdb', 'ext:ini', 'ext:7z', 'ext:cgi', "#", 
	'inurl:filename', 'inurl:upload', 'inurl:profile 管理员', 
	'inurl:file', 'inurl:down', 'inurl:passwd', 'inurl:path', "#", 
	'intitle:"index.of"', 'intitle:管理 ', "#",
	'intext:*@*.com', 'intext:*@*.net', 'intext:*@*.cn', 'intext:ftp://*:* ',  
	'intext:powered by', 
	)

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

def url_filter(url, host):
	#print host
	if url.find(host) == -1:
		return False
	if url.find('http://translate.google') != -1:
		return False
	if url.find('.google.') != -1:
		return False
	if url.find('http://webcache.googleusercontent') != -1:
		return False
	if url.find('http:') == -1 and url.find('ftp:') == -1:
		return False
	if url.find('youtube') != -1:
		return False		
	return True

def requestUrl(url):
	global opener
	request = urllib2.Request(url)
	index = random.randint(0, len(user_agents) - 1)
	user_agent = user_agents[index]
	request.add_header('User-agent', user_agent)

	response = opener.open(request, data = None, timeout = reqTimeout)
	return response

def defaultReport(url):
	print url

def googleSearch(host, what, page = 1, report = defaultReport):
	global opener
	if verbose:
		print(('\n* google site:%s %s' % (host, what)).\
			decode('utf-8').encode(sys.getfilesystemencoding()))
	what = urllib2.quote("site:%s %s" % (host, what))
	url = googleHome + 'search?hl=en&num=100&q=%s' % what
	#print url
	#response = opener.open(url, data = None, timeout = 10)
	response = requestUrl(url)
	#print 'after'
	html = response.read()
	#print html
	tree = etree.HTML(html)
	nodes = tree.xpath(r"/a//@href")
	#print "node count: ", len(nodes), " html len: ", len(html)
	#nodes = re.findall(r' href=["\'](.*?)["\']', html)
	for node in nodes:
		#print node
		m = re.search('/url\?q=([^&]+)', node)
		if m == None:
			url = node
		else:
			url = m.group(1)
		#print node, host, url
		if not url_filter(node, host):
			continue
		report(url)
	return

def gfsosoSearch(host, what, page = 1, report = defaultReport):
	#import pdb
	#pdb.set_trace()
	global opener
	if verbose:
		print(('\n* google site:%s %s' % (host, what)).\
			decode('utf-8').encode(sys.getfilesystemencoding()))
	
	what = urllib2.quote("site:%s %s" % (host, what))
	#print what
	for i in range(page):
		url = gfsosoHome + 'search?hl=en&pn=%d&q=%s' % (i * 10, what)
		#print url
		#response = opener.open(url, data = None, timeout = 10)
		try:
			response = requestUrl(url)
		except Exception,e :
			print 'cannot open %s(%s)' % (url, repr(e))
			return
		#print 'after'
		html = response.read()
		#print html
		#tree = etree.HTML(html)
		#nodes = tree.xpath(r"/a//@href")
		nodes = re.findall(r' href=\\["\'](.*?)\\["\']', html)
		#print "node count: ", len(nodes), " html len: ", len(html)
		for node in nodes:
			#print node
			m = re.search('/url\?q=([^&]+)', node)
			if m == None:
				url = node
			else:
				url = m.group(1)
			#print node, host, url
			if not url_filter(url, host):
				continue

			url = url.replace('\\', '')
			url = url.replace('&amp;', '&')
			report(url)
			if waitForPerReq > 0:
				time.sleep(waitForPerReq)
	return

google = gfsosoSearch

def refreshCookie():
	global cookieJar
	#global opener
	try:
		cookieJar.clear()
		time.sleep(random.randint(15, 30))
		requestUrl(googleHome)
		
	except Exception,e:
		print 'refreshing cookie failed.'
		print e
		return False
	return True
	
def googleHackLocal(host):
	print('******* google hack: ' + host)
	count = 0
	for hack in hacks:
		if hack == '#':
			#time.sleep(5)
			continue
		retry = 0
		while retry < 3:
			try:
				google(host, hack)
			except Exception,e:
				print 'Error occuptted'
				print e
				print 'Refreshing cookie...'
				refreshCookie()
				retry += 1
				continue
			break			
			
		#time.sleep(5 if random.random() > 0.5 else 3)
		time.sleep(random.randint(3, 7))
		if count % 10 == 0:
			time.sleep(30)
		count = count + 1

def googleHackGhdb(host):
	print '******* Hack exploit-db/GHDB'
	i = 2
	while True:
		html = urllib2.urlopen('http://www.exploit-db.com/ghdb/%d/' % i).read()
		# FIXME: sometime result is unavaliable
		#print html
		res = re.search(r'Google search: <a href=\"http://www.google.com/search\?.*?q\=([^"]+)', html)
		if res == None:
			#print str(html)
			break
		res = urllib.unquote_plus(res.group(1))
		google(host, res)
		i += 1
	pass

#####################################################################

if __name__ == "__main__":
	#import pdb
	#pdb.set_trace()
	def usage():
		print 'ghack.py [op] host'
		print '\t-l\t\tseach local GHDB only'
		print '\t-g <host>\tredirect google'
		print '\t-p <proxy>\tindicate proxy. example http@localhost:8080'	
		print '\t-h\t\thelp message'
		print '\n\texample:\n\t\tghack.py www.example.com'

	localOnly = False
	opts, args = getopt.getopt(sys.argv[1:], "hlp:g:P:w:")
	cookieJar = None
	proxy = ""
	what = ""
	for op, value in opts:
		if op == '-l':
			localOnly = True
		elif op == '-p':
			proxy = value
		elif op == '-g':
			googleHome = value
		elif op == '-h':
			usage()
			sys.exit(0)
		elif op == '-P':
			searchPage = int(value)
		elif op == '-w':
			what = value
		if len(args) == 0:
			usage()
			sys.exit(0)

	try:
		#获取Cookiejar对象（存在本机的cookie消息）
		cookieJar = cookielib.CookieJar()
		#自定义opener,并将opener跟CookieJar对象绑定
		if len(proxy) > 0:
			prxList = []
			proxies = proxy.split(',')
			for proxy in proxies:
				prx = proxy.split('@')
				if len(prx) >= 2:						
					prxList.append(urllib2.ProxyHandler({prx[0]: prx[1]}))
	
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), *prxList)
		else:
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
				
		"""
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), 
			urllib2.ProxyHandler({'https': 'localhost:18080'}), 
			urllib2.ProxyHandler({'http': 'localhost:18080'}))
		"""
		#安装opener,此后调用urlopen()时都会使用安装过的opener对象
		urllib2.install_opener(opener)			
		#requestUrl(googleHome)
		#time.sleep(3)
	except Exception,e:
		print 'Initializing failed'
		print e
		raise
		sys.exit(-1)
		
	# user_agent = user_agents[random.randint(0, len(user_agents) - 1)]
	if len(what) > 0:
		google(args[0], what, page = searchPage)
		sys.exit(0)
	googleHackLocal(args[0])
	if not localOnly:
		googleHackGhdb(args[0])		

	print 'Done!'
