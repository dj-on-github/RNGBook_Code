import os
from struct import *
          
def rand16(bits):
    a = os.urandom(2)
    therand16 = unpack('H',a)[0]
    if therand16 < 0:
        therand16 += 0x8000
    mask = (2**bits)-1
    therand16 = therand16 & mask    
    return therand16
    
        
        