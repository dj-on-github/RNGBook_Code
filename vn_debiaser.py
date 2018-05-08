#!/usr/bin/env python

import sys

pattern_table=[ 0x0,0x1,0x0,0x0,0x1,0x3,0x1,0x1,0x0,0x2,0x0,0x0,0x0,0x1,0x0,0x0,
                0x1,0x3,0x1,0x1,0x3,0x7,0x3,0x3,0x1,0x5,0x1,0x1,0x1,0x3,0x1,0x1,
                0x0,0x2,0x0,0x0,0x2,0x6,0x2,0x2,0x0,0x4,0x0,0x0,0x0,0x2,0x0,0x0,
                0x0,0x1,0x0,0x0,0x1,0x3,0x1,0x1,0x0,0x2,0x0,0x0,0x0,0x1,0x0,0x0,
                0x1,0x3,0x1,0x1,0x3,0x7,0x3,0x3,0x1,0x5,0x1,0x1,0x1,0x3,0x1,0x1,
                0x3,0x7,0x3,0x3,0x7,0xf,0x7,0x7,0x3,0xb,0x3,0x3,0x3,0x7,0x3,0x3,
                0x1,0x5,0x1,0x1,0x5,0xd,0x5,0x5,0x1,0x9,0x1,0x1,0x1,0x5,0x1,0x1,
                0x1,0x3,0x1,0x1,0x3,0x7,0x3,0x3,0x1,0x5,0x1,0x1,0x1,0x3,0x1,0x1,
                0x0,0x2,0x0,0x0,0x2,0x6,0x2,0x2,0x0,0x4,0x0,0x0,0x0,0x2,0x0,0x0,
                0x2,0x6,0x2,0x2,0x6,0xe,0x6,0x6,0x2,0xa,0x2,0x2,0x2,0x6,0x2,0x2,
                0x0,0x4,0x0,0x0,0x4,0xc,0x4,0x4,0x0,0x8,0x0,0x0,0x0,0x4,0x0,0x0,
                0x0,0x2,0x0,0x0,0x2,0x6,0x2,0x2,0x0,0x4,0x0,0x0,0x0,0x2,0x0,0x0,
                0x0,0x1,0x0,0x0,0x1,0x3,0x1,0x1,0x0,0x2,0x0,0x0,0x0,0x1,0x0,0x0,
                0x1,0x3,0x1,0x1,0x3,0x7,0x3,0x3,0x1,0x5,0x1,0x1,0x1,0x3,0x1,0x1,
                0x0,0x2,0x0,0x0,0x2,0x6,0x2,0x2,0x0,0x4,0x0,0x0,0x0,0x2,0x0,0x0,
                0x0,0x1,0x0,0x0,0x1,0x3,0x1,0x1,0x0,0x2,0x0,0x0,0x0,0x1,0x0,0x0]

count_table = [ 0,1,1,0,1,2,2,1,1,2,2,1,0,1,1,0,
                1,2,2,1,2,3,3,2,2,3,3,2,1,2,2,1,
                1,2,2,1,2,3,3,2,2,3,3,2,1,2,2,1,
                0,1,1,0,1,2,2,1,1,2,2,1,0,1,1,0,
                1,2,2,1,2,3,3,2,2,3,3,2,1,2,2,1,
                2,3,3,2,3,4,4,3,3,4,4,3,2,3,3,2,
                2,3,3,2,3,4,4,3,3,4,4,3,2,3,3,2,
                1,2,2,1,2,3,3,2,2,3,3,2,1,2,2,1,
                1,2,2,1,2,3,3,2,2,3,3,2,1,2,2,1,
                2,3,3,2,3,4,4,3,3,4,4,3,2,3,3,2,
                2,3,3,2,3,4,4,3,3,4,4,3,2,3,3,2,
                1,2,2,1,2,3,3,2,2,3,3,2,1,2,2,1,
                0,1,1,0,1,2,2,1,1,2,2,1,0,1,1,0,
                1,2,2,1,2,3,3,2,2,3,3,2,1,2,2,1,
                1,2,2,1,2,3,3,2,2,3,3,2,1,2,2,1,
                0,1,1,0,1,2,2,1,1,2,2,1,0,1,1,0]

# get filename
filename = sys.argv[1]
outfilename = sys.argv[2]

outbitlist = list()
outbytelist = list()

outf = open(outfilename,"wb")

with open(filename,"rb") as f:
    bytes = f.read(256) # Read a chunk of bytes
    while bytes:
        for byte in bytes: # VN Debiaser table lookup
            pattern = pattern_table[ord(byte)]
            count = count_table[ord(byte)]
            if count > 0:
                for i in range(count):
                    bit = ((pattern >> i) & 0x01)
                    outbitlist.append(bit)
        
        while len(outbitlist) > 7: # We have 8 or more bits so:
            outbyte = 0
            bits = outbitlist[:8]  # Pull 8 bits off the front
            outbitlist = outbitlist[8:]
            for bit in bits:        # Turn them into a byte
                outbyte = outbyte << 1
                outbyte = outbyte + bit 
            outbytelist.append(outbyte) # add it to the output

        while len(outbytelist) > 256: # Write out in chunks
            data = bytearray(outbytelist)
            outf.write(data)
            outbytelist = list() 
            
        bytes = f.read(256) # Read in the next 32
# The last line
data = bytearray(outbytelist)
outf.write(data)

f.close()
outf.close()

