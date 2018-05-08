def update(v):
    v = 2*v
    if v > vref:
        output(1)
        v = v - vref
    else:
        output(0)
    
    return v

