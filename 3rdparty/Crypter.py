from Crypto.Hash import HMAC       
from Crypto.Hash import MD2
from Crypto.Hash import MD4
from Crypto.Hash import MD5
from Crypto.Hash import RIPEMD
from Crypto.Hash import SHA
from Crypto.Hash import SHA256


                                                                            
                                                  ########			  	 
                                                  #B3mB4m#
                                                  ########

 
#Hi guyss im B3mB4m to day topic how to use PyCrypto - The Python Cryptography Toolkit ? !!

# You can see codes here, but ý want change somethins

word = raw_input("Give me the word : ")


"""

from Crypto.Hash import HMAC       
from Crypto.Hash import MD2
from Crypto.Hash import MD4
from Crypto.Hash import MD5
from Crypto.Hash import RIPEMD
from Crypto.Hash import SHA
from Crypto.Hash import SHA256

HMAC-MD2-MD4-MD5-SHA-SHA526-RIPEMD  .. now lets try 


"""


secret = b'B3mB4m'           
h = HMAC.new(secret)            
h.update(word)         
print "HMAC = "+h.hexdigest()

h2 = MD2.new()                      
h2.update(word)                            
print "MD2 = "+h2.hexdigest()

h3 = MD4.new()
h3.update(word)
print "MD4 = "+h3.hexdigest()
                                       
h4 = MD5.new()                          
h4.update(word)
print "MD5 = "+h3.hexdigest()

h5 = RIPEMD.new()                           
h5.update(word)                     
print "RIPEMD = "+h5.hexdigest()        
                                                          
h6 = SHA.new()
h6.update(word)
print "SHA = "+h6.hexdigest()

h7 = SHA.new()
h7.update(word )
print "SHA256 = "+h7.hexdigest()
