#!/usr/bin/env python

import random

def non_random_table(size, type="add"):
    # Header
    header = list()
    header.append("  ")
    
    # The Header
    for i in xrange(size):
        header.append("%02d" % (i))

    # The list of lists. Each list a row.
    # Add the header.
    # bodyy is a list of lists of bodyx.

    bodyy=list()
    for i in xrange(size):
        bodyx = list()
        bodyx.append("%02d" % (i)) # The row index
        bodyy.append(bodyx)

    # Fill in the rows
    for y in xrange(size):
        for x in xrange(size):
            #bodyy[y].append(nonrandomfunction(x,y,size))
            if type=="add":
                bodyy[y].append("%02d" % (x+y))
            elif type=="multiply":
                bodyy[y].append("%02d" % (x*y))
            elif type=="random":
                bodyy[y].append("%02d" % random.randrange(size*size))

    # Convert to latex text
    # Header
    tabletext = " & ".join(header) + "\\\\ \\hline\n"

    # Rows
    for row in bodyy:
        rowtext = " & ".join(row)
        tabletext += rowtext+ "\\\\\n"
    return tabletext

table = non_random_table(10,"add")
print table


table = non_random_table(10,"multiply")
print table

table = non_random_table(10,"random")
print table

print

