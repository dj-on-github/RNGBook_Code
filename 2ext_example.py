#!/usr/bin/env python

import gf2 as gf
import copy
import sys
              
A = list()
# Create A_1, an identity matrix
A.append(gf.make_identity_matrix(size=256))

# Compute basis element list x_i  
basis = gf.moarrrr_power_to_the_alpha(2, degree=256, length=256)

# Create the matrices
for x in range(1,256):
    # compute A_{i+1}
    matrix = copy.deepcopy(A[x-1]) # copy A_{x-1}
    gf.rotate_right_matrix(matrix) # Shift ot right
    
    #get basis element as a column vector
    element = basis[x]
    columnv = gf.element2column(element,size=256)

    # XOR the column vector into the left column of the matrix
    for y in xrange(256):
        matrix[y][0] = matrix[y][0] ^ columnv[y][0]

    # Add the resulting matrix to the list
    A.append(copy.deepcopy(matrix)) 

def str2int(thestr):
    theint = 0
    for c in thestr:
        theint = (theint << 8) + ord(c)
    return theint
    
def ext2(data1, data2,degree=256,size=256):
    global A
    X = str2int(data1)
    Y = str2int(data2)
    xcol = gf.element2column(X,size=256)
    ycol = gf.element2column(Y,size=256)
    result = 0
    for i in xrange(size):
        Z = gf.gf2_matrix_mul(A[i],xcol)
        bit = gf.inner_product(ycol,Z)
        result = (result << 1) + bit
    return result
    

# Read in the two files as inputs X and Y.
filename1 = sys.argv[1]
filename2 = sys.argv[2]

try:
    f1 = open(filename1,"rb")
except:
    print "Cannot Open %s for reading" % filename1
    exit()
try:
    f2 = open(filename2,"rb")
except:
    print "Cannot Open %s for reading" % filename2
    exit()
    
while True:
    data1 = f1.read(32)
    data2 = f2.read(32)
    if data1 and data2:
        if (len(data1)==32) and (len(data2) == 32):
            key = ext2_blender(data1, data2)
            print "X:%064x  Y:%064x EXT2:%064x" % (str2int(data1),str2int(data2),key)
        else:
            break
    else:
        break

        
