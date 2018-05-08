#!/usr/bin/env python

import sys
import random
randsource = random.SystemRandom() # nondeterministic random source

iterations = int(sys.argv[1])  # Number of throws
number_of_dice = int(sys.argv[2])   # Number of dice each throw

bins = [0 for _ in range((number_of_dice*6)+3)]  # Roll the dice
for i in xrange(iterations):
    throw=0
    for j in xrange(number_of_dice):
        throw = throw + randsource.randint(1,6)
    bins[throw] +=1
    
print "x y" # Print the header

max=0           # Find the maximum so we can normalize it
for f in bins:
    if f > max:
        max = f

for i in xrange(0,(6*number_of_dice)+3): #Print out the histogram
    print "%d %f" % (i, float(bins[i])/float(max))     
    
