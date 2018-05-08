#!/usr/bin/env python

import math
from fractions import Fraction
from scipy.special import gamma, gammainc, gammaincc
import numpy
import cmath
import random

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

def runs(bits):
    n = len(bits)
    zeroes,ones = count_ones_zeroes(bits)

    prop = float(ones)/float(n)
    print "prop ",prop

    tau = 2.0/math.sqrt(n)
    print "tau ",tau

    if abs(prop-0.5) > tau:
        return 0

    vobs = 1.0
    for i in xrange(n-1):
        if bits[i] != bits[i+1]:
            vobs += 1.0

    print "vobs ",vobs
      
    p = math.erfc(abs(vobs - (2.0*n*prop*(1.0-prop)))/(2.0*math.sqrt(2.0*n)*prop*(1-prop) ))
    print "p ",p
    return p

def longest_run_of_ones_in_a_block(bits):
    n = len(bits)

    if n < 128:
        return 0
    elif n<6272:
        M = 8
    elif n<750000:
        M = 128
    else:
        M = 10000

    N = int(floor(float(n)/float(m)))

    v = [0,0,0,0,0,0,0]

    for i in xrange(N):
        #find longest run
        block = bits[i*M:((i+1)*M)]
        run = 0
        longest = 0
        for j in xrange(N):
            if bits[j] == 1:
                run += 1
                if run > longest:
                    longest = run
            else:
                run = 0

        if M == 8:
            if longest <= 1:
                v[0] += 1
            elif longest == 2:
                v[1] += 1
            elif longest == 3:
                v[2] += 1
            else:
                v[3] += 1
        elif M == 128:
            if longest <= 4:
                v[0] += 1
            elif longest == 5:
                v[1] += 1
            elif longest == 6:
                v[2] += 1
            elif longest == 7:
                v[3] += 1
            elif longest == 8:
                v[4] += 1
            else:
                v[5] += 1
        else:
            if longest <= 10:
                v[0] += 1
            elif longest == 11:
                v[1] += 1
            elif longest == 12:
                v[2] += 1
            elif longest == 13:
                v[3] += 1
            elif longest == 14:
                v[4] += 1
            elif longest == 15:
                v[5] += 1
            else:
                v[6] += 1


        # Waiting on book Random Walk in Random and non Random environments"

def binary_matrix_rank_test(bits):
    return 0

def dft(bits):
    N = len(bits)
    result = list()
    for k in xrange(N):
        pt = complex(0,0)
        for n in xrange(N):
            pt = pt + bits[n] * cmath.exp(-2 * cmath.pi * complex(0,1) * complex(k,0)/N)
        result.append(pt)
        print "pt:",pt
    return result
 

def fft(bits):
    N = len(bits)
    if N==1:
        return bits
    elif N % 2 != 0:
        raise ValueError("Please make array length power of 2")
    else:
        evenside = fft(bits[::2])
        oddside = fft(bits[1::2])
        twiddles = list()
        for i in xrange(N):
            twiddle = (cmath.exp(-2j * complex(math.pi * i / N)))
            twiddles.append(twiddle)
        left = list()
        right = list()
        for i in xrange(N/2):
            left.append(evenside[i] + (twiddles[(N/2)+i]*oddside[i]))
            right.append(evenside[i] + (twiddles[i]*oddside[i]))
            result = left+right
        print "result:",result
        return result
        #return np.concatenate([evenside + twiddles[:N / 2] *oddside, evenside + factor[N / 2:] * oddside])

def dft_test(bits):
    n = len(bits)
    if (n % 2) == 1:        # Make it an even number
        raise ValueError("The number of data samples must be even")

    ts = list()             # Convert to +1,-2
    for bit in bits:
        if bit == 0:
            ts.append(-1.0)
        else:
            ts.append(1.0)

    ts_np = numpy.array(ts)
    fs = numpy.fft.fft(ts_np)  # Compute DFT
   
    mags = abs(fs)[:n/2] # Compute magnitudes of first half of sequence

    T = math.sqrt(math.log(1.0/0.05)*n) # Compute upper threshold
    N0 = 0.95*n/2.0

    N1 = 0.0   # Count the peaks above the upper theshold
    for mag in mags:
        if mag < T:
            N1 += 1.0

    d = (N1 - N0)/math.sqrt((n*0.95*0.5)/4) # Compute the P value
    p = math.erfc(abs(d)/math.sqrt(2))

    return p

#SP800-22 2.7
def non_overlapping_template_matching_test(bits,B,M,N):
    n = len(bits)
    m = len(B)
    if (n != (M*N)):
        raise ValueError("N blocks of M bits doesn't add up to the number of bits")

    blocks = list() # Split into N blocks of M bits
    for i in xrange(N):
        blocks.append(bits[i*M:(i+1)*M])

    W=list() # Count the number of matches of the template in each block Wj
    for block in blocks:
        position = 0
        count = 0
        while position < (M-m):
            if block[position:position+m] == B:
                position += m
                count += 1
            else:
                position += 1
        W.append(count)

    mu = float(M-m+1)/float(2**m) # Compute mu and sigma
    sigma = M * ((1.0/float(2**m))-(float((2*m)-1)/float(2**(2*m))))

    chisq = 0.0  # Compute Chi-Square
    for j in xrange(N):
        chisq += ((W[j] - mu)**2)/(sigma**2)

    p = gammaincc(N/2.0, chisq/2.0) # Compute P value

    return p

#SP800-22r1a 2.8
def overlapping_template_matching_test(bits,B,M,N,K):
    n = len(bits)
    m = len(B)
    if (n < (M*N)):
        raise ValueError("N blocks of M bits is more than the number of bits")

    blocks = list() # Split into N blocks of M bits
    for i in xrange(N):
        blocks.append(bits[i*M:(i+1)*M])

    v = [0,0,0,0,0,0] # Count the number of matches of the template in each block Wj
    for block in blocks:
        position = 0
        count = 0
        for position in xrange(M-m):
            if block[position:position+m] == B:
                count += 1
            position += 1
        if count < 5:
            v[count] += 1
        else:
            v[5] += 1
 
    lam = float(M-m+1)/float(2**m) # Compute lambda and nu
    nu = lam/2.0

    chisq = 0.0  # Compute Chi-Square
    pi = [0.364091,0.185659,0.139381,0.100571,0.070432,0.139865]
    for i in xrange(6):
        chisq += ((v[i] - N*pi[i])**2)/(N*pi[i])

    p = gammaincc(5.0/2.0, chisq/2.0) # Compute P value

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

# RANDOM EXCURSION VARIANT TEST
def random_excursion_variant_test(bits):
    n = len(bits)

    x = list()             # Convert to +1,-2
    for bit in bits:
        x.append((bit * 2)-1)

    # Build the partial sums
    pos = 0
    s = list()
    for e in x:
        pos = pos+e
        s.append(pos)    
    sprime = [0]+s+[0] # Add 0 on each end

    # Count the number of cycles J
    J = 0
    for value in sprime[1:]:
        if value == 0:
            J += 1
            
    # Build the counts of offsets
    count = [0 for x in xrange(-9,10)]
    for value in sprime:
        if (abs(value) < 10):
            count[value] += 1

    # Compute P values
    success = True
    for x in xrange(-9,10):
        if x != 0:
            top = abs(count[x]-J)
            bottom = math.sqrt(2.0 * J *((4.0*abs(x))-2.0))
            p = top/bottom

            if p < 0.01:
                err = " Not Random"
                success = False
            else:
                err = ""
            print "x = %1.0f\t count=%d\tp = %f %s"  % (x,count[x],p,err)
            
    if (J < 500):
        print "J too small (J < 500) for result to be reliable"
    elif success:
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
p = frequency_within_block(bits, 3)
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
