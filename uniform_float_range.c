#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include "rdrand_stdint.h"

#define RANGE_START 9
#define RANGE_END 13
#define ITERATIONS 1000000

int histogram[RANGE_END+3];

uint64_t get_random_bits() {
    uint64_t x;
    rdrand_get_uint64_retry(10,&x);
    return x;
}

int main() {
    double f;
    uint64_t random;
    uint64_t random_max;
    uint64_t range;
    uint64_t fint;
    int i;

    range = RANGE_END-RANGE_START+1;

    for (i=0;i<RANGE_END+3;i++) histogram[i] = 0;
    
    random_max = 0xffffffffffffffff; // 64 bits
    for (i=0;i<ITERATIONS;i++) {
        random = get_random_bits();
        f = (((double)range) / random_max)*random;
        fint = (int)f + RANGE_START;
        histogram[fint] += 1;
    }
    for (i=0;i<RANGE_END+3;i++) printf("%d\t%d\n",i, histogram[i]);
}

