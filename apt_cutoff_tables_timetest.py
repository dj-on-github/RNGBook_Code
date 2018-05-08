#!/usr/bin/env python

import math 
from mpmath import *
import matplotlib
import matplotlib.pyplot as plt
import time
from beta_functions import *

PRECISION = 300
mp.dps = PRECISION

wss = [64,256,512,1024,2048,4096,65536]     # Window Sizes
                                # H Values
hs = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]+range(1,21)
for i in xrange(len(hs)): # convert to high precision floats
    hs[i] = mpf(hs[i])

Ws = [32,48,53,64,96,128] # False positive error rate exponents

t1 = time.clock()
for wx in Ws:
    W = mpf('2.0')**-wx
    match = True
    print("  W = 2^-{}".format(wx))
    print("  H{0:5}  {1:5} {2:5}  {3:5} {4:5} {5:5}  {6:5}".format(wss[0],wss[1],wss[2],wss[3],wss[4],wss[5],wss[6]))
    print
    for h in hs: 
        cs = list()
        
        for ws in wss:
            cs.append(str(binomial_quantile(ws,mpf('2.0')**(-h),mpf('1.0')-W)))
        print("{0:5.1f} {1:5} {2:5} {3:5} {4:5} {5:5} {6:5} {7:5}".format(float(h),cs[0],cs[1],cs[2],cs[3],cs[4],cs[5], cs[6]))
    print

t2 = time.clock()
for wx in Ws:
    W = mpf('2.0')**-wx
    match = True
    print("  W = 2^-{}".format(wx))
    print("  H{0:5}  {1:5} {2:5}  {3:5} {4:5} {5:5}  {6:5}".format(wss[0],wss[1],wss[2],wss[3],wss[4],wss[5],wss[6]))
    print
    for h in hs: 
        cs_b = list()
        
        for ws in wss:
            cs_b.append(str(binomial_quantile_backwards(ws,mpf('2.0')**(-h),mpf('1.0')-W)))
        print("{0:5.1f} {1:5} {2:5} {3:5} {4:5} {5:5} {6:5} {7:5}".format(float(h),cs_b[0],cs_b[1],cs_b[2],cs_b[3],cs_b[4],cs_b[5], cs_b[6]))
    print

t3 = time.clock()
    
for wx in Ws:
    W = mpf('2.0')**-wx
    match = True
    print("  W = 2^-{}".format(wx))
    print("  H{0:5}  {1:5} {2:5}  {3:5} {4:5} {5:5}  {6:5}".format(wss[0],wss[1],wss[2],wss[3],wss[4],wss[5],wss[6]))
    print
    for h in hs: 
        cs_b2 = list()
        
        for ws in wss:
            cs_b2.append(str(binomial_quantile_backwards2(ws,mpf('2.0')**(-h),mpf('1.0')-W)))
        print("{0:5.1f} {1:5} {2:5} {3:5} {4:5} {5:5} {6:5} {7:5}".format(float(h),cs_b2[0],cs_b2[1],cs_b2[2],cs_b2[3],cs_b2[4],cs_b2[5], cs_b2[6]))
    print
t4 = time.clock()  

recursive_time = t2-t1
backwards_time = t3-t2
backwards2_time = t4-t3

print("Time for each algortithm variant")
print("Recursive:",recursive_time)
print("Backwards:",backwards_time)
print("Backwards2:",backwards2_time)
    
