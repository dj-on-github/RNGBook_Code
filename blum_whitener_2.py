#!/usr/bin/env python

import random
import sys

# Tuple of (state number, output value, destination state,
#           destination probability, other destination state)
states = [0,(1, 0, 2, 0.4, 1),(2, 1, 3, 0.1, 1),(3,1,4,0.3,2),(4,0,3,0.2,4)]

state = 1
out_value = 0
out_string = ""
index = 0
count = 0
ic = 2**16  # input count

# State bits can be L, 0, 1, H or T.
# Initiatize all states to L
state_bits = ['L' for x in states]
i = 1
for j in xrange(ic):
    # Step 1
    s = ""
    for st in state_bits:
        s = s+str(st)
    if (state_bits[i] == 'H') or (state_bits[i] == 'T'):
        if (state_bits[i] == 'H'):
            out_value = out_value + (0x01 << index)
            index += 1
        elif (state_bits[i] == 'T'):
            index += 1
        state_bits[i] = 'L'
        count += 1
        if index == 8:
            out_string += "%02x" % out_value
            out_value = 0
            index = 0

        if len(out_string) == 64:
            print out_string
            out_string = ""

    # Step 2
    # Run the Markov Chain one step to get 1 or 0
    (s,ov,dest1,dest_prob1,dest2) = states[i]

    if random.SystemRandom().random() < dest_prob1:
        next_state = dest1
    else:
        next_state = dest2
    (s,ov,dest1,dest_prob2,dest2) = states[next_state]

    exit_bit = ov

    # Step 3
    s = str(state_bits[i])

    if state_bits[i] == 'L':
        state_bits[i] = exit_bit
    elif (state_bits[i] == 0) or (state_bits[i] == 1):
        if exit_bit == state_bits[i]:
            state_bits[i] = 'L'
        else:
            if state_bits[i] == 1 and exit_bit == 0:
                state_bits[i] = 'H'
            else:
                state_bits[i] = 'T'
    # Step 4
    i = next_state

print >> sys.stderr,  "Bits in:",ic,", Bits out:",count," Ratio:",(float(count)/ic)


