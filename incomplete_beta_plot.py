#!/usr/bin/env python

import math 
from mpmath import *
import matplotlib
import matplotlib.pyplot as plt
import time
from beta_functions import *

PRECISION = 300
mp.dps = PRECISION
    
# Make a plot
xl = [x*mpf('0.001') for x in range(1001)]
 
plt.plot(xl,[ibeta(mpf('0.5'),mpf('6.0'),x) for x in xl],"--")
plt.text(0.0, .85, r'$I_x(0.5,6)$')
plt.plot(xl,[ibeta(mpf('6.0'),mpf('0.5'),x) for x in xl],"--")
plt.text(0.6, 0.08, r'$I_x(6,0.5)$')
plt.plot(xl,[ibeta(mpf('7.0'),mpf('7.0'),x) for x in xl],"--")
plt.text(0.36, 0.4, r'$I_x(7,7)$')
plt.plot(xl,[ibeta(mpf('1.0'),mpf('2.0'),x) for x in xl],"--")
plt.text(0.3, 0.66, r'$I_x(1,2)$')
plt.plot(xl,[ibeta(mpf('2.0'),mpf('1.0'),x) for x in xl],"--")
plt.text(0.7, 0.65, r'$I_x(2,1)$')
plt.ylabel("Ix(a,b)")
plt.xlabel("x")
plt.grid(True)
plt.savefig('../img/incomplete_beta_plot.pdf')
