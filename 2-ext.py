#!/usr/bin/env python

import sys
import random
import math
from mpmath import *

if len(sys.argv) < 2:
    print "Usage: program min_entropy_per_bit size_of_matrix_side"
    exit()

per_bit_min_entropy = float(sys.argv[1])     # Input entropy
l = int(sys.argv[2])

bx = l * per_bit_min_entropy
by = bx

mp.dps = 100

def blender_bias_from_k(bx, by, l, k):
    expo = mpf(-(bx+by+2-l-k))/2
    bias = mpf('2.0') ** expo
    return bias

def blender_k_from_bias(bx,by,l,bias):
    k = (bx+by+2-l-(mpf('2.0')*log(mpf('1.0')/bias,mpf('2.0'))))
    return k

def ext_k_from_bias(bx,by,l,bias):
    k = max(bx,by)+(bx+by+2-l-(mpf('2.0')*log(mpf('1.0')/bias,mpf('2.0'))))
    return k
    
#print "k,logbias"

for k in xrange(1,257):
    bias = blender_bias_from_k(bx,by,l,k)
    logbias = log(bias,mpf('2.0'))
    print k," ",nstr(logbias,6)


