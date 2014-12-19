#!/usr/bin/env python
#
# File_name: md5 hash cracker
# Writin by: lnxg33k <ahmed[at]isecur1ty.org>
# Currently contains about 13 site for cracking
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import time
import urllib2
import urllib 
import re
import hashlib

if len(sys.argv) < 2:
  print '\nUsage:'
  print '\t%s --online [hash..] ' % sys.argv[0]
  print '\t%s --offline [hash..] [dictionary..]'  % sys.argv[0]
  sys.exit(1)

def banner():
  print '''
                  ___           ___           ___           ___           ___     
    ___          /  /\         /  /\         /  /\         /  /\         /__/|    
   /  /\        /  /:/        /  /::\       /  /::\       /  /:/        |  |:|    
  /  /:/       /  /:/        /  /:/\:\     /  /:/\:\     /  /:/         |  |:|    
 /__/::\      /  /:/  ___   /  /:/~/:/    /  /:/~/::\   /  /:/  ___   __|  |:|    
 \__\/\:\__  /__/:/  /  /\ /__/:/ /:/___ /__/:/ /:/\:\ /__/:/  /  /\ /__/\_|:|____
    \  \:\/\ \  \:\ /  /:/ \  \:\/:::::/ \  \:\/:/__\/ \  \:\ /  /:/ \  \:\/:::::/
     \__\::/  \  \:\  /:/   \  \::/~~~~   \  \::/       \  \:\  /:/   \  \::/~~~~ 
     /__/:/    \  \:\/:/     \  \:\        \  \:\        \  \:\/:/     \  \:\     
     \__\/      \  \::/       \  \:\        \  \:\        \  \::/       \  \:\    
                 \__\/         \__\/         \__\/         \__\/         \__\/
  
        |-----------------------------------------------|
        | [+] MD5 Hash Cracker (online | offline)       |
        | [+] Home: http://www.isecur1ty.org            |
        | [+] Written by: isecur1ty team members        |
        | [+] Credits: Obzy, Relik and Sas-TerrOrisT    |
        |-----------------------------------------------|
'''

option   = sys.argv[1]
passwd   = sys.argv[2]

if option == '--online':
  if len(passwd) != 32: 
    print '\n[*] Error: "%s" doesn\'t seem to be a valid MD5 hash "32 bit hexadecimal"' % passwd
  else:
    try:
      banner()
      def myaddr():
        site = 'http://md5.my-addr.com/'
        rest = 'md5_decrypt-md5_cracker_online/md5_decoder_tool.php'
        para = urllib.urlencode({'md5':passwd})
        req  = urllib2.Request(site+rest)
        try:
          fd   = urllib2.urlopen(req, para)
          data = fd.read()
          match= re.search('(Hashed string</span>: )(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError:  print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      myaddr()

      def victorov():
        try:
          site = 'http://www.victorov.su/'
          para = 'md5/?md5e=&md5d=%s' % passwd
          req  = urllib2.Request(site+para)
          req.add_header
          opener = urllib2.urlopen(req)
          data = opener.read()
          match = re.search('(<b>)(.+[^>])(</b>)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError:  print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      victorov()
      
      def md5crack():
        site = 'http://www.md5crack.com/'
        rest = 'crackmd5.php'
        para = urllib.urlencode({'term':passwd})
        req = urllib2.Request(site+rest)
        try: 
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search('(Found: md5)(..)(\w+.\w+)', data)
          if match: print '[=] site: %s\t\t\tPassword: %s' % (site, match.group(3))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error seems to be down' % site
      md5crack()
      
      def passcracking():
        site = 'http://passcracking.com/'
        rest = 'index.php'
        para = urllib.urlencode({'datafromuser':passwd})
        req = urllib2.Request(site+rest)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search(r"(<td bgcolor=#FF0000>)(.+[^<])(</td><td>)", data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      passcracking()

      def rednoize():
        site = 'http://md5.rednoize.com/'
        para = 'p&s=md5&q=%s&_=' % passwd
        try:
          req = urllib2.urlopen(site+'?'+para)
          data = req.read()
          if not len(data): print '[-] site: %s\t\t\tPassword: Not found' %site
          else: print '[-] site: %s\t\t\tPassword: %s' % (site, data)
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      rednoize()

      def md5pass():
        site = 'http://www.md5pass.info/'
        para = urllib.urlencode({'hash':passwd, 'get_pass':'Get+Pass'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search('(Password - <b>)(\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      md5pass()

      def md5decryption():
        site = 'http://md5decryption.com/'
        para = urllib.urlencode({'hash':passwd,'submit':'Decrypt+It!'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search(r'(Decrypted Text: </b>)(.+[^>])(</font><br/><center>)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      md5decryption()

      def hashkiller():
        site = 'http://opencrack.hashkiller.com/'
        para = urllib.urlencode({'oc_check_md5':passwd,'oc_submit':'Search+MD5'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search('(<div class="result">)(\w+)(:)(\w+.\w+)', data)
          if match:
            print '[-] site: %s\t\t\tPassword: %s' % (site.replace('http://', ''), match.group(4).replace('<br',''))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site.replace('http://', '')
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      hashkiller()

      def bigtrapeze():
        site = 'http://www.bigtrapeze.com/'
        rest = 'md5/index.php?query=%s' % passwd
        req = urllib2.Request(site+rest)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.2)\
        Gecko/20100316 AskTbSPC2/3.9.1.14019 Firefox/3.6.2')
        try:
          opener = urllib2.build_opener()
          data = opener.open(req).read()
          match = re.search('(=> <strong>)(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      bigtrapeze()

      def cloudcracker():
        site = 'http://www.netmd5crack.com/'
        para = 'cgi-bin/Crack.py?InputHash=%s' % passwd
        try:
          req = urllib.urlopen(site+para)
          data = req.read()
          match = re.search(r'<tr><td class="border">[^<]+</td><td class="border">\
          (?P<hash>[^>]+)</td></tr></tbody></table>', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(hash))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      cloudcracker()

      def hashchecker():
        site = 'http://www.hashchecker.com/'
        para = urllib.urlencode({'search_field':passwd, 'Submit':'search'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search('(is <b>)(\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      hashchecker()  

      def hashcracking():
        site = 'http://md5.hashcracking.com/'
        rest = 'search.php'
        para = 'md5=%s' % passwd
        try:
          req = urllib2.urlopen(site+rest+'?'+para)
          data = req.read()
          match = re.search('(is)(.)(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(3))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      hashcracking()

      def cloudcracker():
        site = 'http://www.cloudcracker.net/'
        para = urllib.urlencode({'inputbox':passwd, 'submit':'Crack+MD5+Hash!'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search('(this.select)(....)(\w+=")(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s\n' % (site, match.group(4))
          else: print '[-] site: %s\t\t\tPassword: Not found\n' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      cloudcracker()
    except KeyboardInterrupt: print '\nTerminated by user ...'
    
elif option == '--offline':
  banner()
  try:
    def offline():
      print '[+] This opertaion will take some time, be patient ...' 
      dictionary = sys.argv[3]
      dic = {}
      shooter = 0
      try:
        f = open(dictionary, 'rb')
        start = time.time()
        for line in f:
          line = line.rstrip()
          dic[line] = hashlib.md5(line).hexdigest()
        for k in dic.keys(): 
          if passwd in dic[k]:
            stop = time.time()
            global spent
            spent = stop - start
            print '\n[-] Hash: %s\t\tData: %s\t\tTime: %.f seconds' % (dic[k], k, spent)
            shooter += 1
        if shooter == 0:  print "\n[*]Password not found in [%s] try the online cracker\n" % dictionary
        f.close()
      except IOError: print '\n[*] Erorr: %s doesn\'t exsit \n' % dictionary
    offline()
  except KeyboardInterrupt: print '\nTerminated by user ...'
  
else: pass 
