#!/usr/bin/env python

from rdrand import RdSeedom

r = RdSeedom()
for i in xrange(5):
    print "%f" % r.random()
print
for i in xrange(5):
    print "%032X" % r.getrandbits(256)

