def gmul(a, b):
    poly = 0x001b # 0x201b with the msb lopped off.
    degree = 13
   
    z = 0
    if a & 1:
        r = b
    else:
        r = 0
    for i in xrange(1,degree+1):
        if  (b & (1 << (degree-1))) == 0:
            b = z ^ ((b << 1) & ((1 << degree) - 1))
        else:
            b = poly ^ ((b << 1) & ((1 << degree) - 1))
        if a & (1 << i):
            r = r ^ b
        else:
            r = r ^ z
    return r

def gadd(a, b):
    return a^b

def biw(a,b,c):
    return gadd(gmul(a,b),c)

