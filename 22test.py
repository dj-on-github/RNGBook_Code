#!/usr/bin/env python

import math
from fractions import Fraction
from scipy.special import gamma, gammainc, gammaincc
import numpy
import cmath
import random

from sp800_22_binary_matrix_rank_test import *
from sp800_22_non_overlapping_template_matching_test import *
from sp800_22_dft_test import *
from sp800_22_overlapping_template_matching_test import *
from sp800_22_frequency_within_block_test import *
from sp800_22_random_excursion_variant_test import *
from sp800_22_longest_run_ones_in_a_block_test import *
from sp800_22_runs_test import *


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

def monobit(bits):
    n = len(bits)
    
    zeroes,ones = count_ones_zeroes(bits)
    s = abs(ones-zeroes)
    
    p = math.erfc(float(s)/(math.sqrt(float(n)) * math.sqrt(2.0)))
    return p


# RANDOM EXCURSION TEST
def random_excursion_test(bits):
    n = len(bits)

    x = list()             # Convert to +1,-1
    for bit in bits:
        x.append((bit*2)-1)

    # Build the partial sums
    pos = 0
    s = list()
    for e in x:
        pos = pos+e
        s.append(pos)    
    sprime = [0]+s+[0] # Add 0 on each end
    
    # Build the list of cycles
    pos = 1
    cycles = list()
    while (pos < len(sprime)):
        cycle = list()
        cycle.append(0)
        while sprime[pos]!=0:
            cycle.append(sprime[pos])
            pos += 1
        cycle.append(0)
        cycles.append(cycle)
        pos = pos + 1
    
    J = len(cycles)
    print "J="+str(J)    
    
    vxk = [['a','b','c','d','e','f'] for y in [-4,-3,-2,-1,1,2,3,4] ]

    # Count Occurances  
    for k in xrange(6):
        for index in xrange(8):
            mapping = [-4,-3,-2,-1,1,2,3,4]
            x = mapping[index]
            cyclecount = 0
            #count how many cycles in which x occurs k times
            for cycle in cycles:
                oc = 0
                #Count how many times x occurs in the current cycle
                for pos in cycle:
                    if (pos == x):
                        oc += 1
                # If x occurs k times, increment the cycle count
                if (k < 5):
                    if oc == k:
                        cyclecount += 1
                else:
                    if k == 5:
                        if oc >=5:
                            cyclecount += 1
            vxk[index][k] = cyclecount
    
    # Table for reference random probabilities
    pixk=[[0.5     ,0.25   ,0.125  ,0.0625  ,0.0312 ,0.0312],
          [0.75    ,0.0625 ,0.0469 ,0.0352  ,0.0264 ,0.0791],
          [0.8333  ,0.0278 ,0.0231 ,0.0193  ,0.0161 ,0.0804],
          [0.875   ,0.0156 ,0.0137 ,0.012   ,0.0105 ,0.0733],
          [0.9     ,0.01   ,0.009  ,0.0081  ,0.0073 ,0.0656],
          [0.9167  ,0.0069 ,0.0064 ,0.0058  ,0.0053 ,0.0588],
          [0.9286  ,0.0051 ,0.0047 ,0.0044  ,0.0041 ,0.0531]]
    # Compute chi-sq and P value for the 8 cases
    success = True
    for index in xrange(8):
        mapping = [-4,-3,-2,-1,1,2,3,4]
        x = mapping[index]
        chisq = 0.0
        for k in xrange(6):
            top = float(vxk[index][k]) - (float(J) * (pixk[abs(x)-1][k]))
            top = top*top
            bottom = J * pixk[abs(x)-1][k]
            chisq += top/bottom
        p = gammaincc(5.0/2.0,chisq/2.0)
        if p < 0.01:
            err = " Not Random"
            success = False
        else:
            err = ""
        print "x = %1.0f\tchisq = %f\tp = %f %s"  % (x,chisq,p,err)

    if success:
        print "PASS"
    else:    
        print "FAIL: Data not random"
    return success,sprime

somehex = 0xff00ff00ff00ff0055aa55aa55aa55aa55aaab
bits = hex2bits(somehex)
print "bits = ",bits
print "Monobit(0x%x) = %f" % (somehex,monobit(bits))

print
print "Frequency within blocks"
bits=[0,1,1,0,0,1,1,0,1,0]
p = frequency_within_block_test(bits, 3)
print "bits =",bits 
print "P = %f" % p

print
print "Runs Test"
bits=[1,0,0,1,1,0,1,0,1,1]
p = runs(bits)
print "bits =",bits 
print "P = %f" % p

print
print "Longest Run of Ones in a Block test"
print "Waiting on book"

print
print "DFT Test"
bits=[1,1,0,0,1,0,0,1,0,0,0,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,1,1,
      0,0,0,0,1,0,0,0,1,1,0,1,0,0,1,1,0,0,0,1,0,0,1,1,0,0,0,1,1,0,0,1,1,0,0,0,1,0,1,0,0,0,1,0,1,1,1,0,0,0]

p = dft_test(bits)
print bits
print "P=",p

print
print "Non Overlapping Template Test"

bits = list()
for i in xrange(2**10):
    r = random.getrandbits(2**10)
    for j in xrange(2**10):
        bits.append(r & 0x1)
        r = r >> 1
N = 8
M = len(bits)/N
B = [0,0,0,0,0,0,0,0,1]

p = non_overlapping_template_matching_test(bits,B,M,N)

print "len(bits) = ",len(bits)
print "M = ",M
print "N = ",N
print "B = ",B
print "P-Value = ",p

print
print "Overlapping Template Test"

bits = list()
for i in xrange(1000):
    r = random.getrandbits(1000)
    for j in xrange(1000):
        bits.append(r & 0x1)
        r = r >> 1
N = 968
M = 1032
B = [1,1,1,1,1,1,1,1,1]
K = 5

p = overlapping_template_matching_test(bits,B,M,N,K)

print "len(bits) = ",len(bits)
print "M = ",M
print "N = ",N
print "P-Value = ",p

print
print "Random Excursion Test"
bits=[0,1,1,0,1,1,0,1,0,1]
print "bits = "+str(bits)
success,sprime = random_excursion_test(bits)

f = open('../data_files/random_excursion_test1.dat','w')
x = 0
f.write("#x\tpos\n")
for t in sprime:
    f.write("%d\t%d\n" % (x,t))
    x += 1
f.close()

#Gather 1,000,000 bits and run through excursion test.
bits = list()
for i in xrange(1000):
    r = random.getrandbits(1000)
    for j in xrange(1000):
        bits.append(r & 0x1)
        r = r >> 1
success,sprime = random_excursion_test(bits)

#Gather 1,000,000 bits and run through excursion variant test.
print
print "Random Excursion Variant Test"
bits = list()
for i in xrange(1000):
    r = random.getrandbits(1000)
    for j in xrange(1000):
        bits.append(r & 0x1)
        r = r >> 1
success,sprime = random_excursion_variant_test(bits)
