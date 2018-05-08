#!/usr/bin/env python

import math
import random
rs = random.SystemRandom()

def rand_range(maxrand):
    number_of_bits = int(math.ceil(math.log(maxrand+1,2))) + 64
    x = rs.getrandbits(number_of_bits)
    x = x % 12
    return x

histogram = [0 for x in range(16)]

for i in xrange(1000000):
    result = rand_range(11)
    histogram[result] = histogram[result]+1

print("Histogram")
for i in xrange(16):
    print("value : %2d  frequency %d" % (i,histogram[i]))
 
