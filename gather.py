#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# filename: gather.py
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

noTitle = False
def encoding(data):
	if len(data) <= 0:
		return data
	encodings = ['utf-8', 'gbk', 'gb2312']   #可以添加其他字符编码
	for encoding in encodings:
		try:
			return data.decode(encoding)
		except:
			pass
	return data

def getTitle(domain):
	global noTitle
	if noTitle:
		return ''

	try:
		if domain[:7] != 'http://':
			domain = 'http://' + domain
		response = urllib2.urlopen(domain, timeout = 15)
		tree = etree.HTML(encoding(response.read()))
		nodes = tree.xpath("/html/head/title/text()")
		# nodes = tree.xpath("/html/head/title") # 没有 text() 时，返回节点对象，用 nodes[0].text 访问
		if len(nodes) >= 1:
			return nodes[0]
		else:
			return 'No Title'
	except Exception, e:
		if hasattr(e, 'msg'):
			return 'Error: ' + e.msg
		return 'Error: ' + repr(e)

def querySubdomain(domain):
	# all in on page
	response = urllib2.urlopen('http://i.links.cn/subdomain/', data = 'domain=%s&b2=1&b3=1&b4=1' % domain)
	tree = etree.HTML(response.read())
	nodes = tree.xpath("//a[@rel='nofollow']/@href")
	for node in nodes:
		print node, getTitle(node)

def queryRDNS_old(domain):
	hostInfos = socket.gethostbyname_ex(domain) #r = (hostname, aliaslist, ipaddrlist)
	for ipaddr in hostInfos[2]:
		maxpage = 1
		page = 1
		print '[IP Address: ' + ipaddr + ']'
		try:
			while page <= maxpage:
				response = urllib2.urlopen('http://dns.aizhan.com/index.php?r=index/domains&ip=%s&page=%d' % 
						(ipaddr, page))
				jtext = response.read()
				if len(jtext) <= 0:
					break
				j = json.loads(jtext)
				if j == None:
					break
				#print j.keys()
				if j['maxpage'] != None:
					maxpage = int(j['maxpage'])
				for name in j['domains']:
					print name, getTitle(name)
				page += 1
		except Exception, e:
			print e
			#pass

def queryRDNS(domain):
	hostInfos = socket.gethostbyname_ex(domain) #r = (hostname, aliaslist, ipaddrlist)
	for ipaddr in hostInfos[2]:

            print '[IP Address: ' + ipaddr + ']'
            # 翻页
            for i in range(5): # 最多5页，需要更多到网页上去看
                try:
                    response = urllib2.urlopen('http://dns.aizhan.com/%s/%d/' % (ipaddr, i))
                    text = response.read()
                    tree = etree.HTML(text)       
                    nodes = tree.xpath(r"//td[@class='dns-links']/a/@href")
                    if len(nodes) == 0:
                        break
                    for node in nodes:
                        print node, getTitle(node)
                except Exception, e: 
                    print e


def toStr(l):
	#print type(l)
	if type(l) != types.ListType:
		return l
	result = ''
	for item in l:
		if type(item) == types.ListType:
			for v in itme:
				result += '%s, ' % v
		elif type(item) == types.DictType:
			for (k, v) in item.items():
				result += '%s: %s ' % (k, v)
		else:
			result += str(item) + ', '
	return result


def queryWhois(domain):
	# fetch cookie
	if domain.count('.') > 1:
		domain = domain[domain.find('.') + 1:]
	urllib2.urlopen('http://whois.www.net.cn/whois/domain/%s' % domain)
	response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois?host=%s' % domain)
	jbase = json.loads(response.read())
	if jbase['success']:
		for (k, v) in jbase['module'].items():
			print k if k[-1:] == ':' else k + ': ', toStr(v) 

	response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois_full?host=%s' % domain)
	jdetail = json.loads(response.read())
	if jdetail['success']:
		for (k, v) in jdetail['module'].items():
			print k if k[-1:] == ':' else k + ': ', toStr(v)

def queryWeight(domain):
	url = 'http://mytool.chinaz.com/baidusort.aspx?host=%s&sortType=0' % domain
	response = urllib2.urlopen(url)
	tree = etree.HTML(encoding(response.read()))
	nodes = tree.xpath("/html/body/div/div[5]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/font[1]/text()")
	if len(nodes) <= 0:
		print 'No data'
	else:
		print 'Baidu Weight: ', nodes[0]
	
def nmap(domain):
	os.system('nmap -sV %s' % domain)

def baseInfo(url):
	req = urllib2.Request(url)
	req.add_header('Proxy-Connection', 'Keep-Alive')
	req.add_header('Accept', '*/*')
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0')

	req.get_method = lambda: 'OPTIONS'
	try:
		response = urllib2.urlopen(req, timeout = 15)
		#html = response.read()
		#for k, v in response.info().items():
		#	print k,v 
		if 'Allow' in response.info():
			print 'Allow: ' +  response.info().getheader('Allow')
	except:
		pass

	req.get_method = lambda: 'GET'
	try:
		response = urllib2.urlopen(req, timeout = 15)
		#for k, v in response.info().items():
		#	print k,v 
		if 'Allow' in response.info():
			print 'Allow: ' +  response.info().getheader('Allow')

		if response.info().getheader('Server'):
			print 'Server: ' + response.info().getheader('Server')

		if response.info().getheader('X-Powered-By'):
			print 'Powered By: ' + response.info().getheader('X-Powered-By')
	except:
		pass

	req = urllib2.Request(url)
	req.add_header('Proxy-Connection', 'Keep-Alive')
	req.add_header('Accept', '*/*')
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0')
	req.add_header('Command', 'stop-debug')
	req.get_method = lambda: 'DEBUG'
	try:
		response = urllib2.urlopen(req, timeout = 15)
		if response.read().find(r'OK') != -1:
			print '* Support Debug Method'
	except Exception, e:
		pass
#		if hasattr(e, 'code'):
#			if not (e.code == 501 or e.code == 405 or e.code == 403):
#				print 'DEBUG: ', e

	req = urllib2.Request(url)
	req.add_header('Proxy-Connection', 'Keep-Alive')
	req.add_header('Accept', '*/*')
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0')
	req.get_method = lambda: 'TRACE'
	try:
		response = urllib2.urlopen(req, timeout = 15)
		if response.read().find(r'TRACE / HTTP/') != -1:
			print '* Support TRACE Method'
	except Exception, e:
		pass

def querySiteFile(url):
	files = ( ('robots.txt', 'Allow|Disallow'), ('crossdomain.xml', 'cross-domain-policy'), 
		('phpinfo.php', 'PHP Version'), ('sitemap.xml', 'schemas\/sitemap'), )
	for file in files:
		try:
			response = urllib2.urlopen(url + '/' + file[0], timeout = 15)
			html = response.read()
			if not re.search(file[1], html, re.IGNORECASE):
				continue
			print '[%s]' % file[0]
			print html[:4096]
		except:
			#raise
			pass

if __name__ == '__main__':
	import locale	
	reload(sys)
	sys.setdefaultencoding(locale.getpreferredencoding())

	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
	urllib2.install_opener(opener)
	
	options = 0
	opts, args = getopt.getopt(sys.argv[1:], "fNrswb")
	for op, vaule in opts:
		if op == '-N':
			noTitle = True
		elif op == '-r':
			options |= 1
		elif op == '-s':
			options |= 2
		elif op == '-w':
			options |= 4
		elif op == '-b':
			options |= 16
		elif op == '-f':
			options |= 32

	if options == 0:
		options = 1 | 2 | 4 | 8 | 16 | 32
	url = args[0]
	if url[:7] != 'http://' and url[:8] != 'https://':
		url = 'http://' + url

	baseInfo(url)
	
	urlP = urlparse.urlparse(url)

	if options & 1:
		print '\n============================== reverse dns ==============================\n'
		queryRDNS(urlP.hostname)
	if options & 2:
		print '\n============================== subdomain ==============================\n'
		querySubdomain(urlP.hostname)
	if options & 4:
		print '\n============================== whois ==============================\n'
		queryWhois(urlP.hostname)
	if options & 16:
		print '\n============================== baidu weight ==============================\n'
		queryWeight(urlP.hostname)
	if options & 32:
		print '\n============================== site file ==============================\n'
		querySiteFile(url[:url.find('/', 8)])
	if options & 8:
		print '\n============================== nmap ==============================\n'
		sys.stdout.flush()
		nmap(urlP.hostname)
	sys.exit(0)

