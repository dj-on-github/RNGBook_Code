#!/usr/bin/env python2

import sys

# Use - py lagn_space_pattern.py <bit reverse length> <LagN spacing>

# Perform the bit reversal
def permute(original,reverse_len):
    permutedlist = list()
    blocks = len(original)-(len(original) % reverse_len)
    for i in xrange(blocks):  # Cut the list into blocks to reverse
        bits = original[(i*reverse_len):((i+1)*reverse_len)]
        revblock = list()
        for bit in bits: # Reverse the bits in the block
            revblock.insert(0,bit) 
        permutedlist = permutedlist+revblock # Add them to the output
    return permutedlist

# Set up dict and the original bit series series.
# Dict contains a bit index and the next bit index in the series.
# The original list is a list with the original series indexes.
reverse_len = int(sys.argv[1])
lagmax = int(sys.argv[2])

outarray = list()

for lag in xrange(1,lagmax+1):
    outcolumn = list()
    # Make the list long enough.
    chainlen = (reverse_len+lag)*4
    chain = dict()
    original = list()
    # Build the chain
    for i in xrange(chainlen):
        chain[i]=i+1
        original.append(i)

    # Do the bit reversal
    permutedlist = permute(original,reverse_len)


    # Take each pair and count the spacing.
    for i in xrange(len(permutedlist)-lag):
        #take pair from permuted list
        first = permutedlist[i]
        second = permutedlist[i+lag]
        #Sort
        if first > second:
            first,second = second,first
            
        #Follow Dict and count
        count = 0
        next = first
        while (next != second):
            next = chain[next]
            count += 1
            
        #report the count
        outcolumn.append(count)
    outarray.append(outcolumn)
    
print " Step Distance --->"
for i,row in enumerate(outarray):
    astr = [str(x).ljust(2)+" " for x in row]
    print str(i+1).ljust(3) + ": "+ ','.join(astr)[:120]
    