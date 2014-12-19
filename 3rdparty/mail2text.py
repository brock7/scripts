#!/usr/bin/python
#darkc0de.com email checker >> text message

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import urllib2, urllib, time, poplib

#------------PHONE SETUP----------------------
#Sent from 
EMAIL = "hello@hello.com"
#Phone Number (keep this format)
NUMBER = "123-456-7890"	

#------------MAIL SETUP-----------------------
#Username (full address)
USER = "user@darkc0de.com"
#Password
PASSWORD = "123456"
#Inverval to check in seconds
TIME = "1800"
#---------------------------------------------

def getmail():
	FROM = ""
	SUBJECT = ""
	try:
		M = poplib.POP3('mail.darkc0de.com')
		M.user(USER)
		M.pass_(PASSWORD)
		c = M.stat()[0]
		numMessages = len(M.list()[1])
		for i in range(numMessages):
    			SUBJECT = M.retr(i+1)[1][15]
    			FROM = M.retr(i+1)[1][16]
	except (poplib.error_proto), msg:
		c = -1
		print "Mail Failed:",msg
		pass
	return int(c), FROM, SUBJECT

def sendtxt(FROM, SUBJECT):
	host = "http://www.txtdrop.com/"
	login_form_seq = [
     		('emailfrom',EMAIL),
		('npa',NUMBER[0]),
		('exchange',NUMBER[1]),
		('number',NUMBER[2]),
		('body',FROM+" "+SUBJECT),
		('submitted','1'),
		('submit','Send')]
	login_form_data = urllib.urlencode(login_form_seq)
	opener = urllib2.build_opener()
	try:
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		opener.open(host, login_form_data)
	except(urllib2.URLError), msg:
		print "Phone Failed:",msg
		pass
	print "\n[+] Message Sent\n"

NUMBER = NUMBER.split("-",2)
c, FROM, SUBJECT = getmail()
print "Start:",str(c),"emails"
while 1:
	time.sleep(int(TIME))
	new_c, FROM, SUBJECT = getmail()
	if new_c != -1:
		if new_c > c:
			sendtxt(FROM, SUBJECT)
		if new_c < c:
			c = new_c
		 
	


