#!/usr/bin/env python

import random

# Tuple of (state number, output value, destination state,
#           destination probability, other destination state)
states = [0,(1, 0, 2, 0.4, 1),(2, 1, 3, 0.1, 1),(3,1,4,0.3,2),(4,0,3,0.2,4)]

state = 1
out_value = 0
out_string = ""
index = 0

for i in xrange(4096):
    (s,ov,dest1,dest_prob,dest2) = states[state]
    if ov == 1:
        out_value = out_value + (0x01 << index)
    index += 1

    if index == 8:
        out_string += "%02x" % out_value
        out_value = 0
        index = 0

    if len(out_string) == 64:
        print out_string
        out_string = ""

    if random.SystemRandom().random() < dest_prob:
        state = dest1
    else:
        state = dest2
  
