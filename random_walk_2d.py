#!/usr/bin/env python

import random
import math
repetitions = 10000
steps = 30
finaldistance = [0 for x in range(-30,31)]
for i in xrange(repetitions):
    state = [0.0,0.0]
    for j in xrange(steps):
        x = random.uniform(-1.0,1.0)
        state[0] += x
        if random.choice([True,False]):
            state[1] += math.sqrt(1-(x*x))
        else:
            state[1] -= math.sqrt(1-(x*x))
    distance = math.sqrt(state[0]**2 + state[1]**2)
    intdist = int(math.floor(distance))
    finaldistance[intdist]+=1 
print "distance frequency"
for i in xrange(0,steps+1):
    print "%d %d" % (i,finaldistance[i])


