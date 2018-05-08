#!/usr/bin/env python

import math
import sys
import random

previous = [0,]

def scc256(bitlist):
    global previous
    bitlist257 = previous + bitlist
    previous = bitlist[255:]
    count1 = 0
    counts = [0,0,0,0]
    for i in xrange(256):
        if bitlist[i] == 1:
            count1 += 1

        if bitlist257[i:i+2] == [0,0]:
            counts[0] += 1
        if bitlist257[i:i+2] == [1,0]:
            counts[1] += 1
        if bitlist257[i:i+2] == [0,1]:
            counts[2] += 1
        if bitlist257[i:i+2] == [1,1]:
            counts[3] += 1  
    return (count1,counts)

def compute_mean_scc(count1,counts):
    n = 256
    top = (n*counts[3]) - ((counts[2] + counts[3])*(counts[2] + counts[3]))
    bottom = (n*(counts[2] + counts[3])) - ((counts[2] + counts[3])*(counts[2] + counts[3]))
    if (bottom > 0):
        scc = float(top)/float(bottom)
    else:
        scc = 1.0
    mean = float(count1)/256.0
    return (mean,scc)

    
def gen_scc_data(scc):
    prev = 0
    for i in range(256):
        bits = list()
        for j in range(256):
            paeqb = (scc+1.0)/2.0
            if prev == 1:
                p1 = paeqb
            else:
                p1 = 1-paeqb
            uniformrand = random.random()
            if uniformrand < p1:
                bit = 1
            else:
                bit = 0
            bits.append(bit)
            prev = bit
        yield bits

print "scc, measured_scc"

for sccint in range(41):
    scc = -1.0 + (sccint * 0.05)
    for bitlist in gen_scc_data(scc):
        (count1,counts) = scc256(bitlist)
        (mean,measured_scc) = compute_mean_scc(count1,counts)
        print scc,",",measured_scc

    
