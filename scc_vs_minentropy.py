#!/usr/bin/env python

import math
import matplotlib
import matplotlib.pyplot as plt

def scc2me(scc):
    p = (scc/2.0)+0.5
    p = max(p,1-p)
    h = -math.log(p,2) 
    return h

sccs = [(x-100)*0.01 for x in range(0,201)]
ys = [scc2me(scc) for scc in sccs]

plt.plot(sccs, ys)
plt.xlim([-1,1])
plt.ylim([0,1])
plt.grid(True)
plt.xlabel("Serial Correlation Coefficient")
plt.ylabel("Min Entropy Per Bit")

plt.savefig("../img/scc_vs_minentropy.pdf",format='pdf')

