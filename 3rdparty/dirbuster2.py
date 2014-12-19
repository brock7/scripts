import re, urllib,urllib2, time, httplib, socket, sys, md5, locale
from urllib2 import Request, urlopen, URLError, HTTPError
from socket import *
import threading
from bs4 import BeautifulSoup
import urlparse
import mechanize
import webbrowser
import os



hedef = raw_input("Target : ")


url = hedef
tarayici = mechanize.Browser()
urls = [url]
gez = [url]

while len(urls)>0:
    try:
        tarayici.open(urls[0])
        urls.pop(0)
        for link in tarayici.links():
            yeniurl =  urlparse.urljoin(link.base_url,link.url)
            if yeniurl not in gez and url in yeniurl:
                gez.append(yeniurl)
                urls.append(yeniurl)
                print yeniurl
    except:
        pass
