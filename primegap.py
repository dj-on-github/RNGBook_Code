#!/usr/bin/python

import math

x = 2**1024
xmo = x -1

gap = (x * int(math.log(x))) - (xmo * int(math.log(xmo)))

print gap

