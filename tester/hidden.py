import urllib2
import re
import types
import urlparse
import sys, os
import string
from utils import webutils

# .git | .svn | .file.swp(vim) | file.bak | dir.rar(zip tar tar.gz tar.bz2 tgz tbz)
class HiddenFileTester:
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

	def scanUrl(self, url, scanner):
		if scanner.isVerbose():
			scanner.log('  ->' + url)
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
			respText = webutils.decodeHtml(respText)
			if respText[:3] == codecs.BOM_UTF8:
				respText = respText[3:]
			#respText = respText.decode('utf8')
		except Exception, e:
			pass
		if self.isBinFileType(url) and self.isPrintableText(respText[:32]):
			return False

		if not scanner.isNotFoundPage(respText):
			scanner.report(url, respText[:512])
			return True

		return False

	_dirs = ('.svn/entries', '.git/config', 
			'backup.zip', 'backup.rar', 'backup.tar.gz', 'backup.tar.bz2', 
			'backup.tgz', 'backup.tbz', 'backup.tar', 'backup.7z')
	
	def scanFixed(self, path, scanner):
		for dir in self._dirs:
			url = path + dir
			self.scanUrl(url, scanner)
	
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
			self.scanUrl(url, scanner)
		
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

def scan(url, scanner):
	t = HiddenFileTester()
	t.scan(url, scanner)

