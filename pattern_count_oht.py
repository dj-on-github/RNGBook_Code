#!/usr/bin/env python

import math
import sys

previous = [0,0,0]

def oht(bitlist):
    global previous
    bitlist259 = previous + bitlist
    previous = bitlist[253:]
    counts = [0,0,0,0,0,0]
    for i in xrange(256):
        if bitlist259[i+3] == 1:
            counts[0] += 1
        if bitlist259[i+2:i+4] == [0,1]:
            counts[1] += 1
        if bitlist259[i+1:i+4] == [0,1,0]:
            counts[2] += 1
        if bitlist259[i:i+4] == [0,1,1,0]:
            counts[3] += 1  
        if bitlist259[i+1:i+4] == [1,0,1]:
            counts[4] += 1 
        if bitlist259[i:i+4] == [1,0,0,1]:
            counts[5] += 1 
    return counts

def check_bounds(counts):
    if (counts[0] <= 96) or (counts[0] >= 159): return False
    if (counts[1] <= 44) or (counts[1] >= 87): return False
    if (counts[2] <= 9)  or (counts[2] >= 58): return False
    if (counts[3] <= 4)  or (counts[3] >= 35): return False
    if (counts[4] <= 9)  or (counts[4] >= 58): return False
    if (counts[5] <= 4)  or (counts[5] >= 35): return False
    return True
    
# get filename
filename = sys.argv[1]

passfail=[0.0,0.0]
with open(filename,"rb") as f:
    bytes = f.read(32) # Read 256 bits
    while len(bytes) == 32:
        bitlist = list()
        for byte in bytes:
            for i in range(7,-1,-1):
                bit = ((ord(byte) >> i) & 0x01)
                bitlist.append(bit)
        counts = oht(bitlist) 
        if check_bounds(counts):
            passfail[0] += 1.0
        else:
            passfail[1] += 1.0
        bytes = f.read(32)
f.close()

print "Passing Blocks: ",passfail[0]
print "Failing Blocks: ",passfail[1]
print "Fail Percentage = ",(passfail[1])/(passfail[0]+passfail[1])*100.0,"%"
