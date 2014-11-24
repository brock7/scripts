import sys, os
import urllib2
import cookielib
from lxml import etree
import sys,socket
import json

opener = None

def getTitle(domain):
	try:
		if domain[:7] != 'http://':
			domain = 'http://' + domain
		response = urllib2.urlopen(domain)
		tree = etree.HTML(response.read())
		nodes = tree.xpath("/html/head/title")
		if len(nodes) >= 1:
			return nodes[0].text
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

def queryRDNS(domain):
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

def queryWhois(domain):
	# fetch cookie
	urllib2.urlopen('http://whois.www.net.cn/whois/domain/cankaoxiaoxi.com')
	response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois?host=cankaoxiaoxi.com')
	jbase = json.loads(response.read())
	for (k, v) in jbase['module'].items():
		print k, v
	response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois_full?host=cankaoxiaoxi.com')
	jdetail = json.loads(response.read())
	for (k, v) in jdetail['module'].items():
		print k + ':', v

def nmap(domain):
	pass # TODO: 

if __name__ == '__main__':
	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
	urllib2.install_opener(opener)
	print '============================== subdomain =============================='
	querySubdomain(sys.argv[1])
	print '============================== reverse dns =============================='
	queryRDNS(sys.argv[1])
	print '============================== whois =============================='
	queryWhois(sys.argv[1])
	print '============================== nmap =============================='
	nmap(sys.argv[1])
	sys.exit(0)

