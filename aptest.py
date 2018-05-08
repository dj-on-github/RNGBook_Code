#!/usr/bin/env python

import argparse
parser = argparse.ArgumentParser(description='Random Excursion Variant Test.')
parser.add_argument('filename', type=str, nargs='?', help='Filename of binary file to test')
parser.add_argument('--be', action='store_false',help='Treat data as big endian bits within bytes')
args = parser.parse_args()

print args.filename
print args.be

