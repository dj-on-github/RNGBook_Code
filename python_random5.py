#!/usr/bin/env python
import os

k = 0
bytes = os.urandom(16)
for byte in bytes:
    k = (k << 8) + ord(byte)
print "%032x" %  k

