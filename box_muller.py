#!/usr/bin/env python

import sys
import random
import math
randsource = random.SystemRandom() # nondeterministic random source

n = int(sys.argv[1])  # Number of random numbers

even_n=n        # Compute the number of pairs necessary to
if (n % 2)==1:  # provide at least n numbers.
    even_n = n+1

for i in xrange(even_n/2):   # Generate n/2 pairs
    u1 = randsource.random()
    u2 = randsource.random()
    x1 = math.sqrt(-2.0*math.log(u1))*math.cos(2.0*math.pi*u2)
    x2 = math.sqrt(-2.0*math.log(u1))*math.sin(2.0*math.pi*u2)
    
    print x1  # Output the result
    if ((i+1)*2) <= n: # Don't output the last number if n was odd
        print x2
 
 
