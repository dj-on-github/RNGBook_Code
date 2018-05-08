#!/usr/bin/env python2

import sys

def binary_lagn(bits,n):
    # Initialize
    t1 = 0.0
    t2 = 0.0
    count = len(bits)

    for i in xrange(count):
        if (bits[(i+n) % count]==1) and (bits[i]==1):
            t1 += 1.0
        if (bits[i]==1):
            t2 = t2+1.0
    
    # Now compute the SCC from the counters
    lagnc = (count*t1 - t2*t2)/(count*t2 - t2*t2)

    return lagnc

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
reverse_len = int(sys.argv[2])

bits = read_binary_file(filename)


bits = bits[0:(len(bits)-(len(bits) % reverse_len))] # trim to a multiple of the bit reverse size

print "#n    lag-n"

# Reverse the bits 
block_count = len(bits)/reverse_len

reversed_bits = list()

for block in xrange(block_count):
    sublist = bits[block * reverse_len:(block+1)*reverse_len] # grab reverse_len bits
    outlist = list()
    for bit in sublist: # reverse them
        outlist.insert(0,bit)
    reversed_bits = reversed_bits+outlist # add them to the output 
    
for i in xrange(32):
    print "%d  %0.5f" % (i,(binary_lagn(reversed_bits,i)))
    
