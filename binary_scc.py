def binary_scc(bits):
    # Initialize
    t1 = 0
    t2 = 0
    n = 0
    first = True
    for bit in bits:
        n = n+1
        if first:  # Skip first bit, we need 2 bits
            first = False
        else:
            if (last==1) and (bit==1) t1 += 1
            if (last==1) t2 = t2+1
        last = value
    
    # Now compute the SCC from the counters
    n = n-1 # Reduce n because we are not wrapping
    scc = (n*t1 - t2*t2)/(n*t2 - t2*t2)

    return scc

