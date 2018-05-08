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
p = 0.4
alpha = 0.67

xs = range(n+1)
ys = [BCDF(n,x,p) for x in xs]

k = binomial_quantile(n,p,alpha)
ky = BCDF(n,k,p)

plt.plot(xs,ys,"o")
plt.ylabel("binom_cdf(n={},p={}".format(n,p))
plt.xlabel("k")
plt.xlim([0,32])
plt.grid(True)
plt.annotate("alpha = {}".format(alpha), xy=(0, alpha), xytext=(5, 0.8),
            arrowprops=dict(facecolor='black', shrink=0.05))

plt.plot([0,13.4], [alpha,alpha], 'k--', lw=1)

plt.plot([13.4, 13.4], [alpha,0], 'k--', lw=1)
plt.annotate('Quantile, next highest integer k=14', xy=(14, 0), xytext=(15, 0.2),
            arrowprops=dict(facecolor='black', shrink=0.05))

plt.savefig('../img/binomial_quantile.pdf')


