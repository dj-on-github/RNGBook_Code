#!/usr/bin/env python

import sys

def von_neumann_debiaser(bits):
    result = list()
    l = len(bits)/2
    for i in xrange(l):
        twobits = bits[l*2:(l*2+1)]
        if twobits = [0,1]:
            result.append(1)
        elif twobits = [1,0]:
            result.append(0)
    return result

def yuval_peres_debiser(bits,depth):
    if len(bits) < 2:
        return list()

    if depth==1:
        return von_neumann_debiaser(bits)

    l = len(bits)/2

    # The first part
    first = von_neumann_debiaser(bits)

    u = list()  # The second part
    for i in xrange(l):
        u.append(bits[2*i] ^ bits[(2*i)+1])
    second = yuval_peres_debiaser(u,depth-1)
    
    v = list() # The third part
    for i in xrange(l):
        if bits[2*i] == bits[(2*i)+1]:
            v.append(bits[2*i])
    third = yuval_perez_debiaser(v,depth-1)

    return first+second+third
    
# get depth
depth = int(sys.argv[1])

# get filename
filename = sys.argv[2]
outfilename = sys.argv[3]

outf = open(outfilename,"wb")

outbitlist = list()
outbytelist = list()

with open(filename,"rb") as f:
    bytes = f.read(1024) # Read a chunk of bytes
    bitstr = list()
    while bytes:
        for byte in bytes:
            # convert to bit string
            for i in xrange(8):
                bit = (byte >> i) & 0x01
                bitstr.append(bit)

        outbitlist = outbitlist + yuval_peres_debiaser(bitstr,depth)


        while len(outbitlist) > 7: # We have 8 or more bits so:
            outbyte = 0
            bits = outbitlist[:8]  # Pull 8 bits off the front
            outbitlist = outbitlist[8:]
            for i in xrange(8):       # Turn them into a byte
                outbyte = outbyte << 1
                outbyte = outbyte + bits[7-i] 
            outbytelist.append(outbyte) # add it to the output

        while len(outbytelist) > 1024: # Write out in chunks
            data = bytearray(outbytelist)
            outf.write(data)
            outbytelist = list() 
            
        bytes = f.read(1024) # Read in the next chunk

# The last line
data = bytearray(outbytelist)
outf.write(data)

f.close()
outf.close()

