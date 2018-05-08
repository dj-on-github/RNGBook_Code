from mpmath import mpf
import mpmath as mp
 

def xor_iterate_fips(bits=16, iterations=16):
    mp.prec = 200
    oo2s   = mpf(1)/mpf(2**bits)
    oo2smo = mpf(1)/mpf((2**bits)-1)
    ttt16   = mpf(2**bits)
    ttt16m1 = mpf((2**bits)-1)
    ttt16m2 = mpf((2**bits)-2)
    
    # fetch the first random number to initialize the comparison value
    # as per FIPS 140-2 4.9.2
    rt = random_things(bits)

    therand = rt.rand16()    
    mask = (2**bits)-1
    lastrand = therand & mask
    
    # initial the input probabilities. The lastrand gets 0
    # others get 1/(2^16 -1)
    p_input = list()
    next_p = list()
    p_pool = list()
    for i in xrange(2**bits):
        p_input.append(0)
        p_pool.append(oo2smo)
        next_p.append(0)
    p_pool[lastrand] = 0
    
    print "Initial rand = %X" % lastrand
    
    for i in xrange(iterations):
        therand = rt.rand16() # lastrand will not occur
        mask = (2**bits)-1
        therand = therand & mask
        
        # fill in the input distribution
        for j in xrange(2**bits):
            p_input[j] = oo2smo
            next_p[j]=0
        p_input[lastrand] = 0
        
        for a in xrange(2**bits):
            for b in xrange(2**bits):
                axorb = a ^ b
                p_axorb = p_input[a] * p_pool[b]
                next_p[axorb] += p_axorb
                
        lastrand = therand
        
        for j in xrange(2**bits):
            p_pool[j] = next_p[j]
        
        print "Iteration  %d - random# = %X" % (i+1, lastrand)
        print "  minP    ",min(p_pool)
        print "  maxP    ",max(p_pool)
        print "  Difference ",(max(p_pool)-min(p_pool))
        print

xor_iterate_fips()
        
        