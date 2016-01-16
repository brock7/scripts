# -*- encoding: utf-8 -*-

import searchbase
import re
import urllib, urllib2 
import webutils
from lxml import etree 

class Googto(searchbase.SearchBase):
    
    _totalRecordPattern = re.compile(r'找到约 ([0-9,]+) 条结果')

    def _updateTotalRecord(self, html):
        m = self._totalRecordPattern.search(html)
        if m == None:                                     
            # print '* Not found 1'
            return
        if len(m.groups()) <= 0:
            # print '* Not found 2'
            return
        self._totalRecord = int(m.group(1).replace(',', ''))    
        print '* Total:', self._totalRecord                     


    def _pickupLinks(self, html):
        tree = etree.HTML(html)          
        # nodes = tree.xpath(r'/html/body/table[2]/tbody/tr[2]/td[2]/ol/div
        return tree.xpath(r'//h3/a/@href') 


    def _genUrl(self, what, start):        
        return 'http://www.googto.com/?q=%s&start=%d' % (what, start)

if __name__ == '__main__':                         
    opener = urllib2.build_opener()                
    webutils.setupOpener(opener)
    googto = Googto(opener)

    for url in googto.search('site:letv.com', 10):
        print url                                  
                                          
