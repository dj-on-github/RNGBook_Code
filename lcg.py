#!/usr/bin/env python

def lcg(a,c,m,seed):
    x = seed
    while True:
        x = (x*a + c) % m
        yield (x >> 16) & 0xffffffff
        
lcginst = lcg(a=0x5deece66d,c=11,m=2**48,seed=0x3a6f9eb64)
for i in xrange(10):
    print "0x%08x" % lcginst.next()

