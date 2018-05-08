#!/usr/bin/python

def makefloat(s,e,m):
    sign = (-1)**s

    mantissa = m * (2.0**(-52));
    if e!=0:
        mantissa = mantissa + 1;

    if e==0:
        exponent = -1022
    else:
        exponent = e-1023

    value = sign * mantissa * (2.0**exponent)

    return value

es = [1021,1022,1023,1024,1025,1026]

lowend = 0
highend = 0x0fffffffffffff
for e in es:
    smallest = makefloat(0,e,lowend)
    largest = makefloat(0,e,highend)

    print("e = %d, from : %f   to  %f, range %f" % (e,smallest,largest,largest-smallest))

print()

es = [0,1,2,3]
for e in es:
    smallest = makefloat(0,e,lowend)
    largest = makefloat(0,e,highend)

    print("e = %d, from : %0.50f   to  %0.50f, range %0.50f" % (e,smallest,largest,largest-smallest))
