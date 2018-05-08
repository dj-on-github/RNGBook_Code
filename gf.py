#!/usr/bin/env python

import random
from copy import deepcopy

# Dict of irreducable polynomials for GF(2^n)
# n,binary polynomial
polys = {
            2:    0x7,   # x^2 + x + 1
            3:    0xb,   # X^3 + x + 1
            4:   0x13,   # x^4 + x + 1
            5:   0x25,   # x^5 + x^2 + 1
            6:   0x43,   # x^6 + x + 1
            7:   0x83,   # x^7 + x + 1
            8:  0x11b,   # x^8 + x^4 + x^3 + x + 1
            9:  0x203,   # x^9 + x + 1
            10: 0x403,   # x^10 + x^3 + 1
            11: 0x805,   # X^11 + x^2 + 1
            12:0x1009,   # x^12 + x^3 + 1
            13:0x201b,   # x^13 + x^4 + x^3 + 1
            14:0x4003,   # X^14 + x + 1
            15:0x8003,   # x^15 + x + 1
            16:0x1002b   # x^16 + x^5 + x^3 + x + 1
        }

def gmul(a, b, degree=8):
    if degree == 1:
        return gf2mul(a,b)
    else:
        # Get the polynomial
        poly = polys[degree]
        # But we don't want the x^degree term, hack it off.
        poly = poly & ((1 << degree) - 1)
        
        z = 0
        if a & 1:
            r = b
        else:
            r = 0
        for i in xrange(1,degree+1):
            if  (b & (1 << (degree-1))) == 0:
                b = z ^ ((b << 1) & ((1 << degree) - 1))
            else:
                b = poly ^ ((b << 1) & ((1 << degree) - 1))
            if a & (1 << i):
                r = r ^ b
            else:
                r = r ^ z
        return r

def gadd(a, b):
    return a^b

def gpower(a, power, degree=8):
    result = a
    for i in xrange(power-1):
        result = gmul(a,result)
    return result
    
# GF(2) addition and multiplication.
# Division is the same as multiplication. Subtraction is the same as addition.
def gf2mul(a,b):
    if (a in [0,1]) and (b in [0,1]):
        return a & b
    else:
        raise Error("values must be in GF(2)")

def gf2add(a,b):
    if (a in [0,1]) and (b in [0,1]):
        return a ^ b
    else:
        raise Error("values must be in GF(2)")

# Gaussian elimination of a GF(2) matrix
def gauss(ga):
    a = deepcopy(ga)
    n = len(a)
    
    for i in range(0, n):
        # Search for maximum in this column
        maxEl = abs(a[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(a[k][i]) > maxEl:
                maxEl = abs(a[k][i])
                maxRow = k

        for k in range(i, n):
            tmp = a[maxRow][k]
            a[maxRow][k] = a[i][k]
            a[i][k] = tmp

        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            c = gf2mul(a[k][i],a[i][i])
            for j in range(i, n):
                if i == j:
                    a[k][j] = 0
                else:
                    a[k][j] = gf2add(a[k][j],gf2mul(c,a[i][j]))
    return a

# Determine if matrix a is full rank.
def full_rank(a):
    re = gauss(a)
    count = 0
    for row in re:
        empty = True
        for elem in row:
            if elem == 1:
                empty = False
        if (empty==False):
            count += 1
    if count == len(a):
        return True
    else:
        return False
        
def gf2_matrix_mul(a,b):
    # Left is nxm matrix
    left_columns = len(a[0])
    left_rows = len(a)
    
    # Right is mxp matrix
    right_columns = len(b[0])
    right_rows = len(b)
    
    # result = nxp
    result_columns = right_columns
    result_rows = left_rows
    
    # The number of columns on the left must equal the number of rows on the right.
    if left_columns != right_rows:
        #print "Left = %d x %d,  right = %d x %d" % (left_columns,left_rows,right_columns,right_rows)
        raise Error("The number of columns on the left must equal the number of rows on the right")
        
    result = make_empty_nxm_matrix(result_rows,result_columns)

    #print "Left = %d x %d,  right = %d x %d" % (left_columns,left_rows,right_columns,right_rows)
    # Fill in the result matrix
    for i in xrange(len(a)):
        for j in xrange(len(b[0])):
            total = 0
            for k in xrange(left_columns):
                #print " i j k %d %d %d " % (i,j,k)
                aa = a[i][k]
                bb = b[k][j]
                #print "B "+str(b)
                total = gf2add(total,gf2mul(aa,bb))
            result[i][j]=total

    return result

def gf2_matrix_power(a,power):
    size = len(a)
    if power == 0:
        result = make_identity_matrix(size=size)
        return result
    elif power == 1:
        result = deepcopy(a)
        return result
    else:
        result = deepcopy(a)
        for i in xrange(power-1):
            result = gf2_matrix_mul(a,result)
        return result
    
# Inner product of two GF(2) vectors x[] and y[] is x[0]*y[0] + x[1]*y[1] ... x[n-1]*y[n-1]
# Compute inner product of AiX (called z) and input seed y
def inner_product(y,z):
    ip = 0
    for i in xrange(len(y[0])):    
         ip = gf2add(ip,gf2mul(y[0][i],z[i][0]))
    return ip

# Create a random square GF(2) matrix.
# Populate a matrix with random bits and determine if it is full rank.
# Retry if it is not.
def make_random_square_full_rank_matrix(size=8):
    while True:
        a = list()
        for i in xrange(size):
            row = list()
            for j in xrange(size):
                number = random.SystemRandom().randrange(0,2)
                row.append(number)
            a.append(row[:])
        ba = deepcopy(a)
        if full_rank(ba):
            #print "FULL RANK "+str(ba)
            break
    return a

# Oh my God! It's full of zeroes! But it's not square!
def make_empty_nxm_matrix(rows=3,columns=5):
    row = list()
    for i in xrange(columns):
        row.append(0)
        
    mah_matriks = list()
    for i in xrange(rows):
        mah_matriks.append(deepcopy(row))
     
    return mah_matriks
    
# Oh my God! It's full of zeroes!
def make_empty_square_matrix(size=8):
    matrix = make_empty_nxm_matrix(rows=size,columns=size)
    return matrix
    
def make_identity_matrix(size=8):
    matrix = make_empty_square_matrix(size=size)
    for i in xrange(size):
        matrix[i][i] = 1
    return matrix

# Create a better looking printable representation of a GF(2) matrix
def matrix2str(matrix):
    size = len(matrix)
    result = "["
    for row in matrix:
        rownum = 0
        for elem in row:
            if elem == 1:
                rownum = ((rownum << 1) | 0x00000001)
            else:
                rownum = ((rownum << 1) & 0xffffffff)
        result += "%04x," % rownum
    result = result[:-1] + "]"
    return result

#convert a binary element in GF(2^n) field to a row to use in a matrix
def val2matrix(val,size=8):
    matrix = make_empty_square_matrix(size=size)
    iteration = 0
    for i in xrange(size):
        for j in xrange(size):
            bit = (val >> iteration) & 0x1
            iteration = iteration +1
            matrix[i][j] = bit
    return matrix

#convert an element to a column bit vector
def element2column(val,size=8):
    matrix = make_empty_nxm_matrix(rows=size,columns=1)
    for i in xrange(size):
        bit = (val >> i) & 0x1
        matrix[size-i-1][0] = bit
    return matrix

#convert an element to a column bit vector
def column2element(column):
    value = 0
    for i in xrange(len(column)):
        bit = column[i][0]
        value = (value << 1) | bit
    return value
    
# Create a better looking printable representation of a GF(2) matrix
def matrix2str_binary(matrix):
    size = len(matrix)
    result = "size %d [" % size
    for row in matrix:
        rownum = 0
        astr = ""
        for elem in row:
            if elem == 1:
                astr += "1"
                #rownum = ((rownum << 1) | 0x00000001)
            else:
                astr += "0"
                #rownum = ((rownum << 1) & 0xffffffff)
        result += "%s," % astr
    result = result[:-1] +"]"
    return result

    # Create a better looking printable representation of a GF(2) matrix
def matrix2str_binary_2d(matrix):
    size = len(matrix)
    result = ""
    i =0
    for row in matrix:
        rownum = 0
        if i == 0:
            astr = "["
        else:
            astr = " "
            
        for elem in row:
            if elem == 1:
                astr += "1"
                #rownum = ((rownum << 1) | 0x00000001)
            else:
                astr += "0"
                #rownum = ((rownum << 1) & 0xffffffff)
        if i == (size-1):
            result += "%s]" % astr
        else:
            result += "%s,\n" % astr
        i = i+1
    return result
    
# Take an element and raise it to powers.
def moarrrr_power_to_the_alpha(element, degree=8):
    poly = polys[degree]
    result = list()
    current = element
    power = 0
    iteration = 0
    while True:
        if power == 0:
            result.append(1)
        elif power == 1:
            result.append(element)
        else:
            current = gmul(current,element,degree=degree)
            if (current == 1) or (iteration > ((2**degree) +2)):
                break
            result.append(current)
        iteration += 1
        power += 1
    return result

    