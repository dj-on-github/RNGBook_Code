#!/usr/bin/env python

import sys
import random
import math
rs = random.SystemRandom()

inside = 0
n = int(sys.argv[1])
# Assume r = 1.0 to simplify equation
for i in xrange(n):
    x = rs.random()
    y = rs.random()
    if ((x*x + y*y) <= 1.0):
        inside += 1

pi_approx = 4.0 * inside/n
err = (abs(math.pi - pi_approx)/math.pi)*100.0
print "Pi approximately = %8.6f  Error = %8.6f%%" % (pi_approx, err)

 
    