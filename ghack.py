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
from utils.google import google
from utils import webutils

opener = None
verbose = True
waitForPerReq = 0.0
searchPage = 1

hacks = ('ext:xls', 'ext:xlsx', 'ext:doc', 'ext:docx', 'ext:txt', 'ext:zip', 
	'ext:conf', 'ext:rar', 'ext:sh', 'ext:gz', 'ext:bz2', 'ext:tar', 'ext:tgz', 
	'ext:mdb', 'ext:ini', 'ext:7z', 'ext:cgi', "#", 
	'inurl:filename', 'inurl:upload', 'inurl:profile 管理员', 'inurl:cgi-bin', 
	'inurl:file', 'inurl:down', 'inurl:passwd', 'inurl:path', "#", 
	'intitle:"index.of"', 'intitle:管理 ', "#",
	'intext:*@*.com', 'intext:*@*.net', 'intext:*@*.cn', 'intext:ftp://*:* ',  
	'intext:powered by', 
	)

def googleHackLocal(host):
	#print('******* google hack: ' + host)
	count = 0
	for hack in hacks:
		if hack == '#':
			#time.sleep(5)
			continue
		print '******* [google] site:%s %s *******' % (host, hack)
		try:
			for url in google(opener, 'site:%s %s' % (host, hack), 20):
				print ' ' + url
		except Exception,e:
			print 'Exception', e
			raise
			
		time.sleep(random.randint(2, 5))
		if count % 10 == 0:
			time.sleep(10)
		count = count + 1

def googleHackGhdb(host):
	return # Disabled
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
	opts, args = getopt.getopt(sys.argv[1:], "hlp:g:GP:vw:")
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
		elif op == '-h':
			usage()
			sys.exit(0)
		elif op == '-P':
			searchPage = int(value)
		elif op == '-v':
			verbose = True
		elif op == '-w':
			what = value
	if len(args) == 0:
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
		google(args[0], what, page = searchPage)
		sys.exit(0)
	googleHackLocal(args[0])
	if not localOnly:
		googleHackGhdb(args[0])		

	print 'Done!'
