#!/usr/bin/env python

import math
from fractions import Fraction
from scipy.special import gamma, gammainc, gammaincc


#ones_table = [bin(i)[2:].count('1') for i in range(256)]
def count_ones_zeroes(bits):
    ones = 0
    zeroes = 0
    for bit in bits:
        if (bit == 1):
            ones += 1
        else:
            zeroes += 1
    return (zeroes,ones)

def monobit(bits):
    n = len(bits)

    zeroes,ones = count_ones_zeroes(bits)
    s = abs(ones-zeroes)

    p = math.erfc(float(s)/(math.sqrt(float(n)) * math.sqrt(2.0)))
    return p

def frequency_within_block(bits, num_of_blocks):
    block_size = int(math.floor(len(bits)/num_of_blocks))
    n = int(block_size * num_of_blocks)

    proportions = list()
    for i in xrange(num_of_blocks):
        block = bits[i*(block_size):((i+1)*(block_size))]
        zeroes,ones = count_ones_zeroes(block)
        proportions.append(Fraction(ones,block_size))

    chisq = 0.0
    for prop in proportions:
        chisq += 4.0*block_size*((prop - Fraction(1,2))**2)

    p = gammaincc((num_of_blocks/2.0),float(chisq)/2.0)
    return p

def hex2bits(thehex):
    bits = list()
    while True:
        if (thehex & 0x01) == 0x01:
            bits.append(1)
        else:
            bits.append(0)
        thehex = thehex >> 1
        if thehex == 0:
            break
    return bits


somehex = 0xff00ff00ff00ff0055aa55aa55aa55aa55aaab
bits = hex2bits(somehex)
print "bits = ",bits
print "Monobit(0x%x) = %f" % (somehex,monobit(bits))

print "Frequency within blocks"
bits=[0,1,1,0,0,1,1,0,1,0]
p = frequency_within_block(bits, 3)
print "bits =",bits
print "P = %f" % p
