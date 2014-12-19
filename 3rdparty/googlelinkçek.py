import urllib
import re
import sys
import mechanize
from urlparse import urlparse
 
def search(q,result,page):
 
        br = mechanize.Browser()
        br.set_handle_robots(False) # bypass google check
        br.addheaders= [('User-agent','firefox')]
        query = q.replace(" ","+")
        google = "http://www.google.com/search?num="+result+"&q="+query+"&start="+page
        htmltext = br.open(google).read()
        pattern = re.compile("<h3 class=\"r\"><a href=\"/url\?q=(.*?)&amp.*?\">.*?</a></h3>") # grep url
        found = re.findall(pattern,htmltext)
       
        for i in found:
                url = urlparse(i).netloc
                #url = urllib.unquote(i).decode('utf8')
                print url
       
query = sys.argv[1]
result = sys.argv[2]
 
page = ['0','100','200','300','400','500','600','700','800','900'] # 900 is maximum
 
for i in page:
        search(query,result,i)
