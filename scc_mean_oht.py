#!/usr/bin/env python

import math
import sys

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
    scc = float(top)/float(bottom)
    mean = float(count1)/256.0
    return (mean,scc)

    
# get filename
filename = sys.argv[1]

print "mean, scc"
with open(filename,"rb") as f:
    bytes = f.read(32) # Read 256 bits
    while len(bytes) == 32:
        bitlist = list()
        for byte in bytes:
            for i in range(7,-1,-1):
                bit = ((ord(byte) >> i) & 0x01)
                bitlist.append(bit)
        (count1,counts) = scc256(bitlist) 
        (mean,scc) = compute_mean_scc(count1,counts)

        print mean," ",scc
        bytes = f.read(32)
f.close()

