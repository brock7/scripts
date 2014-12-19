#!/usr/bin/python
# -*- coding: utf-8 -*-
# 0x150 Web Crawler v2.1

from PyQt4 import QtCore, QtGui
import socket
import urllib
import urllib2
import mechanize
import urlparse
from xml.dom.minidom import parse, parseString
from bs4 import BeautifulSoup
import base64
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(722, 364)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 10, 111, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.listView = QtGui.QListWidget(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 50, 301, 251))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.textEdit = QtGui.QLineEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 301, 31))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit.setPlaceholderText(_fromUtf8("Reverse Çek"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 50, 111, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        #self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        #self.pushButton_4.setGeometry(QtCore.QRect(320, 90, 111, 31))
        #self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.listView_2 = QtGui.QListWidget(self.centralwidget)
        self.listView_2.setGeometry(QtCore.QRect(440, 10, 271, 291))
        self.listView_2.setObjectName(_fromUtf8("listView_2"))
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(320, 90, 111, 31))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 270, 111, 31))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 722, 29))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuDosya = QtGui.QMenu(self.menubar)
        self.menuDosya.setObjectName(_fromUtf8("menuDosya"))

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionKaydet = QtGui.QAction(MainWindow)
        self.actionKaydet.setObjectName(_fromUtf8("actionKaydet"))
        self.actionKaydet.setShortcut('Ctrl+S')

        self.actionKaydet.triggered.connect(self.saveFile)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.triggered.connect(QtGui.qApp.quit)
        self.menuDosya.addAction(self.actionKaydet)
        self.menuDosya.addAction(self.actionExit)
        self.menubar.addAction(self.menuDosya.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),self.reverse)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),self.cekkeke)
       # QtCore.QObject.connect(self.pushButton_4,QtCore.SIGNAL("clicked()"),self.temizle)
        QtCore.QObject.connect(self.pushButton_5,QtCore.SIGNAL("clicked()"),self.temizle2)
        QtCore.QObject.connect(self.pushButton_3,QtCore.SIGNAL("clicked()"),self.saveFile)

    def temizle(self):
        self.listView_2.clear()
    def temizle2(self):
        self.listView.clear()
    def cekkeke(self):
        self.listView_2.clear()
        self.myopener = MyOpener()
    #page = urllib.urlopen(url)
        self.page = self.myopener.open("http://"+ str(self.listView.currentItem().text()))

        self.text = self.page.read()
        self.page.close()

        self.soup = BeautifulSoup(self.text)

        for self.tag in self.soup.findAll('a', href=True):
            self.xx = self.tag["href"]
            if  self.xx.startswith("http://") == False and self.xx.startswith("https://")==False:
                if self.xx.startswith("/")==True:
                    self.listView_2.addItem(self.listView.currentItem().text()+self.xx)
                else:
                    self.listView_2.addItem(self.listView.currentItem().text()+"/"+self.xx)
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "0x150 Web Crawler v2.1", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "< < Reverse IP", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "<< Crawler >>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "< < Kaydet >>", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDosya.setTitle(QtGui.QApplication.translate("MainWindow", "Dosya", None, QtGui.QApplication.UnicodeUTF8))
        #self.menuHakk_nda.setTitle(QtGui.QApplication.translate("MainWindow", "Hakkında", None, QtGui.QApplication.UnicodeUTF8))
        self.actionKaydet.setText(QtGui.QApplication.translate("MainWindow", "Kaydet", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        #self.pushButton_4.setText(QtGui.QApplication.translate("MainWindow", "Temizle >>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("MainWindow", "< < Temizle", None, QtGui.QApplication.UnicodeUTF8))
    def saveFile(self):
        self.filename = QtGui.QFileDialog.getSaveFileName(None, 'Save File',"/")
        self.f = open(self.filename, 'w')
        self.xe = open(self.textEdit.text()+"_reverse-ip.txt","w")
        items = []
        cocumuyo = []
        for index in xrange(self.listView_2.count()):
            items.append(self.listView_2.item(index))
        for i in items:
            #print i.text()
            self.f.write(i.text()+"\n")
        for ix in xrange(self.listView.count()):
            cocumuyo.append(self.listView.item(ix))
        for i in cocumuyo:
            self.xe.write(i.text()+"\n")
        self.xe.close()
        self.f.close()
        #print self.listView.currentItem().text()
    def reverse(self):
        self.listView.addItem(self.textEdit.text())
        self.sites = []
        self.top = 50
        self.skip = 0
        self.account_key ="6XgKqcpSQqUPnODbSdOK9sOy30ng0ilUci99d5pol8I"
        self.ipal = self.textEdit.text()
        self.ip = socket.gethostbyname(str(self.ipal))
        while self.skip < 200:
            self.url = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Web?Query='ip:%s'&$top=%s&$skip=%s&$format=Atom"%(self.ip,self.top,self.skip)
            self.request = urllib2.Request(self.url)
            self.auth = base64.encodestring("%s:%s" % (self.account_key, self.account_key)).replace("\n", "")
            self.request.add_header("Authorization", "Basic %s" % self.auth)
            self.res = urllib2.urlopen(self.request)
            self.data = self.res.read()
            self.xmldoc = parseString(self.data)
            self.site_list = self.xmldoc.getElementsByTagName('d:Url')
            for self.site in self.site_list:
                self.domain = self.site.childNodes[0].nodeValue
                self.domain = self.domain.split("/")[2]
                if self.domain not in self.sites:
                    self.sites.append(self.domain)
            self.skip += 50
        for self.xs in self.sites:
            self.listView.addItem(self.xs)
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())