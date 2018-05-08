#!/usr/bin/env python

import sys
import random
import math

kn=[0 for x in xrange(128)] # The three lookup tables
wn=[0 for x in xrange(128)]
fn=[0 for x in xrange(128)]

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

print "Writing kn file"
f = open('../data_files/ziggurat_kn.dat','w')
for i in xrange(1,len(kn)):
    thestring = str(i)+" "+str(kn[i])+"\n"
    f.write(thestring)
f.close()

f = open('../data_files/ziggurat_wn.dat','w')    
print "Writing wn file"
for i in xrange(len(wn)):
    thestring = str(i)+" "+str(wn[i])+"\n"
    f.write(thestring)
f.close()
    
f = open('../data_files/ziggurat_fn.dat','w')    
print "Writing fn file"
for i in xrange(len(fn)):
    thestring = str(i)+" "+str(fn[i])+"\n"
    f.write(thestring)
f.close()
    
