#!/usr/bin/env python

import sys, random
randsource = random.SystemRandom() # nondeterministic random source

sides = int(sys.argv[1])
number_of_rolls = int(sys.argv[2])
throws = [randsource.randint(0,sides-1) for x in xrange(number_of_rolls)]
for throw in throws:
    print throw

