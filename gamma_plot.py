#!/usr/bin/env python

import math
from math import gamma, sqrt
import gamma_functions as g

e = math.e
print e

x = 1.0

f = open("../data_files/gamma_plot.dat","w")
f.write("a gamma(a) igamma(a,x=1.0)\n")

for a in [0.1*i for i in range(1,41)]:
    print a
    y = math.gamma(a)
    y2 = g.lower_incomplete_gamma(a,x) 
    y3 = y2/y
    f.write("{} {} {} {}\n".format(a,y,y2,y3))

