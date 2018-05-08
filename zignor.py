#!/usr/bin/env python

import sys
import random
import math

rand = random.SystemRandom() # nondeterministic random source
num = int(sys.argv[1])  # Number of random numbers

zignor_c = 128
zignor_r = 3.442619855899
zignor_v = 9.91256303526217e-3

adzig_x = [0.0 for x in range(zignor_c+1)]
adzig_r = [0.0 for x in range(zignor_c)]

def tail_computation(dmin,isnegative):
    while True:
        x = math.log(rand.random())/dmin
        y = math.log(rand.random())
        if ((-2*y) < x**2):
            break
    if isnegative:
        return x-dmin
    else:
        return dmin-x

def zignorinit(ic, dr, dv):
    f = math.exp(-0.5 * dr*dr)
    adzig_x[0] = dv/f
    adzig_x[1] = dr
    adzig_x[ic] = 0

    for i in xrange(2,ic):
        adzig_x[i] = math.sqrt(-2.0 * math.log(dv/adzig_x[i-1] +f))
        f = math.exp(-0.5 * (adzig_x[i]**2))
    for i in xrange(ic):
        adzig_r[i] = adzig_x[i+1]/adzig_x[i]

def zignor():
    while True:
        u = 2.0 * rand.random() -1
        i=rand.getrandbits(32) & 0x7f

        # Top boxes
        if abs(u) < adzig_r[i]:
            return u *adzig_x[i]
        # Lowest box
        isnegative =  (u < 0)
        if i==0:
            return tail_computation(zignor_r,isnegative)
        
        x = u * adzig_x[i]
        
        f0 = math.exp(-0.5 * (adzig_x[i] * adzig_x[i] - (x**2)))
        f1 = math.exp(-0.5 * (adzig_x[i+1] * adzig_x[i+1] - (x**2)))

        if (f1 + rand.random() * (f0 - f1)) < 1.0 :
            return x

zignorinit(zignor_c,zignor_r,zignor_v)

for i in xrange(num):
    print zignor()

