#!/usr/bin/env python

import gf2 as gf
import copy

degree = 32 # largest power of the generator polynomial.
element = 2 # Element to raise powers of for the basis
seedlength = 4 # Output bit length of the blender. 
               # Also the number of matrices to generate
               
A = list()
# Create A_1, an identity matrix
A.append(gf.make_identity_matrix(size=degree))

# Compute basis element list x_i  
basis = gf.moarrrr_power_to_the_alpha(element, degree=degree, length=seedlength)
print "Basis x_i = ", ["0x%x" % x for x in basis[:seedlength]]
for x in range(1,seedlength):
    # compute A_{i+1}
    matrix = copy.deepcopy(A[x-1]) # copy A_{x-1}
    gf.rotate_right_matrix(matrix) # Shift ot right
    
    #get basis element as a column vector
    element = basis[x]
    columnv = gf.element2column(element,size=degree)

    # XOR the column vector into the left column of the matrix
    for y in xrange(degree):
        matrix[y][0] = matrix[y][0] ^ columnv[y][0]

    # Add the resulting matrix to the list
    A.append(copy.deepcopy(matrix)) 

for i,x in enumerate(A):
    print "matrix A_%d" % (i+1)
    print gf.matrix2str_binary_2d(x)

