import random
import os
import urllib2
import cookielib

userAgents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
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

def getUserAgent():
	index = random.randint(0, len(userAgents) - 1)
	return userAgents[index]
	
def setupRequest(req):
	req.add_header('User-agent', getUserAgent())

cookieJar = None
def setupOpener(opener):
	if os.environ.has_key('save_cookie'):
		global cookieJar
		cookieJar = cookielib.CookieJar() 
		opener.add_handler(urllib2.HTTPCookieProcessor(cookieJar))

	if os.environ.has_key('http_proxy'):
		prx = os.environ['http_proxy'].split(':');
		opener.add_handler(urllib2.ProxyHandler({prx[0]: prx[1]}))
		
topDomainPostfix = (
	'.com','.la','.io',
	'.co',
	'.info',
	'.net',
	'.org',
	'.me',
	'.mobi',
	'.us',
	'.biz',
	'.xxx',
	'.ca',
	'.co.jp',
	'.com.cn',
	'.net.cn',
	'.org.cn',
	'.mx',
	'.tv',
	'.ws',
	'.ag',
	'.com.ag',
	'.net.ag',
	'.org.ag',
	'.am',
	'.asia',
	'.at',
	'.be',
	'.com.br',
	'.net.br',
	'.bz',
	'.com.bz',
	'.net.bz',
	'.cc',
	'.com.co',
	'.net.co',
	'.nom.co',
	'.de',
	'.es',
	'.com.es',
	'.nom.es',
	'.org.es',
	'.eu',
	'.fm',
	'.fr',
	'.gs',
	'.in',
	'.co.in',
	'.firm.in',
	'.gen.in',
	'.ind.in',
	'.net.in',
	'.org.in',
	'.it',
	'.jobs',
	'.jp',
	'.ms',
	'.com.mx',
	'.nl',
	'.nu',
	'.co.nz',
	'.net.nz',
	'.org.nz',
	'.se',
	'.tc',
	'.tk',
	'.tw',
	'.com.tw',
	'.idv.tw',
	'.org.tw',
	'.hk',
	'.co.uk',
	'.me.uk',
	'.org.uk',
	'.vg')

def getTopDomain(url):
	parts = urlparse(url)
	host = parts.netloc
	extractPattern = r'[^\.]+('+'|'.join([h.replace('.',r'\.') for h in topHostPostfix])+')$'
	pattern = re.compile(extractPattern,re.IGNORECASE)
	m = pattern.search(host)
	return m.group() if m else host

