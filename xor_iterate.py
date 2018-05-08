from fractions import Fraction
from mpmath import *

def xor_iterate(n):
    next_prob=dict()
    one_third = Fraction('1/3')
    p_input = {0:0, 1:one_third, 2:one_third, 3:one_third}
    p_pool = p_input
    print("Iteration P(00)    P(01)    P(10)    P(11)")
    for i in range(n):
        prob00  = p_input[0]*p_pool[0]
        prob00 += p_input[1]*p_pool[1]
        prob00 += p_input[2]*p_pool[2]
        prob00 += p_input[2]*p_pool[3]
        
        prob01  = p_input[0]*p_pool[1]
        prob01 += p_input[1]*p_pool[0]
        prob01 += p_input[2]*p_pool[3]
        prob01 += p_input[3]*p_pool[2]
        
        prob10  = p_input[0]*p_pool[2]
        prob10 += p_input[1]*p_pool[3]
        prob10 += p_input[2]*p_pool[0]
        prob10 += p_input[3]*p_pool[1]
        
        prob11  = p_input[0]*p_pool[3]
        prob11 += p_input[1]*p_pool[2]
        prob11 += p_input[2]*p_pool[1]
        prob11 += p_input[3]*p_pool[0]
        
        p_pool = {0:prob00, 1:prob01, 2:prob10, 3:prob11}
    
        iter = "%d" % (i+1)
        print(iter.rjust(4)+("      %4f %4f %4f %4f" % ( p_pool[0], p_pool[1], p_pool[2], p_pool[3])))
        
def xor_iterate64(n):
    mp.prec = 200
    oo2sf   = mpf(1)/mpf(2**64)
    oo2sfmo = mpf(1)/mpf((2**64)-1)
    ttt64   = mpf(2**64)
    ttt64m1 = mpf((2**64)-1)
    ttt64m2 = mpf((2**64)-2)
    
    p_input_0 = mpf(0)
    p_input_other = oo2sfmo
    
    p_pool_0 = p_input_0
    p_pool_other = p_input_other
    
    for i in range(n):
        p_0     = p_input_0 * p_pool_0
        p_0    += ttt64m1 * p_input_other * p_pool_other
        
        p_other  = p_input_0 * p_pool_other
        p_other += p_input_other * p_pool_0
        p_other += ttt64m2 * p_input_other * p_pool_other
        
        p_pool_0 = p_0
        p_pool_other = p_other
        difference = p_pool_0 - p_pool_other
    
        print("Iteration  %d" % (i+1))
        print("  P(0)    ",p_pool_0)
        print("  P(Other)",p_pool_other)
        print("  Difference ",difference)
        print()
        
        #print iter.rjust(4)+"  "+str(fp0)+" "+str(fp_other)

# A 16 bit random number source
import os
from struct import *
        
def rand16(bits):
    # Get two random bytes from the operating system
    a = os.urandom(2)
    # unpack it into an integer from -32768 .. 32767
    therand16 = unpack('H',a)[0]
    # Fold the negative values to the upper half of 0..65535.
    if therand16 < 0:
        therand16 += 0x8000
    # 2^bits -1 is bits binary ones. E.G. (2^4)-1 = b1111.
    # Using this to mask in just the lower bits bits.
    mask = (2**bits)-1  
    therand16 = therand16 & mask    
    return therand16

# compute output distribution of XORing together outputs from a
# uniform distribution passed through FIPS 140-2
def xor_iteraten_fips(bits=16, iterations=2):
    mp.prec = 200
    oo2s   = mpf(1)/mpf(2**bits)
    oo2smo = mpf(1)/mpf((2**bits)-1)
    ttt16   = mpf(2**bits)
    ttt16m1 = mpf((2**bits)-1)
    ttt16m2 = mpf((2**bits)-2)
    
    # fetch the first random number to initialize the comparison value
    # as per FIPS 140-2 4.9.2

    lastrand = rand16(bits)    
    
    # initialize the input probabilities. The lastrand gets 0
    # others get 1/(2^bits -1)
    p_input = list()
    next_p = list()
    p_pool = list()
    for i in range(2**bits):
        p_input.append(0)
        p_pool.append(oo2smo)
        next_p.append(0)
    p_pool[lastrand] = 0
    
    print("Initial rand = %X" % lastrand)
    
    for i in range(iterations):
        # Get a random number n bits wide
        therand = rand16(bits)
        
        # The FIPS 4.9.2 filter:
        # Keep getting the number until you get one that doesn't match the previous value
        while (therand == lastrand):
            therand = rand16(bits)
        
        # fill in the input distribution and
        # Initialize the next_p distibution to all zeroes.
        for j in range(2**bits):
            p_input[j] = oo2smo
            next_p[j]=0
        p_input[lastrand] = 0
        
        # The inner loop, compute the probability of each combination
        # and its resulting value. Add up the probabilities of each
        # resulting value into next_p.
        # This algorithm is O(bits^2) so runs slow for large bits.
        for a in range(2**bits):
            for b in range(2**bits):
                axorb = a ^ b
                p_axorb = p_input[a] * p_pool[b]
                next_p[axorb] += p_axorb
                
        # The random number from the last iteration becomes the 
        # last random number for the next iteration.
        lastrand = therand
        
        # The pool for the next iteration becomes the result of this iteration.
        for j in range(2**bits):
            p_pool[j] = next_p[j]
        
        print("Iteration  %d - random# = %X" % (i+1, lastrand))
        print("  minP    ",min(p_pool))
        print("  maxP    ",max(p_pool))
        print("  Difference ",(max(p_pool)-min(p_pool)))
        print()  

From mpmath import *
        
def xor_iterate64(n):
    mp.prec = 200
    oo2sf   = mpf(1)/mpf(2**64)
    oo2sfmo = mpf(1)/mpf((2**64)-1)
    ttt64   = mpf(2**64)
    ttt64m1 = mpf((2**64)-1)
    ttt64m2 = mpf((2**64)-2)
    
    p_input_0 = mpf(0)
    p_input_other = oo2sfmo
    
    p_pool_0 = p_input_0
    p_pool_other = p_input_other
    
    for i in xrange(n):
        p_0     = p_input_0 * p_pool_0
        p_0    += ttt64m1 * p_input_other * p_pool_other
        
        p_other  = p_input_0 * p_pool_other
        p_other += p_input_other * p_pool_0
        p_other += ttt64m2 * p_input_other * p_pool_other
        
        p_pool_0 = p_0
        p_pool_other = p_other
        difference = p_pool_0 – p_pool_other
    
        print “Iteration  %d” % (i+1)
        print “  P(0)    “,p_pool_0
        print “  P(Other)”,p_pool_other
        print “  Difference “,difference
        print

        