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

op = mechanize.Browser() #Mechanizeyi tanımla
op.set_handle_robots(False)#Bazı sayfalar programları engeller robot False yapıyoruz.
op.addheaders = [('Referer', 'http://google.com')]#Header ekliyoruz.
#Google'dan çektim siz user agent olarak ekleyedebilirisiniz.
#Header istege baglı degiştirilebilir.


op.open(url) # Siteyi açtır



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
    #str(a) yapmamızın sebebi print seçenegini kullanmıyoruz dikkat ederseniz.
    #Formlar üzerinde işlem yaptıgımızdan str(a) yapıp programın aklını karıştırmamız gerek.
    op.submit()
    time.sleep(1)
    #time.sleep içindeki saniye aralıgıdır, istege baglı degişebilir.
    print "Twit Done !"




























