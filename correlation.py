#!/usr/bin/env python

import math
import random

print "Correlation Coeff,  Pearson Phi,  (2*P(x[i]=x[y]))-1,  X mean,  Y mean"
for round in range(10):
    n = 10000

    # Make two lists of n random bits

    x = list()
    y = list()

    k1 = random.getrandbits(n)
    k2 = random.getrandbits(n)
    for i in range(n):
        x.append(int(k1 & 0x1))
        y.append(int(k2 & 0x1))
        k1 = k1 >> 1
        k2 = k2 >> 1

    #insert bias
    for i in range(n):
        if (x[i] == 1) and (random.randint(0,100) > 60):
            x[i] = 0
        if (y[i] == 1) and (random.randint(0,100) > 60):
            y[i] = 0

    # insert correlation
        if (x[i] != y[i]) and (random.randint(0,100) > 90):
            if random.choice((True,False)):
                x[i] = y[i]
            else:
                y[i] = x[i]

    ## center the data
    #for i in range(n):
    #    if x[i] == 0:
    #        x[i] = -1
    #    if y[i] == 0:
    #        y[i] = -1

    # Compute the serial correlation

    sumxiyi = 0
    sumxi = 0
    sumyi = 0
    sumxi2 = 0
    sumyi2 = 0

    for i in range(n):
        sumxiyi += x[i]*y[i]
        sumxi   += x[i]
        sumyi   += y[i]
        sumxi2  += x[i]*x[i]
        sumyi2  += y[i]*y[i]

    top = (n*sumxiyi) - (sumxi*sumyi)
    bottom = (n*sumxi2 - (sumxi*sumxi))*((n*sumyi2)- (sumyi*sumyi))
    c_cc = float(top)/math.sqrt(float(bottom))

    # Pearsons Phi
    n11 = 0
    n10 = 0
    n01 = 0
    n00 = 0
    y1 = 0
    y0 = 0
    x1 = 0
    x0 = 0

    for i in range(n):
        if x[i] == 1 and y[i] == 1:
            n11 += 1
        if x[i] == 1 and y[i] != 1:
            n10 += 1
        if x[i] != 1 and y[i] == 1:
            n01 += 1
        if x[i] != 1 and y[i] != 1:
            n00 += 1
       
        if y[i] == 1:
            y1 += 1
        if y[i] != 1:
            y0 += 1
        if x[i] == 1:
            x1 += 1
        if x[i] != 1:
            x0 += 1

    top = n11 * n00 - n10*n01
    bottom = math.sqrt(float(y1*y0*x1*x0))
    c_pp = float(top)/bottom

    # compute the means
    x_mean = float(x1)/float(n)
    y_mean = float(y1)/float(n)
    # Do it the other way
    aeqb = 0
    for i in range(n):
        if x[i] == y[i]:
            aeqb += 1
    prob = float(aeqb)/float(n)
    c_aeqb = (prob*2.0) - 1.0

    print "%1.6f            %1.6f      %1.6f             %1.6f %1.6f" % (c_cc,c_pp,c_aeqb, x_mean, y_mean)

