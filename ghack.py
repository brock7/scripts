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

from StringIO import StringIO
import gzip

from utils.google import google
from utils import webutils

opener = None
verbose = True
waitForPerReq = 1.0
searchPage = 1
resultCount = 20

hacks = ('ext:xls', 'ext:xlsx', 'ext:doc', 'ext:docx', 'ext:txt', 'ext:zip', 
	'ext:conf', 'ext:rar', 'ext:sh', 'ext:gz', 'ext:bz2', 'ext:tar', 'ext:tgz', 
	'ext:mdb', 'ext:ini', 'ext:7z', 'ext:cgi', 'ext:py', "#", 
	'inurl:filename', 'inurl:upload', 'inurl:profile 管理员', 'inurl:cgi', #'inurl:cgi-bin', 
	'inurl:file', 'inurl:down', 'inurl:passwd', 'inurl:path', "#", 
	'intitle:"index.of"', 'intitle:管理 ', "#",
	'intext:*@*.com', 'intext:*@*.net', 'intext:*@*.cn', 'intext:ftp://*:* ',  
	'intext:powered by', 
	)

def googleHackLocal(host):
	#import pdb
	#pdb.set_trace()
	#print('******* google hack: ' + host)
	count = 0
	for hack in hacks:
		if hack == '#':
			#time.sleep(5)
			continue
		print '******* [google] site:%s %s *******' % (host, hack)
		try:
			for url in google(opener, 'site:%s %s' % (host, hack), resultCount):
				print '     [#] ' + url.decode('utf-8')
		except Exception,e:
			print 'Exception', e
			raise
			
		time.sleep(random.randint(2, 5))
		if count % 10 == 0:
			time.sleep(10)
		count = count + 1

def googleHackGhdb(host):
	#return # Disabled
	print '******* Hack exploit-db/GHDB *******'
	i = 3977
	count = 0
	pattern = re.compile(r'Google search: <a href=\"http://www.google.com/search\?.*?q\=([^"]+)')
	while True:
		req = urllib2.Request('http://www.exploit-db.com/ghdb/%d/' % i)
		webutils.setupRequest(req)
		req.add_header('Accept-Encoding', 'gzip,deflate')
		try:
			response = opener.open(req, timeout = 15)
			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO( response.read())
				f = gzip.GzipFile(fileobj=buf)
				html= f.read()
			else:
				html = response.read()
		except:
			continue
		#print html
		res = pattern.search(html)
		if res == None:
			#print str(html)
			#break
			continue
		if len(res.groups()) <= 0:
			continue
		#res = urllib.unquote_plus(res.group(1))
		what = webutils.escapeHtml(res.group(1))
		print '******* [google] [GHDB: %d] site:%s %s *******' % (i, host, what)
		for url in google(opener, 'site:%s %s' % (host, what), resultCount):
			print '    [#] ' + url.decode('utf-8')
		i -= 1
		if i <= 0:
			break

		time.sleep(random.randint(2, 5))
		if count % 10 == 0:
			time.sleep(10)
		count = count + 1

#####################################################################

if __name__ == "__main__":
	#import pdb
	#pdb.set_trace()
	import locale
	reload(sys)
	sys.setdefaultencoding(locale.getpreferredencoding())

	def usage():
		print 'ghack.py [op] host'
		print '\t-l\t\tseach local GHDB only'
		print '\t-g <host>\tredirect google'
		print '\t-p <proxy>\tindicate proxy. example http@localhost:8080'	
		print '\t-h\t\thelp message'
		print '\n\texample:\n\t\tghack.py www.example.com'

	localOnly = False
	remoteOnly = False
	opts, args = getopt.getopt(sys.argv[1:], "hln:p:g:GP:rvw:")
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
		elif op == '-G':
			google = googleSearch
		elif op == '-n':
			resultCount = int(value)
			#print resultCount
		elif op == '-h':
			usage()
			sys.exit(0)
		elif op == '-P':
			searchPage = int(value)
		elif op == '-r':
			remoteOnly = True
		elif op == '-v':
			verbose = True
		elif op == '-w':
			what = value
	if len(args) == 0 and len(what) == 0:
		usage()
		sys.exit(0)

	try:
		opener = urllib2.build_opener()
		webutils.setupOpener(opener)
	except Exception,e:
		print 'Exception:', e
		raise
		sys.exit(-1)
		
	if len(what) > 0:
		# google(args[0], what, page = searchPage)
		for url in google(opener, what, resultCount):
			print url.decode('utf-8')
		sys.exit(0)
	if not remoteOnly:
		googleHackLocal(args[0])
	if not localOnly:
		googleHackGhdb(args[0])		

	print 'Done!'
