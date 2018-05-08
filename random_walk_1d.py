#!/usr/bin/env python

import random
repetitions = 10000
steps = 30
finalstates = [0 for i in xrange(0,steps+1)]
for i in xrange(repetitions):
    state = 0
    for j in xrange(steps):
        if random.choice([True, False]):
            state += 1
        else:
            state -= 1
    finalstates[abs(state)] += 1
# Print out
for i in xrange(0,steps+1):
    print "%d %d" % (i,finalstates[i])


