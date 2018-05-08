#!/usr/bin/env python

import math 
from mpmath import *

PRECISION = 300

# Continued Fraction Computation
# 6.5.31 Handbook of Mathematical Functions, page 263
#    Recursive implementation
def ibeta_cf(d,a,b,x):
    if d == 100:
        return mpf('0.0') # end at 100 iterations
    if d == 0: # First term 1/1+|
        mult = ((x**a)*((mpf('1.0')-x)**b))/a
        mult = mult * gamma(a+b)
        mult = mult / (gamma(a) * gamma(b))    
        m=0
        return mult*mpf('1.0')/(mpf('1.0')+ibeta_cf(d+1,a,b,x))
    elif ((d % 2) == 1):
        m = (d-1)/2
        result = (a+m)*(a+b+m)*x
        result = -result/((a+(2*m))*(a+(2*m)+mpf('1.0')))
        return result/(mpf('1.0')+ibeta_cf(d+1,a,b,x))
        #return d2mp1(a,b,m,x)/(mpf('1.0')+ibeta_cf(d+1,a,b,x))
    else:
        m = d/2
        result = (m*(b-m)*x)/((a+(2*m)-mpf('1.0'))*(a+(2*m)))
        return result/(mpf('1.0')+ibeta_cf(d+1,a,b,x))
        #return d2m(a,b,m,x)/(mpf('1.0')+ibeta_cf(d+1,a,b,x))



# An iterative version working backwards through the continued fraction
def ibeta_cf_backwards(a,b,x):
    f = mpf('0.0')  # running fraction value
    for d in range(100,-1,-1):
        if d == 0: # First Term (last of iteration) 1/1+|
            mult = ((x**a)*((mpf('1.0')-x)**b))/a
            mult = mult * gamma(a+b)
            mult = mult / (gamma(a) * gamma(b))    
            m=0
            return mult*mpf('1.0')/(mpf('1.0')+f)
        elif ((d % 2) == 1): # Odd terms e_{2*m +1}
            m = (d-1)/2
            numerator = (a+m)*(a+b+m)*x
            numerator = -numerator/((a+(2*m))*(a+(2*m)+mpf('1.0')))
            f = numerator/(mpf('1.0')+f)
        else:                # Even terms e_{2*m}
            m = d/2
            numerator = m*(b-m)*x
            numerator = numerator/((a+(2*m)-mpf('1.0'))*(a+(2*m)))
            f = numerator/(mpf('1.0')+f)        

# An iterative version working backwards, using equations from 26.5.9.
def ibeta_cf_backwards2(a,b,x):
    f = mpf('0.0')  # running fraction value
    for e in range(100,0,-1):
        if e == 1: # First Term (last of iteration) 1/1+|
            mult = ((x**a)*((mpf('1.0')-x)**(b-mpf('1.0'))))/a
            mult = mult * gamma(a+b)
            mult = mult / (gamma(a) * gamma(b))    
            m=0
            return mult*mpf('1.0')/(mpf('1.0')+f)
        elif ((e % 2) == 1): # Odd terms d_n/1+|
            m = (e-1)/2
            numerator = m*(a+b+m-mpf('1.0'))*x
            numerator = numerator/((a+(2*m)-mpf('1.0'))* (a+(2*m)) * (mpf('1.0')-x))            
            f = numerator/(mpf('1.0')+f)
        else:                # Even terms d_{n+1}+|
            m = e/2
            numerator = (a+m-mpf('1.0'))*(b-m)*x
            numerator = -numerator/((a+(2*m)-mpf('2.0'))*(a+(2*m)-mpf('1.0'))*(mpf('1.0')-x))            
            f = numerator/(mpf('1.0')+f)
            
def ibeta(a,b,x):
    if (x == 0.0 or x==1.0):
        return x
    if x < ((a-1.0)/(a+b-2.0)):
        return ibeta_cf(0,a,b,x)
    else:
        return mpf(1.0)-ibeta_cf(0,b,a,mpf('1.0')-x)
        
def ibeta_backwards(a,b,x):
    if (x == 0.0 or x==1.0):
        return x 
    if x < ((a-1.0)/(a+b-2.0)):
        return ibeta_cf_backwards(a,b,x)
    else:
        return mpf(1.0)-ibeta_cf_backwards(b,a,mpf('1.0')-x)

def ibeta_backwards2(a,b,x):
    if (x == 0.0 or x==1.0):
        return x 
    if x < ((a-1.0)/(a+b-2.0)):
        return ibeta_cf_backwards2(a,b,x)
    else:
        return mpf(1.0)-ibeta_cf_backwards2(b,a,mpf('1.0')-x)

            
# Binomial CDF
def BCDF(n, k, p):
    return mpf('1.0') - ibeta(mpf(k+1),mpf(n-k),p)
    
# Binomial CDF
def BCDF_backwards(n, k, p):
    return mpf('1.0') - ibeta_backwards(mpf(k+1),mpf(n-k),p)

# Binomial CDF
def BCDF_backwards2(n, k, p):
    return mpf('1.0') - ibeta_backwards2(mpf(k+1),mpf(n-k),p)

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
    
    
# Find smallest k where B(n,k,p) > alpha
# using binary chop search
# Equivalent to Excel CRITBINOM function
def binomial_quantile_backwards(n, p, alpha):
    min = 0;
    max = n;
    mid = min + ((max-min) >> 1)
    keepgoing = True
    while (keepgoing):
        b = BCDF_backwards(n,mid,p)
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

# Find smallest k where B(n,k,p) > alpha
# using binary chop search
# Equivalent to Excel CRITBINOM function
def binomial_quantile_backwards2(n, p, alpha):
    min = 0;
    max = n;
    mid = min + ((max-min) >> 1)
    keepgoing = True
    while (keepgoing):
        b = BCDF_backwards2(n,mid,p)
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

