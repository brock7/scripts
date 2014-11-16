#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# author: Brock | 老妖(laoyaogg@qq.com)
#

import sys, os
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
#import locale
#import socket
import string

checkAll = False
config = './config'
scanWait = 0
scanType = 0 # 0 list, 1 crawler
scanDepth = 3
notFoundInfo = 'Not Found'
saveCookie = False
cookie = ''

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

class Tester:
	def scan(self, url, scaner):
		pass

results = [
	"<b>Fatal error</b>:", 
	"Access Denied",
	"Microsoft OLE DB Provider", 
	"You have an error in your SQL syntax", 
	r'ERROR [0-9]+?:', 
];

class SimpleTester(Tester):
	def scan(self, url, scanner):
		# print url
		req = urllib2.Request(url)
		response = scanner.sendReq(req)
		if response == None:
			return
		try:
			respText = response.read()
			if checkAll:
				scanner.report(url, respText[:512])
				return

			for p in results:
				if re.search(p , respText):
					scanner.report(url, respText[:512])
		except:
			pass

class Scanner:
	_opener = None	
	_testers = ()
	
	def __init__(self):
		pass
	
	def report(self, url, msg):
		print '=' * 60
		print '[URL] ' + url
		print '[MESSAGE] ' + msg
		print '=' * 60
		
	def sendReq(self, request, data = None, timeout = 15):
		index = random.randint(0, len(user_agents) - 1)
		user_agent = user_agents[index]
		request.add_header('User-agent', user_agent)
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
				return None
		except Exception,e:
			print 'Exception:', e
			return None
		except:
			return None
			
		return response
	
	def getUrls(self):
		return ()

	def scanUrl(self, url):
		for tester in self._testers:
			tester.scan(url, self)

	def scan(self):
		#pdb.set_trace()
		# print '=' * 60
		if saveCookie:
			cookieJar = cookielib.CookieJar()
			"""
			ck = cookielib.Cookie(version=0, name='Name', value='1', port=None, 
					port_specified=False, domain='www.example.com', domain_specified=False, 
					domain_initial_dot=False, path='/', path_specified=True, secure=False, 
					expires=None, discard=True, comment=None, comment_url=None, 
					rest={'HttpOnly': None}, rfc2109=False)
			cj.set_cookie(ck)
			"""
			self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		else:
			self._opener = urllib2.build_opener()
		
		urls = self.getUrls()
		
		for url in urls:
			self.scanUrl(url)
		return True
	
class ListScanner(Scanner):
	
	def __init__(self, hostRoot, fileName, testers = (SimpleTester(), ) ):
		self._hostRoot = hostRoot
		self._fileName = fileName
		self._testers = testers
		
	def getUrls(self):
		for uri in open(self._fileName).readlines():
			if uri[0] != '/':
					uri = '/' + uri
			yield self._hostRoot + uri

class CrawlerScanner(Scanner):
	
	_linkList = set()
	
	_reexp = re.compile(r"""<a[^>]*?href\s*=\s*['"]?([^'"\s>]{1,500})['">\s]""", 
				re.I | re.M | re.S)
				
	_range = '.*'

	def __init__(self, hostRoot, testers = [SimpleTester()]):
		self._hostRoot = hostRoot
		urlP = urlparse.urlparse(hostRoot)
		
		if urlP.hostname.count('.') > 1:
			self._range = urlP.hostname[urlP.hostname.find('.') + 1:]
		else:
			self._range = urlP.hostname;
		#print urlP.hostname, self._range
		self._testers = testers

	def adjustUrl(self, refer, url):
		urlP = urlparse.urlparse(url)
		#print 'protocol:',urlP.scheme
		#print 'hostname:',urlP.hostname
		#print 'port:',urlP.port
		#print 'path:',urlP.path
		#print 'query:', urlP.query
		#print 'params', urlP.params
		if urlP.hostname == None:
			url = urlparse.urljoin(refer, url)
		url = url.replace('&amp;', '&')
		return url

	def scanPage(self, url, depth):
		depth += 1
		if depth < scanDepth:
			#print url
			req = urllib2.Request(url)
			response = self.sendReq(req)
			if response == None:
				raise StopIteration()
			try:
				html = response.read()
			except:
				#raise StopIteration()
				html = ''
			#tree = etree.HTML(html)
			#links = tree.xpath(r"/a//@href")			
			links = self._reexp.findall(html)
			#print len(links), links
			linkRec = set()
			for link in links:
				if re.search(r'^javascript:', link):
					continue
				link = self.adjustUrl(url, link)
				if not link in self._linkList and not link in linkRec:
					if link.find(self._range) != -1:
						linkRec.add(link)
						print '=>' + link
						yield link
			self._linkList = self._linkList.union(linkRec)
			for link in linkRec:				
				for link2 in self.scanPage(link, depth):
					yield link2

	def getUrls(self):
		self._linkList.add(self._hostRoot)
		print '=>' + self._hostRoot
		yield self._hostRoot
		for url in self.scanPage(self._hostRoot, 0):
			yield url	

#####################################################################
# vulnerability testers
"""
http://bbs.drvsky.com/read.php?tid[]=2679
Fatal error: Unsupported operand types in /home/wwwroot/drvsky/require/guestfunc.php on line 23
"""
# look like it's no effection now
class PhpArrayExposePathTester(Tester):
	def scan(self, url, scaner):
		urlP = urlparse.urlparse(url)
		if re.search(r'\.php$', urlP.path):
			if url.find('=') != -1:
				url = url.replace('=', '[]=')
				#print url

				req = urllib2.Request(url)
				response = scanner.sendReq(req)
				if response == None:
					return
				try:
					respText = response.read()
				except:
					return
				if checkAll:
					scanner.report(url, respText[:512])
					return

				if re.search('Fatal error', respText):
					scanner.report(url, respText[:512])


class SqlInjectionTester(Tester):
	def scan(self, url, scaner):
		pass

# .git | .svn | .file.swp(vim) | file.bak | dir.rar(zip tar tar.gz tar.bz2 tgz tbz)
class HiddenFileTester(Tester):
	_pathRec = set()
	_textExt = ('entries', 'config', '.bak', '.swp', 
			'.html', '.htm', '.php', '.jsp', '.asp', '.aspx', '.txt')

	def isBinFileType(self, url):
		for ext in self._textExt:
			if url[-len(ext):] == ext:
				return False
		return True

	def isPrintableText(self, content):
		for c in content:
			if not c in string.printable:
				return False
		return True

	def scanUrl(self, url):
		#print url
		req = urllib2.Request(url)
		response = scanner.sendReq(req)
		if response == None:
			return
		# print type(response)
		if type(response) == types.StringType:
			respText = response
		else:
			try:
				respText = response.read()
			except:
				return			
		try:
			respText = respText.decode('utf-8').encode(locale.getdefaultlocale()[1])			
		except Exception, e:
			pass
		if self.isBinFileType(url) and self.isPrintableText(respText[:64]):
			return
		if not re.search(notFoundInfo, respText):
			scanner.report(url, respText[:512])
	
	_dirs = ('.svn/entries', '.git/config', 
			'backup.zip', 'backup.rar', 'backup.tar.gz', 'backup.tar.bz2', 
			'backup.tgz', 'backup.tbz', 'backup.tar', 'backup.7z')
	
	def scanFixed(self, path, scanner):
		for dir in self._dirs:
			url = path + dir
			self.scanUrl(url)
	
	def scanDynamic(self, path, file, scanner):
		urlP = urlparse.urlparse(file)
		pathItems = os.path.split(urlP.path)
		#print pathItems
		path2 = path[:-1];
		path3 = pathItems[0][pathItems[0].rfind('/') + 1 :]
		#print "path3 = " + path3
		#print path, path2, path3
		if file[-1:] != '/':
			files = [path + '.' + pathItems[1] + '.swp', 
				path + pathItems[1] + '.bak', file + '2', 			
				file + '.zip', file + '.rar', file + '.tar.gz', 
				file + '.tar.bz2', file + '.tgz', file + '.tbz', 
				file + '.tar', file + '.7z']
		else:
			files = []
		if len(path3) > 0:
			files.extend((path2 + '.zip', path2 + '.rar', path2 + '.tar.gz', 
				path2 + '.tar.bz2', path2 + '.tgz', path2 + '.tbz', 
				path2 + '.tar', path2 + '.7z', 
				path + path3 + '.zip', path + path3 + '.rar', path + path3 + '.tar.gz', 
				path + path3 + '.tar.bz2', path + path3 + '.tgz', path + path3 + '.tbz', 
				path + path3 + '.tar', path + path3 + '.7z', ))

		for url in files:
			self.scanUrl(url)
		
	def scan(self, url, scanner):
		#print '*** ' + url
		urlP = urlparse.urlparse(url)
		if urlP.path == '':
			url += '/'
		urlP = urlparse.urlparse(url)
		# pathItems = urlP.path.split('/')
		#pathItems = os.path.split(urlP.path)
		if len(urlP.query) <= 0:
			file = url
		else:
			file = url[:url.rfind('?')]
		path = url[:url.rfind(r'/') + 1]
		
		if not path in self._pathRec:
			self._pathRec.add(path)
			self.scanFixed(path, scanner)
		#req = urllib2.Request(url)
		#if file != path:
		self.scanDynamic(path, file, scanner)

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
		-n <keyword> filter out the keyword
		-p <scanType> 0 list 1 crawler. default 0
		-s save cookie
		-w wait time."""	
		print helpMsg 
		sys.exit(0)
	
	opts, args = getopt.getopt(sys.argv[1:], "ad:e:f:hk:n:psw:")
	#print opts
	#print args
	for op, value in opts:
		if op == '-a':
			checkAll = True
		elif op == '-d':
			scanDepth = int(value)
		elif op == "-e":
			results.append(value)	
		elif op == "-f":
			config = value
		elif op == "-h":
			usage()
		elif op == '-k':
			cookie = value
		elif op == '-n':
			notFoundInfo = value
		elif op == '-p':
			scanType = 1
		elif op == '-s':
			saveCookie = True
		elif op == "-w":		
			scanWait = float(value)
	
	urlRoot = args[0]
	
	if config[-1] != '/':
		config += '/'
	
	if not re.search(r'^http://', urlRoot):
		urlRoot = 'http://' + urlRoot
	
	if scanType == 0:
		ls = os.listdir(config)
		for path in ls:
			if re.search('\.txt$', path):
				print 'List scanning: [', urlRoot, config + path, ']'
				scanner = ListScanner(urlRoot, config + path)
				scanner.scan()
	elif scanType == 1:
		scanner = CrawlerScanner(urlRoot, (HiddenFileTester(), PhpArrayExposePathTester(), ))
		scanner.scan()
