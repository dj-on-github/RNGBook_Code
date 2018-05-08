#!/usr/bin/env python


from Crypto.PublicKey import RSA
key_pair = RSA.generate(2048)
p = key_pair.p
q = key_pair.q

M = p*q;

key_pair2 = RSA.generate(2048)
x = key_pair2.p

result = list()

for i in xrange(256):
    byte = 0
    for j in xrange(8):
        x = (x*x) % M
        byte = (byte << 1) | (x % 2)
    result.append(byte)

str = ""
for i,byte in enumerate(result):
    str += "%02x" % byte
    if (i>1) and (i % 16 == 0):
        print str
        str=""

