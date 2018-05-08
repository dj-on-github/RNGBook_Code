#!/usr/bin/env python

import math
import gmpy2
from gmpy2 import mpfr
import matplotlib
import matplotlib.pyplot as plt

from incomplete_beta import *
from binomial_quantile import *

#BCDF(n, k, p): # binomial CDF
#binomial_quantile(n, p, alpha): # Binomial Quantile

n = 32
p = 0.6

xs = range(n+1)
ys = [BCDF(n,x,p) for x in xs]

plt.plot(xs,ys,"o")
plt.ylabel("binom_cdf(n={},p={}".format(n,p))
plt.xlabel("k")
plt.xlim([0,32])
plt.grid(True)

plt.savefig('../img/binomial_cdf.pdf')


