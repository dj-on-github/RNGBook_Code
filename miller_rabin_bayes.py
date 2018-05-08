#!/usr/bin/python

import math

pxbar = 1.0/710.0
px = 709.0/710.0

    
for k in xrange(100,140):
    pygx = 2.0 ** (-2*k)
    pygxbar = 1.0-(2.0 ** (-2*k))
    
    top = pygx * px
    bottom = top + (pygxbar * pxbar)

    error_prob = top/bottom
    error_bits = math.log(error_prob,2)

    print "k=%d, error_prob = 1 in 2^%f" % (k,error_bits)

 
  