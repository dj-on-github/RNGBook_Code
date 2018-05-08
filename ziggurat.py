#!/usr/bin/env python

import sys
import random
import math

rand = random.SystemRandom() # nondeterministic random source
num = int(sys.argv[1])  # Number of random numbers

kn=[0 for x in xrange(128)] # The three lookup tables
wn=[0 for x in xrange(128)]
fn=[0 for x in xrange(128)]

def ziggurat_normal():
    global kn
    global wn
    global fn
    
    hz = rand.randrange(-2**31,(2**31)-1)
    iz = hz & 127
    
    if (abs(hz)<kn[iz]): # Initial attempt
        return hz*wn[iz]
    else: # Fallback Algorithm called about 1% of times
        r = 3.442620;
        x=0.0
        y=0.0

        while True:
            x=float(hz)*wn[iz]

            if (iz==0):
                while True:
                    x=-math.log(rand.uniform(0,1.0))*0.2904764
                    y=-math.log(rand.uniform(0,1.0))
                    if ((y+y)<(x*x)):
                        break
                return (r+x)*((int(hz>0)*2)-1)

            if (fn[iz]+(rand.uniform(0,1.0))*(fn[iz-1]-fn[iz])
                                      < math.exp(-.5*x*x)):
                return x

            hz=random.getrandbits(32)
            iz=hz&127
            if(abs(hz)<kn[iz]):
                return (hz*wn[iz])


# Create tables
def build_tables():
    global kn
    global wn
    global fn
    m1 = 2147483648.0
    m2 = 4294967296.0
    dn=3.442619855899
    tn=dn
    vn=9.91256303526217e-3

    # Build the tables kn, wn, fn
    q=vn/math.exp(-.5*dn*dn)
    kn[0]=(dn/q)*m1
    kn[1]=0
    wn[0]=q/m1
    wn[127]=dn/m1
    fn[0]=1.0
    fn[127]=math.exp(-.5*dn*dn)
    
    for i in xrange(126,0,-1):
        dn=math.sqrt(-2.*math.log(vn/dn+math.exp(-.5*dn*dn)));
        kn[i+1]=int((dn/tn)*m1);
        tn=dn;
        fn[i]=math.exp(-.5*dn*dn);
        wn[i]=dn/m1;

build_tables()
for i in xrange(num):
    print ziggurat_normal()

