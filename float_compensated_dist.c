#include <stdio.h>
#include <stdint.h>
#include <math.h>

uint64_t get_random_bits() {
    FILE *f;
    uint64_t x;
    f = fopen("/dev/urandom", "rb");
    fread(&x,1,8,f);
    fclose(f); 
    return x;
}

uint64_t choose_exponent(uint64_t start) {
    uint64_t e;

    e = start;
    do {
        if ((get_random_bits() & 0x01) == 1) return e; 
        e = e-1; 
    } while (e > 0);
    return ((uint64_t)0);
}

int main() {
    uint64_t start;
    uint64_t mantissa;
    uint64_t exponent;
    uint64_t sign;
    uint64_t x;
    double *f;

    start = 1022;
    int i;
    for (i=0;i<1000;i++) {
        mantissa = get_random_bits() & 0x0fffffffffffff;
        exponent = choose_exponent(start);
        sign = get_random_bits() & 0x01;
        x = (sign << 63) | ((exponent & 0x7ff) << 52) | mantissa;
        f = (double *)&x;
        printf("%f  exponent=%llu\n",*f,exponent);
    }
}


