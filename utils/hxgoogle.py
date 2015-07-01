import urllib, urllib2
import cookielib
import re
import sys, getopt
import os
import random
from lxml import etree
import time
import locale
import webutils

HXGOOGLE_HOME = 'http://www.hxgoogle.com'
NUM_PER_PAGE = 10
totalRecord = sys.maxint
reqDelay = 0.0

pattern = re.compile(r'<span>约有([0-9,]+)项结果')
pattern2 = re.compile(r'抱歉，没有找到与“.*?”相关的网页')

def _updateTotalRecord(html):
    global totalRecord
    m = pattern2.search(html)
    if m != None:
	totalRecord = 0
        #print 'not found'
        return
    m = pattern.search(html)
    if m == None:
	return
    if len(m.groups()) <= 0:
    return
    totalRecord = int(m.group(1).replace(',', ''))
    print 'Total: ', totalRecord

    """
    结果xpath
    /html/body/table[2]/tbody/tr[2]/td[2]/ol/div/div[1]/div/h3

    /html/body/table[2]/tbody/tr[2]/td[2]/ol/div/div[2]/div/h3/a

    /html/body/table[2]/tbody/tr[2]/td[2]/ol/div/div[3]/div/h3/a
    """
def _hxPageHandler(opener, url):
    req = urllib2.Request(url)
    webutils.setupRequest(req)
    req.add_header('Referer', url[:-4])

    try:
	response = opener.open(req, timeout = REQ_TIMEOUT)
        html = response.read()
	#print html
    except Exception, e:
        print "Exception: url: %s - " % url, e
	raise StopIteration()
    if totalRecord == sys.maxint:
        _updateTotalRecord(html)


def _hxSearch(opener, what, resultNum = -1, startNum = 0):
    if resultNum == -1:
            pageCount = -1
    else:
            pageCount = int((resultNum + NUM_PER_PAGE - 1) / NUM_PER_PAGE)

    startPage = int((startNum + NUM_PER_PAGE - 1) / NUM_PER_PAGE)

    global totalRecord
    totalRecord = sys.maxint

    what = urllib2.quote(what)

    pageNum = 1
    resCnt = 0

    while True:
        if pageCount != -1:
            if pageNum > pageCount:
                break

        url = HXGOOGLE_HOME + '/search.jsp?q=%s&newwindow=1&safe=off&noj=1&hl=zh-CN&start=%d&sa=N' % 
            (what, (startPage + pageNum) * 10)

        for result in _hxPageHandler(opener, url):
            # i += 1
            resCnt += 1
            yield result
            if resultNum != -1 and resCnt >= resultNum:
                raise StopIteration()
            if resCnt >= totalRecord:
                raise StopIteration()

        if totalRecord == sys.maxint:
            if resultNum == -1:
                totalRecord = sys.maxint - 1
            else:
                totalRecord = resultNum

        if resCnt >= totalRecord:
            raise StopIteration()
        #if i < NUM_PER_PAGE: # FIXME: if the result total is 10... :(
        #   raise StopIteration()
        #   break
        pageNum += 1
        if reqDelay > 0:
            time.sleep(reqDelay)

