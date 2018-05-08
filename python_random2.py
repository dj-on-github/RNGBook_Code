#!/usr/bin/env python

import random
r = random

for i in xrange(1,17):
    x = r.getrandbits(i)
    print "  bits: %2d random value: 0x%04x" % (i,x)
 
    
