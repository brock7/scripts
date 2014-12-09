#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# author: Brock | 老妖(laoyaogg@qq.com)
# date: 2014-11-15
# ver: 0.5
#

import sys, os
reload(sys)
sys.path.append('utils')

import urllib2
import cookielib
import re
import random
#from lxml import etree
import time
import getopt
#import errno
#import pdb
import urlparse
import types
import locale
#import socket
import string
import codecs
from utils import webutils
import importlib

checkAll = False
verbose = False
config = './config'
scanWait = 0
scanType = 0 # 0 list, 1 crawler
scanDepth = 2

saveCookie = False
cookie = ''
searchCount = -1
googleWhat = ''
ofile = sys.stdout
notFoundInfo = u'Page Not Found|页面没有找到|找不到页面|页面不存在|^Unknown$|^Bad Request$'

def log(str):
	str += '\n'
	ofile.write(str)
	ofile.flush()
	if ofile != sys.stdout:
		sys.stdout.write(str)

class Scanner:
	_opener = None	
	_testers = []
	_progress = False
	_user_agent = 'Firefox'

	def __init__(self):
		pass

	@staticmethod
	def log(s):
		log(s)

	def report(self, url, msg):
		if self._progress:
			sys.stdout.write('\n')
			self._progress = False
		log('=' * 60)
		log('[URL] ' + url)
		log('[MESSAGE]')
		log(msg)
		log('=' * 60)

	@staticmethod
	def isNotFoundPage(html):
		return re.search(notFoundInfo, html, re.IGNORECASE) != None

	@staticmethod
	def isCheckAll():
		return checkAll

	@staticmethod
	def isVerbose():
		return verbose

	@staticmethod
	def getCookie():
		return cookie
	
	@staticmethod
	def setupCookie(req):
		if len(cookie) > 0:
			request.add_header('Cookie', cookie)

	def sendReq(self, request, data = None, cookie = '', timeout = 15):
		webutils.setupRequest(request)
		if len(cookie) > 0:
			request.add_header('Cookie', cookie)

		try:
			response = self._opener.open(request, data = data, timeout = timeout)
			if scanWait > 0:
				time.sleep(scanWait)
		except urllib2.HTTPError, e:
			#print e, type(e), dir(e), e.code
			if scanWait > 0:
				time.sleep(scanWait)
			if e.code != 404:
				return e.msg
			else:
				return "Page Not Found"
		except Exception,e:
			if verbose:
				log('Exception: ' + repr(e) + ' at :' + request.get_full_url())
			return None
		except:
			return None
			
		return response
	
	def getUrls(self):
		return ()

	def scanUrl(self, url):
		if verbose:
			log("=>" + url)
		reported = False
		for tester in self._testers:
			if tester.scan(url, self):
				reported = True
		if not verbose and  not reported:
			sys.stdout.write('.')
			sys.stdout.flush()
			self._progress = True

	def scan(self):
		self._opener = urllib2.build_opener()
		webutils.setupOpener(self._opener)

		#records = set()
		urls = self.getUrls()
		for url in urls:
			#if not url in records:
			#	records.add(url)
			self.scanUrl(url)
		return True
	
class ListScanner(Scanner):
	
	def __init__(self, hostRoot, fileName):
		self._hostRoot = hostRoot
		self._fileName = fileName
		
	def getUrls(self):
		for uri in open(self._fileName).readlines():
			uri = urllib2.quote(uri.strip())
			if len(uri) <= 0:
				continue
			if uri[0] != '/':
				uri = '/' + uri
			url = self._hostRoot + uri
			yield url

class SingleScanner(Scanner):
	def __init__(self, url):
		self._url = url
	def getUrls(self):
		yield self._url

from utils import crawler
class CrawlerScanner(Scanner):
	def __init__(self, startUrl):
		self._startUrl = startUrl
		
	def getUrls(self):
		myCrawler = crawler.Crawler()
		for url in myCrawler.crawl(self._opener, self._startUrl):
			yield url

from utils import google
class GoogleScanner(Scanner):
	def __init__(self, keyword):
		self._keyword = keyword
	
	def getUrls(self):
		gen = google.google(self._opener, self._keyword, searchCount)
		for url in gen:
			yield url

def loadTester(scanner, names):
	mods = []
	for name in names:
		m = importlib.import_module('tester.' + name)
		if m == None:
			print 'cannot load tester: ' + name
			sys.exit(-1)
		scanner._testers.append(m)

#####################################################################

if __name__ == "__main__":
	
	def usage():
		helpMsg = sys.argv[0] + """ [opt] host			
		
		-a show all exist page
		-d <depth>	scanning depth
		-e add custom error message
		-f config file. default ./config
		-h show help message
		-k <cookie>	set cookie
		-n <keyword> 'page not found' filter
		-N <keyword> extra 'page not found' filter
		-o output file
		-p <search result count>  default 100
		-s save cookie
		-t <scanType> 0 list, 1 crawler, 2 google, 3 url. default 0
		-v verbose
		-w wait time."""	
		print helpMsg 
		sys.exit(0)
	
	reload(sys)
	sys.setdefaultencoding(locale.getpreferredencoding())

	opts, args = getopt.getopt(sys.argv[1:], "aAd:e:f:hk:m:n:N:o:st:vw:")
	#print opts
	#print args

	outfile = ''
	testerMods = ''

	for op, value in opts:
		if op == '-a':
			checkAll = True
		if op == '-A':
			checkAll = False
		elif op == '-d':
			scanDepth = int(value)
		elif op == "-e":
			results.append(value)	
		elif op == "-f":
			config = value
		#elif op == '-g':
		#	googleWhat = value
		elif op == "-h":
			usage()
		elif op == '-k':
			cookie = value
		elif op == '-m':
			testerMods = value
		elif op == '-n':
			notFoundInfo = value.decode(locale.getpreferredencoding())
		elif op == '-N':
			notFoundInfo += '|' + value.decode(locale.getpreferredencoding())
		elif op == '-o':
			outfile = value
		elif op == '-p':
			searchCount = int(value)
		elif op == '-s':
			saveCookie = True
		elif op == '-t':
			scanType = int(value)
			if scanType == 2:
				saveCookie = True
		elif op == '-v':
			verbose = True
		elif op == "-w":		
			scanWait = float(value)
	
	try:
		if len(outfile) > 0:
			ofile = open(outfile, "w")
	except:
		print 'cannot open: ' + outfile
		sys.exit(-1)

	if len(args) <= 0:
		usage()
		sys.exit(0)

	if scanType == 0:
		if testerMods == '':
			testerMods = 'simple'
		urlRoot = args[0]
		if not re.search(r'^http://', urlRoot, re.IGNORECASE):
			urlRoot = 'http://' + urlRoot

		checkAll = True
		if os.path.isdir(config):
			if config[-1] != '/':
				config += '/'
			ls = os.listdir(config)
			for path in ls:
				if re.search('\.txt$', path, re.IGNORECASE):
					log('List scanning: [' + urlRoot + " " + config + path + ']')
					scanner = ListScanner(urlRoot, config + path)
					loadTester(scanner, testerMods.split(','))
					scanner.scan()
		else:
			scanner = ListScanner(urlRoot, config)
			loadTester(scanner, testerMods.split(','))
			scanner.scan()

	elif scanType == 1:
		if testerMods == '':
			testerMods = 'hidden,php_array'
		urlRoot = args[0]
		if not re.search(r'^http://', urlRoot, re.IGNORECASE):
			urlRoot = 'http://' + urlRoot
		scanner = CrawlerScanner(urlRoot)
		loadTester(scanner, testerMods.split(','))
		scanner.scan()
	elif scanType == 2:
		if testerMods == '':
			testerMods = 'hidden,php_array'
		keyword = args[0]
		scanner = GoogleScanner(keyword)
		loadTester(scanner, testerMods.split(','))
		scanner.scan()
	elif scanType == 3:
		if testerMods == '':
			testerMods = 'hidden,php_array'
		url = args[0]
		scanner = SingleScanner(url)
		loadTester(scanner, testerMods.split(','))
		scanner.scan()

