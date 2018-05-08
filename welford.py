#!/usr/bin/env python
import math
import sys

class welford():
    def __init__(self):
        self.n = 0
        self.mean = 0.0
        self.m2 = 0.0
        
    def update(self,x):
        self.n += 1
        delta = x - self.mean
        self.mean += delta/self.n
        delta2 = x - self.mean
        self.m2 += delta*delta2

    def results(self):
        pop_variance = self.m2/self.n
        pop_stddev = math.sqrt(self.m2/self.n)
        sample_variance = self.m2/(self.n-1)
        sample_stddev = math.sqrt(self.m2/(self.n-1))
        return (pop_variance,
                pop_stddev,
                sample_variance,
                sample_stddev,
                self.mean,
                self.n)

w = welford()

if sys.argv > 0:  # Get the filename
    filename = sys.argv[1]
    file = open(filename,"r")
else:
    file = sys.stdin
    
for line in file.readlines(): # process the file
    try:
        value = float(line)
        w.update(value)
    except:
        pass

# Get the results
(p_v, p_sd , s_v, s_sd, mean, n) = w.results()
if n < 2:
    print "Too few samples (%d) to compute standard deviation" % n
else:
    print "n                             : ", n
    print "Mean                          : ",mean
    print "Population Variance           : ",p_v
    print "Population Standard Deviation : ",p_sd
    print "Sample Variance               : ",s_v
    print "Sample Standard Deviation     : ",s_sd
  



