#!/usr/bin/env python

import sys
import random
import math

rand = random.SystemRandom() # nondeterministic random source
num = int(sys.argv[1])  # Number of random numbers

kn=[0 for x in xrange(128)] # The three lookup tables
wn=[0 for x in xrange(128)]
fn=[0 for x in xrange(128)]

//static double DRanNormalTail(double dMin, int iNegative) {
//    double x, y;
//    do
//    {   x = log(DRanU()) / dMin;
//        y = log(DRanU());
//    } while (-2 * y < x * x);
//
//    return iNegative ? x - dMin : dMin - x;
//}



#define ZIGNOR_C 128 /* number of blocks */
#define ZIGNOR_R 3.442619855899 /* start of the right tail */
                   /* (R * phi(R) + Pr(X>=R)) * sqrt(2\pi) */
#define ZIGNOR_V 9.91256303526217e-3

#/* s_adZigX holds coordinates, such that each rectangle has*/
#/* same area; s_adZigR holds s_adZigX[i + 1] / s_adZigX[i] */
#static double s_adZigX[ZIGNOR_C + 1], s_adZigR[ZIGNOR_C];


ZIGNOR_C = 128
ZIGNOR_R = 3.442619855899
ZIGNOR_V = 9.91256303526217e-3 #(R * phi(R) + Pr(X>=R)) * sqrt(2\pi)
s_adZigX = [0.0 for x in xrange(ZIGNOR_C + 1)]
s_adZigR = [0.0 for x in xrange(ZIGNOR_C)]

def DRanU():
    return rand.uniform(0,1.0)

def IRanU():
    return rand.randrange(-(2**31),(2**31)-1)
    
def DranNormalTail(dMin, iNegative):
    while True:
        x = math.log(DRanU())/dMin
        y = math.log(DRanU())
        if (-2 * y < x * x):
            break
    if iNegative:
        return x-dMin
    else:
        return dMin-x
        
def zigNorInit(iC, dR, dV):
    global ZIGNOR_C
    global ZIGNOR_R
    global ZIGNOR_V
    global s_adZigX
    global s_adZigR

    f = math.exp(-0.5 * dR * dR)
    s_adZigX[0] = dV / f # [0] is bottom block: V / f(R)
    s_adZigX[1] = dR
    s_adZigX[iC] = 0

    for i in xrange(2,iC):
        s_adZigX[i] = math.sqrt(-2 * math.log(dV / s_adZigX[i - 1] + f))
        f = math.exp(-0.5 * s_adZigX[i] * s_adZigX[i])
    
    for i in xrange(2,iC):
        s_adZigR[i] = s_adZigX[i + 1] / s_adZigX[i];

def DRanNormalZig():
    global ZIGNOR_C
    global ZIGNOR_R
    global ZIGNOR_V
    global s_adZigX
    global s_adZigR
    
    while True:
        u = 2.0 * DRanU() - 1.0
        i = IRanU() & 0x7F
        
        #first try the rectangular boxes
        if (fabs(u) < s_adZigR[i]):
            return u * s_adZigX[i]
            
        #bottom box: sample from the tail
        if (i == 0):
            return DRanNormalTail(ZIGNOR_R, u < 0):
        
        # is this a sample from the wedges?
        x = u * s_adZigX[i]
        f0 = math.exp(-0.5 * (s_adZigX[i] * s_adZigX[i] - x * x))
        f1 = math.exp(-0.5 * (s_adZigX[i+1] * s_adZigX[i+1] - x * x))
        
        if (f1 + DRanU() * (f0 - f1) < 1.0):
            return x;   
            
                 
#static void zigNorInit(int iC, double dR, double dV) {
#    int i; double f;
#    f = exp(-0.5 * dR * dR);
#    s_adZigX[0] = dV / f; /* [0] is bottom block: V / f(R) */
#    s_adZigX[1] = dR;
#    s_adZigX[iC] = 0;
#
#    for (i = 2; i < iC; ++i) {
#        s_adZigX[i] = sqrt(-2 * log(dV / s_adZigX[i - 1] + f));
#        f = exp(-0.5 * s_adZigX[i] * s_adZigX[i]);
#    }
#    for (i = 0; i < iC; ++i)
#        s_adZigR[i] = s_adZigX[i + 1] / s_adZigX[i];
#}



#double DRanNormalZig(void) {
#    unsigned int i;
#    double x, u, f0, f1;      
#    for (;;) {
#        u = 2 * DRanU() - 1;
#        i = IRanU() & 0x7F;
#        /* first try the rectangular boxes */
#        if (fabs(u) < s_adZigR[i])
#            return u * s_adZigX[i];
#        /* bottom box: sample from the tail */
#        if (i == 0)
#            return DRanNormalTail(ZIGNOR_R, u < 0);
#        /* is this a sample from the wedges? */
#        x = u * s_adZigX[i];
#        f0 = exp(-0.5 * (s_adZigX[i] * s_adZigX[i] - x * x) );
#        f1 = exp(-0.5 * (s_adZigX[i+1] * s_adZigX[i+1] - x * x) );
#        if (f1 + DRanU() * (f0 - f1) < 1.0) return x;
#    }
#}  



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

