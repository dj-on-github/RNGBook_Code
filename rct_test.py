#!/usr/bin/env python2

import random
import math
import sys

# Read data.
def read_binary_file(symbol_size,filename):
    bits = list()
    symbols = list()
    with open(filename, "rb") as thefile:
        while True:
            block = thefile.read(4096)
            if block:
                for thebyte in block:
                    for i in xrange(8):
                        thebit = (((ord(thebyte) << i) & 0x80) >> 7)
                        bits.append(thebit)
                symbolcount = int(math.floor(len(bits)/symbol_size))
                for symbolnum in xrange(symbolcount):
                    symbolbits = bits[symbolnum*symbol_size:(symbolnum+1)*symbol_size]
                    symbol = 0
                    for bit in symbolbits:
                        symbol = (symbol << 1)+bit
                    symbols.append(symbol)
                bits = bits[(symbol_size*symbolcount):] # Save leftover bits
                for symbol in symbols:
                    yield symbol
            else:
                return


W = float(sys.argv[1])
H = float(sys.argv[2])
symbol_size = int(sys.argv[3])
filename = str(sys.argv[4])

f = read_binary_file(symbol_size,filename)

A = f.next()
B = 1
errors = 0
maxcount = 10**7

C = int(math.ceil((W/H) + 1.0))
print "W =",W
print "H =",H
print "Symbol Size =",symbol_size 
print "C =",C

count = 0
for X in f:
    count += 1
    if A == X:
        B += 1
        if B >= C:
            errors += 1
            B = 1
    else:
        B = 1
    A = X

print "Errors %d  Count = %d rate = %f as_a_power_of_2 = %f  " % \
  (errors,count, (count/errors), math.log((count/errors),2))

