#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# author: Brock | 老妖(laoyaogg@qq.com)
# date: 2014-11-15
# ver: 0.5
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
import locale
#import socket
import string
import codecs

checkAll = False
verbose = False
config = './config'
scanWait = 0
scanType = 0 # 0 list, 1 crawler
scanDepth = 3
notFoundInfo = u'Page Not Found|页面没有找到|找不到页面|页面不存在'
saveCookie = False
cookie = ''
searchPage = 10
googleWhat = ''
ofile = sys.stdout

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

def log(str):
	str += '\n'
	ofile.write(str)
	ofile.flush()
	if ofile != sys.stdout:
		sys.stdout.write(str)

class Tester:
	def scan(self, url, scaner):
		return False

results = [
	"<b>Fatal error</b>:", 
	"Access Denied",
	"Microsoft OLE DB Provider", 
	"You have an error in your SQL syntax", 
	r'ERROR [0-9]+?:', 
	"Forbidden", 
];

class SimpleTester(Tester):
	def scan(self, url, scanner):
		# print 'SimpleTester.scan:', url
		req = urllib2.Request(url)
		response = scanner.sendReq(req)
		if response == None:
			return False
		try:
			if type(response) == types.StringType:
				respText = response
			else:
				if response.geturl() != url and response.geturl() != url + '/':
					# print "REDIRECTED: ", response.geturl(), url
					return False
				respText = response.read()
			#print respText
			if respText[:3] == codecs.BOM_UTF8:
				respText = respText[3:]
			try:
				respText = respText.decode('utf8')
			except:
				pass

			if checkAll:
				scanner.report(url, respText[:512])
				return True

			for p in results:
				if re.search(p , respText, re.IGNORECASE):
					scanner.report(url, respText[:512])
					return True
		except:
			pass
		return False

class Scanner:
	_opener = None	
	_testers = ()
	_progress = False
	_user_agent = 'Firefox'
	def __init__(self):
		pass
	
	def report(self, url, msg):
		if self._progress:
			sys.stdout.write('\n')
			self._progress = False
		log('=' * 60)
		log('[URL] ' + url)
		log('[MESSAGE]')
		log(msg)
		log('=' * 60)

	def sendReq(self, request, data = None, timeout = 15):
		request.add_header('User-agent', self._user_agent)
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
			self._progress = True

	def scan(self):
		#pdb.set_trace()
		# print '=' * 60
		if saveCookie:
			cookieJar = cookielib.CookieJar()
			#"""
			#ck = cookielib.Cookie(version=0, name='Name', value='1', port=None, 
			#		port_specified=False, domain='www.example.com', domain_specified=False, 
			#		domain_initial_dot=False, path='/', path_specified=True, secure=False, 
			#		expires=None, discard=True, comment=None, comment_url=None, 
			#		rest={'HttpOnly': None}, rfc2109=False)
			#cj.set_cookie(ck)
			#"""
			self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		else:
			self._opener = urllib2.build_opener()
		index = random.randint(0, len(user_agents) - 1)
		self._user_agent = user_agents[index]

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
			uri = urllib2.quote(uri.strip())
			if len(uri) <= 0:
				continue
			if uri[0] != '/':
				uri = '/' + uri
			url = self._hostRoot + uri
			yield url

class CrawlerScanner(Scanner):
	
	_linkList = set()
	
	_reexp = re.compile(r"""<a[^>]*?href\s*=\s*['"]?([^'"\s>]{1,500})['">\s]""", 
				re.I | re.M | re.S)
				
	_range = '.*'

	def __init__(self, hostRoot, testers = [SimpleTester()]):
		self._hostRoot = hostRoot
		urlP = urlparse.urlparse(hostRoot)
		
		# FIXME: _range has a bug. some url isn't in the range 
		if urlP.hostname.count('.') > 1:
			self._range = urlP.hostname[urlP.hostname.find('.') + 1:]
		else:
			self._range = urlP.hostname;
		#print urlP.hostname, self._range
		self._testers = testers

	def adjustUrl(self, refer, url):
		if re.search(r'^\/\/', url):
			url = 'http:' + url

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
						yield link
			self._linkList = self._linkList.union(linkRec)
			for link in linkRec:				
				for link2 in self.scanPage(link, depth):
					yield link2

	def getUrls(self):
		self._linkList.add(self._hostRoot)
		yield self._hostRoot
		for url in self.scanPage(self._hostRoot, 0):
			yield url	

import ghack
class GoogleScanner(Scanner):
	def __init__(self, hostRoot, testers = (SimpleTester(), ) ):
		self._hostRoot = hostRoot
		self._testers = testers
	
	def getUrls(self):
		if ghack.opener == None:
			ghack.opener = self._opener
			# global verbose
			ghack.verbose = verbose
			ghack.waitForPerReq = scanWait

		urls = set()
		ghack.google(self._hostRoot, googleWhat, searchPage, 
			lambda url: urls.add(url))
			# print len(self._urls)
		for url in urls:
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
		if re.search(r'\.php$', urlP.path, re.IGNORECASE):
			if url.find('=') != -1:
				url = url.replace('=', '[]=')
				#print url

				req = urllib2.Request(url)
				response = scanner.sendReq(req)
				if response == None:
					return False
				try:
					respText = response.read()
				except:
					return False
				try:
					if respText[:3] == codecs.BOM_UTF8:
						respText = respText[3:]
					respText = respText.decode('utf8')
				except Exception, e:
					pass
				
				if checkAll:
					scanner.report(url, respText[:512])
					return True

				if re.search('Fatal error', respText):
					scanner.report(url, respText[:512])
					return True
		return False

class SqlInjectionTester(Tester):
	def scan(self, url, scaner):
		pass

# /DZ/Data/BACKUP~1/141010~1.SQL OR /DZ/DATA/BACKUP/???.SQL
# guess by date     ~~~~~~~~
# it's effective in winnt
class DZBackupTester(Tester): # FIXME: change to Scanner, not Tester
	def scan(self, url, scanner):
		pass # TODO:

# .git | .svn | .file.swp(vim) | file.bak | dir.rar(zip tar tar.gz tar.bz2 tgz tbz)
class HiddenFileTester(Tester):
	_pathRec = set()
	_textExts = ('entries', 'config', '.bak', '.swp', 
			'.html', '.htm', '.php', '.jsp', '.asp', '.aspx', '.txt')

	def isBinFileType(self, url):
		for ext in self._textExts:
			if url[-len(ext):] == ext:
				return False
		return True

	def isPrintableText(self, content):
		for c in content:
			if not c in string.printable:
				return False
		return True

	def scanUrl(self, url):
		if verbose:
			log('  ->' + url)
		req = urllib2.Request(url)
		response = scanner.sendReq(req)
		if response == None:
			return False
		# print type(response)
		if type(response) == types.StringType:
			respText = response
		else:
			try:
				if response.geturl() != url and response.geturl() != url + '/':
					# jumped, ignore?
					#print response.geturl(), url
					return False
				respText = response.read()
			except:
				return False			
		try:
			if respText[:3] == codecs.BOM_UTF8:
				respText = respText[3:]
			respText = respText.decode('utf8')
		except Exception, e:
			pass
		if self.isBinFileType(url) and self.isPrintableText(respText[:32]):
			return False

		if not re.search(notFoundInfo, respText, re.IGNORECASE):
			scanner.report(url, respText[:512])
			return True

		return False

	_dirs = ('.svn/entries', '.git/config', 
			'backup.zip', 'backup.rar', 'backup.tar.gz', 'backup.tar.bz2', 
			'backup.tgz', 'backup.tbz', 'backup.tar', 'backup.7z')
	
	def scanFixed(self, path, scanner):
		for dir in self._dirs:
			url = path + dir
			self.scanUrl(url)
	
	_ignoreExts = ('.html', '.htm', '.css', '.pdf')

	def isIgnoreFileType(self, url):
		for ext in self._ignoreExts:
			if url[-len(ext):] == ext:
				return True
		return False

	def scanDynamic(self, path, file, scanner):
		urlP = urlparse.urlparse(file)
		try:
			pathItems = os.path.split(urlP.path)
		except:
			return
		#print pathItems
		path2 = path[:-1]; # no last '/'
		curdir = pathItems[0][pathItems[0].rfind('/') + 1 :]
		#print "curdir = " + curdir
		#print path, path2, curdir

		# ignore '.htm', '.html', ...
		if file[-1:] != '/' and not self.isIgnoreFileType(file):
			# http://www.xxx.com/file.php.bak
			files = [path + '.' + pathItems[1] + '.swp', 
				path + pathItems[1] + '.bak', file + '2', 			
				file + '.zip', file + '.rar', file + '.tar.gz', 
				file + '.tar.bz2', file + '.tgz', file + '.tbz', 
				file + '.tar', file + '.7z']
		else:
			files = []

		if len(curdir) > 0:
			files.extend((
				# http://www.xxx.com/dir.zip
				path2 + '.zip', path2 + '.rar', path2 + '.tar.gz', 
				path2 + '.tar.bz2', path2 + '.tgz', path2 + '.tbz', 
				path2 + '.tar', path2 + '.7z', 

				# http//www.xxx.com/dir/ + dir + '.zip' 
				path + curdir + '.zip', path + curdir + '.rar', path + curdir + '.tar.gz', 
				path + curdir + '.tar.bz2', path + curdir + '.tgz', path + curdir + '.tbz', 
				path + curdir + '.tar', path + curdir + '.7z', ))

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
		if len(urlP.fragment) > 0:
			url = url[:url.find('#')]

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
		-N <keyword> extra filter
		-o output file
		-p <searchPage>  default 5
		-s save cookie
		-t <scanType> 0 list, 1 crawler, 2 google. default 0
		-v verbose
		-w wait time."""	
		print helpMsg 
		sys.exit(0)
	
	reload(sys)
	sys.setdefaultencoding(locale.getpreferredencoding())

	opts, args = getopt.getopt(sys.argv[1:], "ad:e:f:hk:n:N:o:st:vw:")
	#print opts
	#print args

	outfile = ''
	for op, value in opts:
		if op == '-a':
			checkAll = True
		elif op == '-d':
			scanDepth = int(value)
		elif op == "-e":
			results.append(value)	
		elif op == "-f":
			config = value
		elif op == '-g':
			googleWhat = value
		elif op == "-h":
			usage()
		elif op == '-k':
			cookie = value
		elif op == '-n':
			notFoundInfo = value.decode(locale.getpreferredencoding())
		elif op == '-N':
			notFoundInfo += '|' + value.decode(locale.getpreferredencoding())
		elif op == '-o':
			outfile = value
		elif op == '-p':
			searchPage = int(value)
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

	urlRoot = args[0]

	if not re.search(r'^http://', urlRoot, re.IGNORECASE):
		urlRoot = 'http://' + urlRoot

	if scanType == 0:
		checkAll = True
		if os.path.isdir(config):
			if config[-1] != '/':
				config += '/'
			ls = os.listdir(config)
			for path in ls:
				if re.search('\.txt$', path, re.IGNORECASE):
					log('List scanning: [' + urlRoot + " " + config + path + ']')
					scanner = ListScanner(urlRoot, config + path)
					scanner.scan()
		else:
			scanner = ListScanner(urlRoot, config)
			scanner.scan()

	elif scanType == 1:
		scanner = CrawlerScanner(urlRoot, (HiddenFileTester(), PhpArrayExposePathTester(), ))
		scanner.scan()
	elif scanType == 2:
		urlP= urlparse.urlparse(urlRoot)
		urlRoot = urlP.hostname
		scanner = GoogleScanner(urlRoot, (HiddenFileTester(), PhpArrayExposePathTester(), ))
		scanner.scan()

