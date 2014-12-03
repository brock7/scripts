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
from utils import webutils

checkAll = False
verbose = False
config = './config'
scanWait = 0
scanType = 0 # 0 list, 1 crawler
scanDepth = 2

notFoundInfo = u'Page Not Found|页面没有找到|找不到页面|页面不存在|^Unknown$|^Bad Request$'
saveCookie = False
cookie = ''
searchCount = -1
googleWhat = ''
ofile = sys.stdout

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
	"^Access Denied$",
	"Microsoft OLE DB Provider", 
	"You have an error in your SQL syntax", 
	r'ERROR [0-9]+?:', 
	"Forbidden", 
];

#import pdb
class SimpleTester(Tester):
	def scan(self, url, scanner):
		#print 'SimpleTester.scan:', url
		#pdb.set_trace()
		req = urllib2.Request(url)
		response = scanner.sendReq(req)
		if response == None:
			return False
		#print response
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
				#pdb.set_trace()
				if not re.search(notFoundInfo, respText, re.IGNORECASE):
					scanner.report(url, respText[:512])
					return True
				else:
					#pdb.set_trace()
				 	return False

			for p in results:
				if re.search(p , respText, re.IGNORECASE):
					scanner.report(url, respText[:512])
					return True
		except:
			raise
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
		#pdb.set_trace()
		# print '=' * 60
		#"""
		#ck = cookielib.Cookie(version=0, name='Name', value='1', port=None, 
		#		port_specified=False, domain='www.example.com', domain_specified=False, 
		#		domain_initial_dot=False, path='/', path_specified=True, secure=False, 
		#		expires=None, discard=True, comment=None, comment_url=None, 
		#		rest={'HttpOnly': None}, rfc2109=False)
		#cj.set_cookie(ck)
		#"""
		self._opener = urllib2.build_opener()
		webutils.setupOpener(self._opener)

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

from utils import crawler
class CrawlerScanner(Scanner):
	def __init__(self, startUrl, testers = [SimpleTester()]):
		self._testers = testers
		self._startUrl = startUrl
		
	def getUrls(self):
		myCrawler = crawler.Crawler()
		for url in myCrawler.crawl(self._opener, self._startUrl):
			yield url

from utils import google
class GoogleScanner(Scanner):
	def __init__(self, hostRoot, testers = (SimpleTester(), ) ):
		self._hostRoot = hostRoot
		self._testers = testers
	
	def getUrls(self):
		gen = google.google(self._opener, 'site:%s %s' % (self._hostRoot, googleWhat), 
				searchCount)
		for url in gen:
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
		-p <search result count>  default 100
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

