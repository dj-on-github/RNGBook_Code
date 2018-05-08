#!/usr/bin/env python

import sys
import math
import matplotlib
import matplotlib.pyplot as plt

def binom_pmf(n,p):
    xs = range(n+1)
    ys = [(math.factorial(n)/(math.factorial(k)*math.factorial(n-k))) \
          *(p**k) \
          *((1-p)**(n-k)) for k in range(n+1) ]
    return xs,ys

n = int(sys.argv[1])
p = float(sys.argv[2])
if len(sys.argv) > 3:
    xlimit = int(sys.argv[3])
    plt.xlim([0,xlimit])

xs,ys = binom_pmf(n,p)

plt.plot(xs,ys,"o")
plt.ylabel("binom_pmf(n={},p={}".format(n,p))
plt.xlabel("k")
plt.grid(True)
plt.savefig('../img/binomial_pmf.pdf')

