#!/usr/bin/env python2

import math
import sys
import random

previous = [0,]

blocksize = 256
if len(sys.argv) > 1:
    blocksize = int(sys.argv[1])

def scc_blocksize(bitlist,blocksize):
    global previous
    bitlist_sizeplus1 = previous + bitlist
    previous = bitlist[blocksize-1:]
    count1 = 0
    counts = [0,0,0,0]
    for i in xrange(blocksize):
        if bitlist[i] == 1:
            count1 += 1

        if bitlist_sizeplus1[i:i+2] == [0,0]:
            counts[0] += 1
        if bitlist_sizeplus1[i:i+2] == [1,0]:
            counts[1] += 1
        if bitlist_sizeplus1[i:i+2] == [0,1]:
            counts[2] += 1
        if bitlist_sizeplus1[i:i+2] == [1,1]:
            counts[3] += 1  
    return (count1,counts)

def compute_mean_scc(count1,counts):
    n = blocksize
    top = (n*counts[3]) - ((counts[2] + counts[3])*(counts[2] + counts[3]))
    bottom = (n*(counts[2] + counts[3])) - ((counts[2] + counts[3])*(counts[2] + counts[3]))
    if (bottom > 0):
        scc = float(top)/float(bottom)
    else:
        scc = 1.0
    mean = float(count1)/float(blocksize)
    return (mean,scc)

    
def gen_scc_data(scc):
    prev = 0
    for i in range(256):
        bits = list()
        for j in range(blocksize):
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
        (count1,counts) = scc_blocksize(bitlist,blocksize)
        (mean,measured_scc) = compute_mean_scc(count1,counts)
        print scc,",",measured_scc

    
