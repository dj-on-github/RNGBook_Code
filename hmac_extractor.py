#!/usr/bin/env python

import hmac
import hashlib
import base64
import sys

# get filename
filename = sys.argv[1]
key = sys.argv[2]

with open(filename,"rb") as f:
    bytes = f.read(128) # Read 1024 bits
    while len(bytes) == 128:
        digest = hmac.new(key, msg=bytes, digestmod=hashlib.sha256).digest()
        astr = ""
        for byte in digest:
            astr += "%02X" % ord(byte)
        print astr
        bytes = f.read(128)
f.close()

