import sys, os
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
sys.exit(0)
################################################################

from formatter import AbstractFormatter, NullWriter
from htmllib import HTMLParser
 
def _(str, in_encoder="gbk", out_encoder="utf8"):
    #return unicode(str, in_encoder).encode(out_encoder)
    return str


class myWriter(NullWriter):
    def __init__(self):
        NullWriter.__init__(self)
        self._bodyText = []

    def send_flowing_data(self, str):
        self._bodyText.append(str)

    def _get_bodyText(self):
        return '/n'.join(self._bodyText)

    bodyText = property(_get_bodyText, None, None, 'plain text from body')

class myHTMLParser(HTMLParser):
    def do_meta(self, attrs):
        self.metas = attrs

def convertFile(filename):
    mywriter = myWriter()
    absformatter = AbstractFormatter(mywriter)
    parser = myHTMLParser(absformatter)
    parser.feed(open(filename).read())
    return ( _(parser.title), parser.formatter.writer.bodyText )

import os
import os.path

#OUTPUTDIR = "./txt"
#INPUTDIR = "."
#if __name__ == "__main__":
#    if not os.path.exists(OUTPUTDIR):
#        os.mkdir(OUTPUTDIR)
#
#    for file in os.listdir(INPUTDIR):
#        if file[-4:] == '.htm':
#            print "Coverting", file,
#            outfilename, text = convertFile(file)
#            outfilename = outfilename + '.txt'
#            outfullname = os.path.join(OUTPUTDIR, outfilename)
#            open(outfullname, "wt").write(text)
#            print "Done!"
#
################################################################################
"""

#!/usr/bin/env python
# encoding:utf8
# author:zhouhh
# date:2012.11.20
from bs4 import BeautifulSoup
import os
import codecs
f="shedia.txt"
t=codecs.open(f,"wb",encoding="gb18030")
#t.write("\nzhh made for my dear yff \n2012.11.18\n")
ts=[]
 
t.write("\nzhh made for my dear yff \n2012.11.18\n\n")
for i in sorted(os.listdir(".")):
    if(i[-3:]=="htm"):
        print "convert %s title "%i
        htm=codecs.open(i,"rb",encoding="gb18030")
    soup=BeautifulSoup(htm)
        htm.close()
    #f="%stxt"%i[:-3]
    #print "write to %s"%f
        #t.write(soup.select("p")[0].text)
    title=soup.title.text[7:]
    ts.append(title)
t.write("\n".join(ts))
 
for i in sorted(os.listdir(".")):
    if(i[-3:]=="htm"):
        print "convert %s"%i
        htm=codecs.open(i,"rb",encoding="gb18030")
    soup=BeautifulSoup(htm)
        htm.close()
    #f="%stxt"%i[:-3]
    #print "write to %s"%f
        #t.write(soup.select("p")[0].text)
    t.write("\nzhh made for my dear yff \n2012.11.18\n\n")
    title=soup.title.text[7:]
 
        t.write(title)
    t.write(soup.select("pre")[0].text)
    #t.write(soup.body.text)
t.close()
"""

