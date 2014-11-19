import urllib2
import cookielib
from lxml import etree

cookieJar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
urllib2.install_opener(opener)

urllib2.urlopen('http://whois.www.net.cn/whois/domain/cankaoxiaoxi.com')
response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois?host=cankaoxiaoxi.com')
print response.read()
response = urllib2.urlopen('http://whois.www.net.cn/whois/api_whois_full?host=cankaoxiaoxi.com')
print response.read()

