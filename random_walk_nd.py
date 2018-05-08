#!/usr/bin/env python

import sys
import random
import math
repetitions = 10000
steps = 30

n = int(sys.argv[1])     # Number of dimensions
limit = int(sys.argv[2]) # Maximum bin number
if len(sys.argv) > 2:
    granularity = int(sys.argv[3])
else:
    granularity = 1
    
def random_unit_n_vector(n):
    v = [random.gauss(0, 1) for i in xrange(n)]
    m = math.sqrt(sum(x*x for x in v))
    return [x/m for x in v]

finaldistance = [0 for x in xrange(0,(granularity*steps)+1)]
for i in xrange(repetitions):
    state = [0.0 for x in xrange(n)]
    for j in xrange(steps):
        step = random_unit_n_vector(n)
        state2 = [a + b for a,b in zip(state, step)]
        state = state2
    distance = math.sqrt(sum(x*x for x in state))
    intdist = int(math.floor(distance*granularity))
    finaldistance[intdist]+=1 

# Print out
for i in xrange((granularity*limit)+1):
    print "%2.1f %d" % (float(i)/float(granularity),finaldistance[i])


