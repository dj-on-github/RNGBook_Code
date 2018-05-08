#!/usr/bin/python
import math

def is_prime(n):
    if n==2 or n==3: return True
    if (n % 2 == 0) or (n < 2): return False # Reject even or negative
    limit = int(n**0.5)+1
    for i in xrange(3,limit,2): # list of odd numbers
        if (n % i == 0):
            return False    
    return True

for n in xrange(2**17):
    if is_prime(n):
        print n


