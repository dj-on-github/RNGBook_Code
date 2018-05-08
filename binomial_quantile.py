#!/usr/bin/env python

import math
import gmpy2
from gmpy2 import mpfr
from incomplete_beta import *
from binomial_quantile import *

# Binomial CDF
def BCDF(n, k, p):
    return mpfr('1.0') - ibeta(mpfr(k+1),mpfr(n-k),p)

# Find smallest k where B(n,k,p) > alpha
# using binary chop search
# Equivalent to Excel CRITBINOM function
def binomial_quantile(n, p, alpha):
    min = 0;
    max = n;
    mid = min + ((max-min) >> 1)
    keepgoing = True
    while (keepgoing):
        b = BCDF(n,mid,p)
        if (b > alpha):
            max = mid
        elif (b < alpha):
            min = mid
        elif (b == alpha):
            keepgoing = False
 
        newmid = min + ((max-min) >> 1)
        if (newmid == mid):
            keepgoing=False
        mid = newmid
    
    if (b < alpha): # Make sure we have smallest b > alpha
        mid += 1
    return mid

