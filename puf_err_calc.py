#!/usr/bin/env python

from scipy.stats import binom
import sys

array_size = int(sys.argv[1]) # Input array size from command line

errs = [0.1,0.3,0.5,0.7,1,2,3,4,5,10,15,20,25,30,35,40] # Percentage errors
str = ','.join(("%4.1f"%float(x))+"%" for x in errs) # Format the table header
print("       "+str)

for yield_loss_power in xrange(2,15):  # Yield loss from 10^-2 to 10^-15
    str = ("10^-%d" % yield_loss_power).ljust(6)
    for err in errs:
        perr = float(err)/100.0
        bits = binom.ppf(q=(1.0-(10.0**(-yield_loss_power))),n=array_size,p=perr)
        str = str + ","+("%5d" % bits)
    print(str)



