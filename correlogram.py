#!/usr/bin/env python

import math
import numpy
import cmath
import random

# Compute Correlogram with the Wiener-Khninchin theorem 
#   Fr(f) = FFT[X(t)]
#   S(f) = Fr(f)Fr*(f)  // times its complex conugate
#   R(tau) = IFFT[S(f)]

def wiener_khninchin(bits):
    n = len(bits)
    if (n % 2) == 1:        # Make it an even number
        raise ValueError("The number of data samples must be even")

    ts = list()             # Convert to +1,-1
    for bit in bits:
        if bit == 0:
            ts.append(-1.0)
        else:
            ts.append(1.0)

    ts_np = numpy.array(ts)
    fs = numpy.fft.fft(ts_np)  # Compute DFT
   
    # Muliply each element by its complex conjugate
    fs_out = list()
    for x in xrange(len(fs)):
        theconjugate = fs[x].conjugate()
        newvalue = fs[x]*theconjugate
        fs_out.append(newvalue)
    np_fs_out = numpy.array(fs_out)

    # Take the inverse FFT
    crg = numpy.fft.ifft(np_fs_out)

    # Turn it into a list of reals
    corellogram = list()
    for x in  crg:
        corellogram.append(x.real/n)

    return corellogram


# Make some serially correlated bits
r = random.SystemRandom()
bits = list()
previous = 0
for i in xrange(256):
    if previous == 0:
        level = 0.2
    else:
        level = 0.8
    ref = r.random()
    if (ref > level):
        newbit = 1
    else:
        newbit = 0
    previous = newbit
    bits.append(newbit)

c = wiener_khninchin(bits) # Compute the correllogram

print "bits:",bits
print
for i in xrange(32):
    print "%02d  %06f" % (i,c[i])
 
