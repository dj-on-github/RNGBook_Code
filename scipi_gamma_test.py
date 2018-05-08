#!/usr/bin/env python

from scipy.special import gamma, gammainc, gammaincc
from scipy.special import gammaincc

def incomplete_lower_gamma(a,x):
    return gammainc(a,x) * gamma(a)

def incomplete_upper_gamma(a,x):
    return gammaincc(a,x) * gamma(a)


