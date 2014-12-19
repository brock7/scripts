import sys
import urlparse
import urllib  
import mechanize
from bs4 import BeautifulSoup
 
site = sys.argv[1]
urls = [site]
visited = [site]
 
print "Crawling => "+site
print
 
for url in urls:
 
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
        urls.pop(0)
 
        for a in soup.findAll('a',href=True):
                a['href'] = urlparse.urljoin(site,a['href'])
                url = urllib.unquote(a['href']).decode('utf8').replace(" ","+")
 
                if site in url and url not in visited:
                        urls.append(url)
                        visited.append(url)
                        print url
