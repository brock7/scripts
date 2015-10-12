# -*- encoding: utf-8 -*-

import urllib2
import sys
import os
import webutils

class SearchBase:
    
    _opener = None
    _totalRecord = sys.maxint
    
    reqTimeout = 20

    def __init__(self, opener):
	self._opener = opener

    # TODO: get total record number from page
    def _updateTotalRecord(self, html):
        pass

    # TODO: pick up links from page
    def _pickupLinks(self, html):
        pass

    def _pageHandler(self, url):
        # print 'page handler'
        req = urllib2.Request(url)
        webutils.setupRequest(req)
        req.add_header('Referer', url[:-4])

        try:
            response = self._opener.open(req, timeout = self.reqTimeout)
            html = response.read()
            # print html
        except Exception, e:
            print "Exception: url: %s - " % url, e
            raise StopIteration()

        if self._totalRecord == sys.maxint:
            self._updateTotalRecord(html)

        for url in self._pickupLinks(html):
            yield url

    # TODO: return number of results per page. default is 10
    def _getNumPerPage(self):
        return 10

    # TODO: generate a url for searching
    def _genUrl(self, what, start):
        return ''

    def search(self, what, resultNum = -1, startNum = 0):

        numPerPage = self._getNumPerPage();

        if resultNum == -1:
            pageCount = -1
        else:
            pageCount = int((resultNum + numPerPage - 1) / numPerPage)
                                                                              
        startPage = int((startNum + numPerPage - 1) / numPerPage)         

        self._totalRecord = sys.maxint

        what = urllib2.quote(what)

        pageNum = 1
        resCnt = 0

        while True:
            if pageCount != -1:
                if pageNum > pageCount:
                    break

            url = self._genUrl(what, (startPage + pageNum - 1) * numPerPage)
            # print url
            
            for result in self._pageHandler(url):
                resCnt += 1
                yield result
                if resultNum != -1 and resCnt >= resultNum:
                    raise StopIteration()
                if resCnt >= self._totalRecord:
                    raise StopIteration()

            if self._totalRecord == sys.maxint:
                if resultNum == -1:
                    self._totalRecord = sys.maxint - 1
                else:
                    self._totalRecord = resultNum

            if resCnt >= self._totalRecord:
                raise StopIteration()
            #if i < numPerPage: # FIXME: if the result total is 10... :(
            #   raise StopIteration()
            #   break
            pageNum += 1

