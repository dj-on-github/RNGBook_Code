from mpmath import *
        
def xor_iterate64(n):
    mp.prec = 200
    oo2sf   = mpf(1)/mpf(2**64)
    oo2sfmo = mpf(1)/mpf((2**64)-1)
    ttt64   = mpf(2**64)
    ttt64m1 = mpf((2**64)-1)
    ttt64m2 = mpf((2**64)-2)
    
    p_input_0 = mpf(0)
    p_input_other = oo2sfmo
    
    p_pool_0 = p_input_0
    p_pool_other = p_input_other
    
    for i in xrange(n):
        p_0     = p_input_0 * p_pool_0
        p_0    += ttt64m1 * p_input_other * p_pool_other
        
        p_other  = p_input_0 * p_pool_other
        p_other += p_input_other * p_pool_0
        p_other += ttt64m2 * p_input_other * p_pool_other
        
        p_pool_0 = p_0
        p_pool_other = p_other
        difference = p_pool_0 – p_pool_other
    
        print “Iteration  %d” % (i+1)
        print “  P(0)    “,p_pool_0
        print “  P(Other)”,p_pool_other
        print “  Difference “,difference
        print

        