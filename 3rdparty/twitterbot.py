#!/usr/bin/env python
# -*- coding: cp1254 -*-

import mechanize 
import time

print """

Coded by B3mB4m

Twitter BOT V 0.1 !

b3mb4m@gmail.com

"""

url = "https://mobile.twitter.com/session/new"

op = mechanize.Browser() #Mechanizeyi tan�mla
op.set_handle_robots(False)#Baz� sayfalar programlar� engeller robot False yap�yoruz.
op.addheaders = [('Referer', 'http://google.com')]#Header ekliyoruz.
#Google'dan �ektim siz user agent olarak ekleyedebilirisiniz.
#Header istege bagl� degi�tirilebilir.


op.open(url) # Siteyi a�t�r



gmail = raw_input("Email: ")
passwd = raw_input("Password: ")

op.select_form(nr=0)
op.form["username"] = gmail
op.form["password"] = passwd
print ""

op.submit()

if op.title() != "Twitter":
    print "."
    sys.exit()
else:
    print ""
    print "Twitter Login Success !"
    print ""


text = raw_input("Message:  ")
a = 0
while True:
    a += 1
    tweet = 'https://mobile.twitter.com/compose/tweet'
    op.open(tweet)
    op.select_form(nr=0)
    op.form['tweet[text]'] = text + str(a)
    #str(a) yapmam�z�n sebebi print se�enegini kullanm�yoruz dikkat ederseniz.
    #Formlar �zerinde i�lem yapt�g�m�zdan str(a) yap�p program�n akl�n� kar��t�rmam�z gerek.
    op.submit()
    time.sleep(1)
    #time.sleep i�indeki saniye aral�g�d�r, istege bagl� degi�ebilir.
    print "Twit Done !"




























