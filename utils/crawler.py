import urllib2
import re
import urlparse
import webutils

class Crawler(object):
	
	_linkList = set()
	_reexp = re.compile(r"""<a[^>]*?href\s*=\s*['"]?([^'"\s>]{1,500})['">\s]""", 
				re.I | re.M | re.S)
	_scope = '.*'

	def adjustUrl(self, refer, url):
		if re.search(r'^\/\/', url):
			url = 'http:' + url

		urlP = urlparse.urlparse(url)
		if urlP.hostname == None:
			url = urlparse.urljoin(refer, url)
		url = url.replace('&amp;', '&')
		return url
	
	def scanPage(self, url, depth):
		req = urllib2.Request(url)
		webutils.setupRequest(req)
		response = self._opener.open(req)
		if response == None:
			raise StopIteration()
		try:
			html = response.read()
		except:
			raise StopIteration()

		links = self._reexp.findall(html)
		linkRec = set()
		for link in links:
			if re.search(r'^javascript:', link):
				continue
			link = self.adjustUrl(url, link)
			if not link in self._linkList and not link in linkRec:
				if link.find(self._scope) != -1:
					linkRec.add(link)
					yield link
		self._linkList = self._linkList.union(linkRec)
		if self._maxCount >= 0 and len(self._linkList) >= self._maxCount:
		  	raise StopIteration()

		depth -= 1
		if depth <= 0:
			raise StopIteration()

		for link in linkRec:				
			for link2 in self.scanPage(link, depth):
				yield link2

	def crawl(self, opener, url, depth = 2, count = -1, scope = ''):
		assert depth > 0	
		self._startUrl = url
		self._opener = opener
		# FIXME: _scope has a bug. some url isn't in the range 
		if len(scope) <= 0:
			urlP = urlparse.urlparse(url)
			if urlP.hostname.count('.') > 1:
				self._scope = urlP.hostname[urlP.hostname.find('.') + 1:]
			else:
				self._scope = urlP.hostname;

		self._linkList.clear()
		self._maxCount = count

		self._linkList.add(self._startUrl)
		yield self._startUrl

		for url in self.scanPage(self._startUrl, depth):
			yield url

if __name__ == '__main__':
		opener = urllib2.build_opener()
		webutils.setupOpener(opener)
		crawler = Crawler()
		for url in crawler.crawl(opener, 'http://www.letv.com/'):
		 	print url

