#!/usr/bin/env python

def lagn_scc(scc,n):
    # Initialize
    lagns=list()
    probs = list()
    probs.append(1.0) # Lag-0 Correlation == 1
    lagns.append(1.0) 
    lag1prob = (scc/2.0)+0.5
    
    for i in xrange(1,n):
        prob = (lag1prob * probs[i-1]) + ((1-lag1prob)*(1-probs[i-1])) 
        probs.append(prob)
        # convert from probability to correlation coef  
        lagns.append((prob-0.5)*2.0)
        
    return lagns, probs

print "#n  lagn_cc     bias"
lagns,probs = lagn_scc(scc=-0.7,n=16)
for i in xrange(len(lagns)):
    print "%02d  %1.8f  %1.8f" % (i,lagns[i],probs[i])
    
