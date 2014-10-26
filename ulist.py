#!/bin/env python
# -*- coding:utf-8 -*-

login_r = """
{"id":"MissMuse","user_name":"°„°È??","face_url":"http://images.newsmth.net/nForum/img/face_default_m.jpg","face_width":0,"face_height":0,"gender":"m","astro":"??°¡®Æ°¡®¥","life":"3®¢??","lifelevel":10,"qq":"","msn":"","home_page":"","level":"®Æ??°Ï","is_online":true,"post_count":6238,"last_login_time":1414972692,"last_login_ip":"116.225.114.139","is_hide":true,"is_activated":true,"is_register":true,"login_count":1174,"is_admin":false,"first_login_time":1126071802,"stay_count":16662167,"score_user":9702,"score_manager":0,"is_login":true,"forum_totol_count":18653,"forum_user_count":5539,"forum_guest_count":13114,"new_mail":false,"full_mail":false,"new_like":0,"new_reply":23,"new_at":0,"new_msg":0,"ajax_st":1,"ajax_code":"0005","ajax_msg":"2®¥°¡°¬3®¶1|"}
"""

content = """
<script type="text/javascript">if(!document.getElementById('body')){var redir = window.location.href.replace('/nForum/', '/nForum/#!');window.location.href = redir;}</script><style type="text/css">.friend-list,.mail-list{border-top:1px solid #c9d7f1}.title_1{width:20px;padding-left:12px}@media screen and (-webkit-min-device-pixel-ratio:0){.title_1{width:30px}}.title_2{width:100px;padding-left:12px}.title_3{width:auto;padding-left:12px;font-size:12px}.title_4{width:150px;padding-left:12px;color:#717171}.title_5{width:250px;padding-left:12px;color:#717171}.title_6{width:60px;padding-left:12px;color:#717171}.title_7{width:30px;padding-left:12px;color:#717171}.no-read a{color:#598ede;font-weight:bold}.middle{text-align:center padding-left:0}.t-btn{float:left;padding-left:12px}.t-btn input{margin-right:5px}.t-btn .mail-select{padding-top:0;padding-bottom:0}.page{float:right}.t-pre,.t-pre-bottom{padding:2px 0;width:100%;border-bottom:1px solid #c9d7f1;overflow:hidden}.mail-list .m-table tr:hover{cursor:pointer}.t-btn .friend-select{padding-top:0;padding-bottom:0}#friend_add{padding:4px 12px;border-bottom:1px solid #c9d7f1}#friend_add input{margin-left:5px}.t-pre-online .t-btn{margin-top:2px;*margin-top:6px;*padding-left:0}.t-pre-online .page{margin-top:0}</style>    	<div class="mbar"><ul><li><a href="/nForum/user/info">?®¥°¿?°¡®∫®¢?DT??</a></li><li><a href="/nForum/user/passwd">®∫?3??®π??DT??</a></li><li><a href="/nForum/user/custom">®Æ??°Ï°¡??°ß®∞?2?®∫y</a></li><li><a href="/nForum/msg">?®¨???°È</a></li><li><a href="/nForum/mail">®Æ??°ÏD??t</a></li><li><a href="/nForum/refer">????®¨®¢D?</a></li><li class="selected"><a href="/nForum/friend">o?®Æ?®¢D°¿®™</a></li><li><a href="/nForum/fav">®∫?2?°„???</a></li></ul></div><div class="c-mbar"><ul><li><a href="/nForum/friend"><samp class="ico-pos-dot"></samp>?®∞¶Ã?o?®Æ?</a></li><li><a href="/nForum/friend/online"><samp class="ico-pos-dot"></samp>?®≤??o?®Æ?</a></li><li><a href="/nForum/online" class="select"><samp class="ico-pos-dot"></samp>?®≤??®Æ??°Ï</a></li></ul></div><div class="b-content"><div class="mail-list"><div class="t-pre t-pre-online"><div class="t-btn"><li>???°„??®¨3®¶?°¡®π12®ÆD 19960 ®®??®≤??°Í????D°¡°È2®¢®Æ??°Ï 5986 ®®?°Í?°§??®™ 13974 ®®??°Í</li></div><div class="page"><ul class="pagination"><li class="page-pre">?®≤??®Æ??°Ï:<i>5986</i>&emsp;°§?®∞3:</li><li><ol title="°§?®∞3®¢D°¿®™" class="page-main"><li class="page-normal"><a href="/nForum/online?p=1" title="®¶?®∞?®∞3"><<</a></li><li class="page-normal"><a href="/nForum/online?p=1" title="°¡a¶Ã?¶Ã®≤1®∞3">1</a></li><li class="page-select"><a title="¶Ã°¿?°„®∞3">2</a></li><li class="page-normal"><a href="/nForum/online?p=3" title="°¡a¶Ã?¶Ã®≤3®∞3">3</a></li><li class="page-normal"><a href="/nForum/online?p=4" title="°¡a¶Ã?¶Ã®≤4®∞3">4</a></li><li class="page-normal"><a href="/nForum/online?p=5" title="°¡a¶Ã?¶Ã®≤5®∞3">5</a></li><li class="page-normal"><a href="/nForum/online?p=6" title="°¡a¶Ã?¶Ã®≤6®∞3">6</a></li><li class="page-normal"><a href="/nForum/online?p=7" title="°¡a¶Ã?¶Ã®≤7®∞3">7</a></li><li class="page-normal"><a href="/nForum/online?p=8" title="°¡a¶Ã?¶Ã®≤8®∞3">8</a></li><li class="page-omit">...</li><li class="page-normal"><a href="/nForum/online?p=300" title="°¡a¶Ã?¶Ã®≤300®∞3">300</a></li><li class="page-normal"><a href="/nForum/online?p=3" title="??®∞?®∞3">>></a></li></ol></li><li class="page-suf"></li></ul></div></div><table class="m-table"><tr class="title"><td class="title_7">D®∞o?</td><td class="title_2">ID</td><td class="title_3">°¡°‰®¨?</td><td class="title_5">¶Ã???IP</td><td class="title_6">°§°È°‰?</td><td class="title_6">2®¥°¡°¬</td><td class="title_6"></td></tr><tr><td class="title_7">1</td><td class="title_2"><a href="/nForum/user/query/ABARTH">ABARTH</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">117.136.0.*</td><td class="title_6">00:03</td><td class="title_6"><a href="/nForum/msg/ABARTH">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=ABARTH">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">2</td><td class="title_2"><a href="/nForum/user/query/ABARTH">ABARTH</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">117.136.0.*</td><td class="title_6">00:07</td><td class="title_6"><a href="/nForum/msg/ABARTH">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=ABARTH">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">3</td><td class="title_2"><a href="/nForum/user/query/abcaa">abcaa</a></td><td class="title_3">???®¢????</td><td class="title_5">114.252.48.*</td><td class="title_6">00:07</td><td class="title_6"><a href="/nForum/msg/abcaa">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abcaa">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">4</td><td class="title_2"><a href="/nForum/user/query/abcdd">abcdd</a></td><td class="title_3">???®¢????</td><td class="title_5">114.255.160.*</td><td class="title_6">00:00</td><td class="title_6"><a href="/nForum/msg/abcdd">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abcdd">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">5</td><td class="title_2"><a href="/nForum/user/query/abcdefg2010">abcdefg2010</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">61.49.56.*</td><td class="title_6">00:00</td><td class="title_6"><a href="/nForum/msg/abcdefg2010">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abcdefg2010">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">6</td><td class="title_2"><a href="/nForum/user/query/abchina2008">abchina2008</a></td><td class="title_3">???®¢????</td><td class="title_5">61.148.243.*</td><td class="title_6">00:02</td><td class="title_6"><a href="/nForum/msg/abchina2008">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abchina2008">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">7</td><td class="title_2"><a href="/nForum/user/query/ABDD">ABDD</a></td><td class="title_3">???®¢????</td><td class="title_5">113.200.79.*</td><td class="title_6">00:00</td><td class="title_6"><a href="/nForum/msg/ABDD">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=ABDD">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">8</td><td class="title_2"><a href="/nForum/user/query/abenxiang">abenxiang</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">122.233.242.*</td><td class="title_6">00:04</td><td class="title_6"><a href="/nForum/msg/abenxiang">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abenxiang">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">9</td><td class="title_2"><a href="/nForum/user/query/abenxiang">abenxiang</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">122.233.242.*</td><td class="title_6">00:09</td><td class="title_6"><a href="/nForum/msg/abenxiang">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abenxiang">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">10</td><td class="title_2"><a href="/nForum/user/query/abey">abey</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">176.61.12.*</td><td class="title_6">00:10</td><td class="title_6"><a href="/nForum/msg/abey">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abey">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">11</td><td class="title_2"><a href="/nForum/user/query/abigkitty">abigkitty</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">117.136.38.*</td><td class="title_6">00:00</td><td class="title_6"><a href="/nForum/msg/abigkitty">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abigkitty">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">12</td><td class="title_2"><a href="/nForum/user/query/ablg123">ablg123</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">114.248.126.*</td><td class="title_6">00:11</td><td class="title_6"><a href="/nForum/msg/ablg123">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=ablg123">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">13</td><td class="title_2"><a href="/nForum/user/query/About2Rain">About2Rain</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">222.128.169.*</td><td class="title_6">00:13</td><td class="title_6"><a href="/nForum/msg/About2Rain">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=About2Rain">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">14</td><td class="title_2"><a href="/nForum/user/query/aboveyusheng">aboveyusheng</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">211.140.4.*</td><td class="title_6">00:02</td><td class="title_6"><a href="/nForum/msg/aboveyusheng">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=aboveyusheng">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">15</td><td class="title_2"><a href="/nForum/user/query/aboydhg">aboydhg</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">114.255.3.*</td><td class="title_6">00:02</td><td class="title_6"><a href="/nForum/msg/aboydhg">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=aboydhg">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">16</td><td class="title_2"><a href="/nForum/user/query/abple">abple</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">211.136.233.*</td><td class="title_6">00:00</td><td class="title_6"><a href="/nForum/msg/abple">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abple">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">17</td><td class="title_2"><a href="/nForum/user/query/abu2009">abu2009</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">111.193.218.*</td><td class="title_6">00:10</td><td class="title_6"><a href="/nForum/msg/abu2009">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abu2009">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">18</td><td class="title_2"><a href="/nForum/user/query/abu2009">abu2009</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">111.193.218.*</td><td class="title_6">00:15</td><td class="title_6"><a href="/nForum/msg/abu2009">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abu2009">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">19</td><td class="title_2"><a href="/nForum/user/query/abutterfly">abutterfly</a></td><td class="title_3">Web?°•®§®§</td><td class="title_5">61.148.242.*</td><td class="title_6">00:05</td><td class="title_6"><a href="/nForum/msg/abutterfly">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=abutterfly">°§°ÈD??®∫o®∞</a></td></tr><tr><td class="title_7">20</td><td class="title_2"><a href="/nForum/user/query/acalism">acalism</a></td><td class="title_3">????®¨?????</td><td class="title_5">58.254.168.*</td><td class="title_6">00:01</td><td class="title_6"><a href="/nForum/msg/acalism">°§°È?®¨D??°È</a></td><td class="title_6"><a href="/nForum/mail/send?id=acalism">°§°ÈD??®∫o®∞</a></td></tr></table><div class="t-pre-bottom t-pre-online"><div class="t-btn">&nbsp;</div><div class="page"><ul class="pagination"><li class="page-pre">?®≤??®Æ??°Ï:<i>5986</i>&emsp;°§?®∞3:</li><li><ol title="°§?®∞3®¢D°¿®™" class="page-main"><li class="page-normal"><a href="/nForum/online?p=1" title="®¶?®∞?®∞3"><<</a></li><li class="page-normal"><a href="/nForum/online?p=1" title="°¡a¶Ã?¶Ã®≤1®∞3">1</a></li><li class="page-select"><a title="¶Ã°¿?°„®∞3">2</a></li><li class="page-normal"><a href="/nForum/online?p=3" title="°¡a¶Ã?¶Ã®≤3®∞3">3</a></li><li class="page-normal"><a href="/nForum/online?p=4" title="°¡a¶Ã?¶Ã®≤4®∞3">4</a></li><li class="page-normal"><a href="/nForum/online?p=5" title="°¡a¶Ã?¶Ã®≤5®∞3">5</a></li><li class="page-normal"><a href="/nForum/online?p=6" title="°¡a¶Ã?¶Ã®≤6®∞3">6</a></li><li class="page-normal"><a href="/nForum/online?p=7" title="°¡a¶Ã?¶Ã®≤7®∞3">7</a></li><li class="page-normal"><a href="/nForum/online?p=8" title="°¡a¶Ã?¶Ã®≤8®∞3">8</a></li><li class="page-omit">...</li><li class="page-normal"><a href="/nForum/online?p=300" title="°¡a¶Ã?¶Ã®≤300®∞3">300</a></li><li class="page-normal"><a href="/nForum/online?p=3" title="??®∞?®∞3">>></a></li></ol></li><li class="page-suf"></li></ul></div></div></div></div><script type="text/javascript">$('#notice_nav').html('<a href="/nForum/mainpage">????®¶???</a>&ensp;>>&ensp;<a href="/nForum/online">?®≤??®Æ??°Ï</a>');$.setTitle('????®¶???-?®≤??®Æ??°Ï');;</script>
"""

import urllib2
import re
import sys
import time

"""
if not re.findall('"id":"MissMuse1"', login_r.decode('gb2312')):
	print 'login failed'
	print login_r

sys.exit(0)
"""

udict = {}

def parseUserList(text):
	userPrefix = '<td class="title_2">'
	ipPrefix = '<td class="title_5">'
	ulist = re.findall(r'<td class="title_2"><a href="/nForum/user/query/(.+?)">.*?<td class="title_5">(.*?)</td><td class="title_6">', 
		text)
	if len(ulist) == 0:
		return False;
	
	for elem in ulist:
		ip = elem[1]
		if not udict.has_key(ip):
			udict[ip] = list()
		udict[ip].append(elem[0]);
		print ip, udict[ip]
	
	#for (k,v) in udict.items():
	#	print k,v
	return True
	
#parseUserList(content)
#sys.exit(0)

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
req = urllib2.Request('http://www.newsmth.net/nForum/user/ajax_login.json')
req.add_header('X-Requested-With', 'XMLHttpRequest')
req.add_header('Referer', 'http://www.newsmth.net/')
#req.add_header('Accept-Encoding', 'gzip, deflate')
data = 'id=missmuse&passwd=820312&mode=0&CookieDate=0'
response = opener.open(req, data)
html = response.read().decode('gb2312')
if not re.findall(r'"id":"MissMuse"', html) :
	print html
	print 'login failed'
	sys.exit(-1)

page = 1
while True:
	req = urllib2.Request('http://www.newsmth.net/nForum/online?ajax&p=%d' % page)
	req.add_header('X-Requested-With', 'XMLHttpRequest')
	req.add_header('Referer', 'http://www.newsmth.net/')
	try:
		response = opener.open(req, data)
		if not parseUserList(response.read().decode('gb2312')):
			break
	except:
		break
	page += 1;
	time.sleep(3)

print '*** summery: ***'
for (k,v) in udict.items():
	print k,v