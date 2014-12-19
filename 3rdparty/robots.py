import urllib2
def robot():
    
    url = ["/robots.txt", "/readme.html", "/wp-config.php", "/wp-config.bak", "/wp-config.phpBak",
           "/wp-config.phpBak", "/wp-config.save", "/wp-config.back", "/wp-config.old", "/wp-config.html", "/wp-config.txt"]
    for i in url:
        urls = i
        n = urllib2.urlopen(site+i)
        
        if n.code ==200:
            
            print "[+]Found -->"+site+i
        else:
            pass
   
 
robot()
    
 
 

 
