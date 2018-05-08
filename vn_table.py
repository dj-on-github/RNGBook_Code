#!/usr/bin/env python

count_table = [0 for x in xrange(256)]
pattern_table = [0 for x in xrange(256)]

for i in xrange(256):
    abyte = i
    count = 0
    pattern = 0
    for j in xrange(4):
        pair = abyte & 0x03
        abyte = abyte >> 2
        if (pair == 1):   # 01 case
            pattern = (pattern << 1) | 0x01
            count = count + 1
        elif (pair == 2):   # 10 case
            pattern = pattern << 1
            count = count + 1
    count_table[i] = count
    pattern_table[i] = pattern

print "Pattern Table"
for y in xrange(16):
    line = pattern_table[y*16:(y*16)+16]
    linelist = [("0x%02x" % x) for x in line]
    #for x in line:
    #    linelist.append("0x%02x" % x)
    line = ",".join(linelist)
    print line

print "Count Table"
for y in xrange(16):
    line = count_table[y*16:(y*16)+16]
    linelist = [("%d" % x) for x in line]
    line = ",".join(linelist)
    print line

