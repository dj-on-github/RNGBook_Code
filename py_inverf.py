#!/usr/bin/env python

import scipy.special as s

for x in xrange(201):
    p = -1.0 + (x*0.01)
    erfi = s.erfinv(p)
    print "%1.2f  %1.8f" % (p,erfi)


