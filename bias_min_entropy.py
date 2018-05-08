#!/usr/bin/env python

import math
from fractions import Fraction

def bias_min_entropy(n,b):
    #me = -math.log((math.factorial(n)/( (2**n) * math.factorial((int(b*n))) * math.factorial((int(n-(b*n)))) ) ),2)
    #me = (math.factorial(n)/( (2**n) * math.factorial((int(b*n))) * math.factorial((int(n-(b*n)))) ) )
    upper = math.factorial(n)
    lower =  (2**n) * math.factorial((int(b*n))) * math.factorial((int(n-(b*n))))
    inner = Fraction(upper,lower)

    if bias > 0.5:
        p = bias**n
    else:
        p = (1-bias)**n

    me = -math.log(p,2)
    return me

print "# bias min-entropy"

for count in xrange(21):
    bias = 0.05 * count

    me = bias_min_entropy(100,bias)/100

    print "%1.2f  %f" % (bias,me)


