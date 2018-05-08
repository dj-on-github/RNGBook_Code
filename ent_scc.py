def ent_scc(values):
    # Initialize
    first = True
    t1 = 0.0
    t2 = 0.0
    t3 = 0.0
    n = 0
    for value in values:
        n += 1
        
        if first:  # Store first value as u0
            first = False
            last = 0
            u0 = value
        else:
            t1 = t1 + last * value
        
        t2 = t2 + value
        t3 = t3 + value**2
        last = value
    
    # last cycle wrap around
    t1 = t1 + last*u0
        
    # Now compute the SCC from the counters
    scc = (n * t1 - (t3*t3))/(n * t2 - (t3*t3))

    return scc

