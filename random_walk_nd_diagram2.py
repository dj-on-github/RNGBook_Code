#!/usr/bin/env python

import sys
import random
import math

# Compute the end points of a number of random walks.

n = 2 # 2 dimension
steps = int(sys.argv[1]) # Number of steps
number_of_paths = int(sys.argv[2]) # number of paths

def random_unit_n_vector(n):
    v = [random.gauss(0, 1) for i in xrange(n)]
    m = math.sqrt(sum(x*x for x in v))
    return [x/m for x in v]

print "# Final position of %d 2D random walks of %d steps" %(number_of_paths,steps)
print "#X         Y"
for i in xrange(number_of_paths):
    state = [0.0 for x in xrange(n)]
    for j in xrange(steps):
        step = random_unit_n_vector(n)
        state2 = [a + b for a,b in zip(state, step)]
        state = state2
    print str(state[0])+"  "+str(state[1])


