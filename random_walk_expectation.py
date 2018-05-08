#!/usr/bin/python

import math

def expected_dist(N,d):
    if d == 1:
        e = math.sqrt((2.0*N)/math.pi)
    else:
        e = math.sqrt((2.0*N)/d)
        e = e*(math.gamma((d+1)/2.0)/math.gamma(d/2.0))
    return e

N = 1000
for d in xrange(1,11):
    print "%d steps, %dD, expectation = %f" % (N,d,expected_dist(N,d))

