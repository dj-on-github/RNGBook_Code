#!/usr/bin/env python

import random

class pcg():
    def __init__(self,algorithm="LCG_RS", size=64, outsize=32, seed=None, randomize=True):

        # Trim the seed to the state size
        seedmask = 
        if seed != None:
            self.seed = seed & ((1 << size)-1)

        # 

        if algorithm = "PCG_LCG_RS_16_8"

        if seed != None:
            self.state = seed

        if randomize:
            
    def pcg_lcg_xsh_rs_16_8(seed):
        state = seed



