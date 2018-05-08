#!/usr/bin/python

import random
rand = random.SystemRandom()

# Miller Rabin Primality Test
def is_probably_prime(n,k):
    # The range doesn't handle the small primes well
    # So handle them first
    if (n == 2) or (n == 3) or (n==5):
        return True
    if (n < 7):
        return False
    
    # Separate the 2 factors from n-1
    # So n-1 = 2**r * d
    d = n-1
    r = 0
    while ((d % 2) == 0) and (d > 2):
        d = d >> 1
        r = r + 1
    # k is the chosen iteration count
    for i in xrange(k):
        a = rand.randint(2,n-2)
        x = pow(a,d,n)
        if (x==1) or (x == (n-1)):
            continue
            
        for j in xrange(r-1):
            x = pow(x,2,n)
            if x == 1:
                return False
            if x == (n-1):
                break
        if x == (n-1):
            continue
        return False
    return True

#for i in xrange(1,100):
#    if is_probably_prime(i,10):
#        print "%d  Prime" % i
#    else:
#        print "%d" % i

def find_prime(bits):
    n = rand.getrandbits(bits)
    n = n | 0x01 # set the lowest bit
    n = n | (1 << (bits-1)) # set the upper bit
    k = 133
    while not(is_probably_prime(n,k)):
        n = rand.getrandbits(bits)
        n = n | 0x01 # set the lowest bit
        n = n | (1 << (bits-1)) # set the upper bit
    return n

if __name__ == "__main__":
    for i in xrange(4):
        x = find_prime(1024)
        print "Prime %X" % x
    