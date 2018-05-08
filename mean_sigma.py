#!/usr/bin/env python
import math
import sys

n = mean = m2 = 0

def welford(x):
    global n
    global mean
    global m2

    n += 1
    delta = x - mean
    mean += delta/n
    delta2 = x - mean
    m2 += delta*delta2

# get filename
if sys.argv > 0:
    filename = sys.argv[1]
    file = open(filename,"r")
else:
    file = sys.stdin

for line in file.readlines():
    try:
        value = float(line)
        welford(value)
    except:
        pass

if n < 2:
    print "Too vew samples to compute standard deviation"
    print "Mean = %f" % mean
else:
    print "Population Variance = %f" % (m2 / n)
    print "Population std dev  = %f" % math.sqrt(m2 / n)
    
    print "Sample     Variance = %f" % (m2 / (n-1))
    print "Sample     std dev  = %f" % math.sqrt(m2 / (n-1))
    print "Mean                = %f" % mean

file.close()

