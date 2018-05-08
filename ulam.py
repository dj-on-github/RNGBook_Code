#!/usr/bin/env python2

import sys

tries = int(sys.argv[1])

N = range(tries)

def isprime(n):
    """Returns True if n is prime."""
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True

cnt = 0

for i in N:
    x = ((i*i)-i)+41
    if isprime(x):
        cnt += 1
    print str(i).ljust(4),": ",str(x).ljust(5),"   ",str(isprime(x))
    
print str(cnt),"/",str(tries)
