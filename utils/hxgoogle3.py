# -*- encoding: utf-8 -*-

import searchbase
import re
import urllib, urllib2 
import webutils
from lxml import etree 

pattern = re.compile(r'<div id="resultStats">找到约 ([0-9,]+) 条结果')
pattern2 = re.compile(r'找不到和您的查询 "<em>.*?</em>" 相符的内容或信息。')

class HxGoogle(searchbase.SearchBase):
    
    def _updateTotalRecord(self, html):

        m = pattern2.search(html)
        if m != None:
            self._totalRecord = 0
            #print 'not found'
            return
            m = pattern.search(html)
        if m == None:
            return
        if len(m.groups()) <= 0:
            return
        self._totalRecord = int(m.group(1).replace(',', ''))
        print 'Total: ', self._totalRecord

    def _pickupLinks(self, html):
        tree = etree.HTML(html)          
        # nodes = tree.xpath(r'/html/body/table[2]/tbody/tr[2]/td[2]/ol/div
        return tree.xpath(r'//h3/a/@href') 


    def _genUrl(self, what, start):        
        return 'http://g2.hxgoogle.com/search.jsp?q=%s&newwindow=1&safe=off&noj=1&hl=zh-CN&start=%d&sa=N' % (what, start)


hx = None

def google(opener, what, resultNum = -1, startNum = 0):
    global hx
    if hx == None:
        hx = HxGoogle(opener)
    return hx.search(what, resultNum, startNum)

if __name__ == '__main__':                         
    opener = urllib2.build_opener()                
    webutils.setupOpener(opener)
    # goo = HxGoogle(opener)

    for url in google(opener, 'site:letv.com', 20):
        print url
 
