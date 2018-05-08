#!/usr/bin/env python

import random

bitsize = 16
iterations = 10000000
failcount = 0

maximum = (2**bitsize) -1

prev = random.randint(0, maximum)
for i in xrange(iterations):
    current = random.randint(0, maximum)
    if current == prev:
        failcount += 1
    prev = current

print "From 0 to",maximum
print "Errors ", failcount
print "1 error in %d numbers" % int(float(iterations)/float(failcount))


