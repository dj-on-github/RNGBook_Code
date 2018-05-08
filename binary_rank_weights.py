#!/usr/bin/env python


print "M   Q   Pi_1           Pi_2           Pi_3"

for x in range(3,65):
    M = x
    Q = x

    r = M
    outside = 2.0 ** ((r*(Q+M-r)) -M*Q)
    mult = 1.0
    for i in range(0,r):
        mult = mult * (1.0 - (2.0**(i-Q))) * (1-2.0**(i-M)) 
        mult = mult / (1-2.0**(i-r))

    prob_m = outside * mult

    #print ("M = %d" % M).ljust(7) + ("Q = %d" % Q).ljust(7) + "P_M = ",prob

    r = M-1
    outside = 2.0 ** ((r*(Q+M-r)) -M*Q)
    mult = 1.0
    for i in range(0,r):
        mult = mult * (1.0 - (2.0**(i-Q))) * (1-2.0**(i-M)) 
        mult = mult / (1-2.0**(i-r))

    prob_mm = outside * mult

    prob_remain = 1.0 - prob_m - prob_mm

    print str(M).ljust(4) + str(Q).ljust(4) + str(prob_m).ljust(15) + str(prob_mm).ljust(15) + str(prob_remain).ljust(15)


        
