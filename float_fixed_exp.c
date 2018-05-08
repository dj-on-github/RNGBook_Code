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

int main() {
    uint64_t mantissa;
    uint64_t exponent;
    uint64_t sign;
    uint64_t x;
    double *f;

    int i;
    for (i=0;i<1000;i++) {
        x = get_random_bits();
        mantissa = x &  0x0fffffffffffff;
        exponent = 1022;
        sign = (x >> 52) & 0x01;
        x = ((exponent & 0x7ff) << 52) | mantissa;
        f = (double *)&x;
        *f = *f - 0.5;
        x = x | (sign << 63);
        *f = *f + 0.5; 
        printf("%f\n",*f);
    }
}


