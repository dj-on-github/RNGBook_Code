#!/usr/bin/env python

import math
import random
rs = random.SystemRandom()

def rand_range(range_start, range_end):
    range_size = 1+range_end-range_start
    number_of_bits = int(math.ceil(math.log(range_size,2)))
    while True:
        x = rs.getrandbits(number_of_bits)
        if x < range_size:
            break

    result = x + range_start
    return result

range_start = 5
range_end = 14
number_of_numbers = 1000000

histogram = [0 for x in range(range_end+4)]

for i in xrange(number_of_numbers):
    result = rand_range(range_start,range_end)
    histogram[result] = histogram[result]+1

print("Histogram")
for i in xrange(range_end+3):
    print("value : %2d  frequency %d" % (i,histogram[i]))
 
