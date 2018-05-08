#!/usr/bin/env python

import math 
import gmpy2
from gmpy2 import mpfr
    
# Continued Fraction Computation
# 26.5.8 Handbook of Mathematical Functions, page 944
def d2mp1(a,b,m,x):
    result = (a+m)*(a+b+m)*x
    result = result/((a+(2*m))*(a+(2*m)+mpfr('1.0')))
    return -result
def d2m(a,b,m,x):
    result = m*(b-m)*x
    return result/((a+(2*m)-mpfr('1.0'))*(a+(2*m)))
    
# Recursive implementation of continued fraction
def ibeta_cf(d,a,b,x):
    if d == 100:
        return mpfr('0.0') # end at 100 iterations
    if d == 0: # First term 1/1+|
        mult = ((x**a)*((mpfr('1.0')-x)**b))/a
        mult = mult * gmpy2.gamma(a+b)
        mult = mult / (gmpy2.gamma(a) * gmpy2.gamma(b))    
        m=0
        return mult*mpfr('1.0')/(mpfr('1.0')+ibeta_cf(d+1,a,b,x))
    elif ((d % 2) == 1): # Odd terms d_n/1+|
        m = (d-1)/2
        return d2mp1(a,b,m,x)/(mpfr('1.0')+ibeta_cf(d+1,a,b,x))
    else:                # Even terms d_{n+1}+|
        m = d/2
        return d2m(a,b,m,x)/(mpfr('1.0')+ibeta_cf(d+1,a,b,x))

def ibeta(a,b,x):
    if (x == 0.0 or x==1.0):
        return x
    if x < ((a-1.0)/(a+b-2.0)):
        return ibeta_cf(0,a,b,x)
    else:
        return mpfr(1.0)-ibeta_cf(0,b,a,mpfr('1.0')-x)

 
