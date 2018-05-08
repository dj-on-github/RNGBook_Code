#include <stdio.h>
#include <stdint.h>
#include <math.h>

uint64_t extract_exponent(uint64_t x) {
    uint64_t e;
    e = (x >> 52) & 0x07ff; // 11 bits
    return e;   
}

uint64_t extract_mantissa(uint64_t x) {
    uint64_t m;
    m = x &  0x0fffffffffffff; // 52 bits
    return m;   
}

uint64_t extract_sign(uint64_t x) {
    uint64_t s;
    s = (x >> 63)  &  0x01; // 63rd bit
    return s;   
}

void printit(double f) {
    uint64_t *ptr;
    uint64_t sign;
    uint64_t exponent;
    uint64_t mantissa;
    ptr =  (uint64_t *)&f;

    sign = extract_sign(*ptr);     
    exponent = extract_exponent(*ptr);     
    mantissa = extract_mantissa(*ptr);

    double fmantissa;
    fmantissa = 1.0 + (mantissa * (pow(2.0,-52)));

    printf("%0.1f\t %lld\t0x%08llx\t0x%013llx\t%lld\t%lld\t%f\n",f,sign,exponent,mantissa,(-1 * sign),(exponent-1023),fmantissa);
     
}

int main() {
    double minusthree;
    double one;
    double ten;
    double zero;

    minusthree = -3.0;
    zero = 0.0;
    one = 1.0;
    ten = 10.0;

    printf("Value   Sign    Exponent    Mantissa\n");
    printit(minusthree);
    printit(zero);
    printit(one);
    printit(ten);
   
}


