#!/usr/bin/env python

import sys

def binary_lagn(bits,n):
    # Initialize
    t1 = 0.0
    t2 = 0.0
    equal_count = 0
    notequal_count = 0 
    count = len(bits)
    for i in xrange(count):
        if bits[(i+n) % count]==bits[i]:
            equal_count += 1
        else:
            notequal_count +=1

        if (bits[(i+n) % count]==1) and (bits[i]==1):
            t1 += 1.0
        if (bits[i]==1):
            t2 = t2+1.0

    # Now compute the SCC from the counters
    lagnc = (count*t1 - t2*t2)/(count*t2 - t2*t2)

    prob_equal = float(equal_count)/float(equal_count+notequal_count)
    return lagnc,prob_equal

# Read data in blocks for speed.
def read_binary_file(filename):
    bits = list()
    with open(filename, "rb") as thefile:
        while True:
            block = thefile.read(4096)
            if block:
                for thebyte in block:
                    for i in xrange(8):
                        thebit = (((ord(thebyte) << i) & 0x80) >> 7)
                        bits.append(thebit)
            else:
                return bits

filename = sys.argv[1]
bits = read_binary_file(filename)

print "#n    lag-n probequal"
for i in xrange(16):
    lagn,prob_eq = binary_lagn(bits,i)
    lagn2 = 2.0*(prob_eq-0.5)
    print "%d  %0.5f  %0.5f %0.5f" % (i, lagn,prob_eq,lagn2)
    
