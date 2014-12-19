#
# Coded By Ajith Kp
# (c) Ajith Kp (c)
#
# input URL/IP
# Project Home Page: http://www.TerminalCoders.BlogSpot.iN
#
# ajithkp560[at]gmail.com
# 0x0x0x
#
from Tkinter import *
import Tix as tk
import urllib2, sys, re
from socket import gethostbyname
source='http://www.ip-adress.com/reverse_ip/'
uagent= {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)'}

class GUI:
    def __init__(self,v):
        self.entry = Entry(v, width=65, bg='#002B36', fg='#93A1A1', )
        self.entry.pack()
        self.button=Button(v, text=">>>",command=self.pressButton, bg="black", fg="green")
        self.button.pack()
        self.t = StringVar()
        self.t.set(":.: Reverse IP Lookup Tool :.:")
        self.label=Label(v, textvariable=self.t, font='Helvetica -14 bold')
        self.label.pack()
        self.n = 0
    def pressButton(self):
        site = self.entry.get()
        try:
            ip=gethostbyname(site)
            self.label=Label(w, text="\n\nScanning %s:[%s]\n\n"%(site, ip), font='Helvetica -12 bold', fg="#002B36")
            self.label.pack()
            request=urllib2.Request('%s%s'%(source, site), headers=uagent)
            page=urllib2.urlopen(request).read()
            findout=re.findall("href=\"/whois/\S+\">Whois</a>]", page)
            listbox = Listbox(w, fg="GREEN", bg="BLACK", width=10, height=20)
            listbox.pack()
            for revz in findout:
                revipz=revz.replace('href=\"/whois/', '').replace('\">Whois</a>]', '')
                listbox.insert(END, revipz)
            listbox.pack(fill=BOTH)
        except BaseException, e:
            self.label=Label(w, text="Error: %s"%(e), font='Helvetica -13 bold', fg="red", bg="black")
            self.label.pack()
w=Tk()
w.title("Reverse IP Lookup By Ajith Kp")
w.minsize(300,400)
gui=GUI(w)
w.mainloop()
