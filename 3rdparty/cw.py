import urlparse            
import mechanize
import urllib2
import random

useragent = ['Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2pre) Gecko/20100207 Ubuntu/9.04 (jaunty) Namoroka/3.6.2pre',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
            'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)',
            'Microsoft Internet Explorer/4.0b1 (Windows 95)',
            'Opera/8.00 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
            'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
            'Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.11 [en]']
agents = random.choice(useragent)
url = raw_input("\n\tTarget : ")
print ""
def crawler():
    
        tarayici = mechanize.Browser()
        tarayici.set_handle_robots(False)
        tarayici.addheaders = [('User-agent', agents)]

        urls = [url]
        gez = [url]

        try: 
            while len(urls)>0:
                try:             
                    tarayici.open(urls[0])
                    urls.pop(0)
                    try:
                        for link in tarayici.links():
                            yeniurl =  urlparse.urljoin(link.base_url,link.url)
                            if yeniurl not in gez and url in yeniurl:
                                gez.append(yeniurl)
                                urls.append(yeniurl)

                                if "=" in yeniurl:
                                    print yeniurl
                    except:
                        break                     
                except:
                    urls.pop(0)
        except:
            pass   
crawler()
