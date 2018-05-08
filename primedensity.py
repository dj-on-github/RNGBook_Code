#!/usr/bin/python

import math

a = 2**1023
b = (2**1024)-1

denom_a = int(math.log(a))
denom_b = int(math.log(b))

pcount = (b/denom_b) - (a/denom_a) 

print "10^",math.log10(pcount)
print "2^",math.log(pcount,2)
