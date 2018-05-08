#include <stdio.h>
#include <stdint.h>
#include "rdrand_stdint.h"

#define R 4096
#define A 17872
#define BMINUS1  0xffffffff

#define ITERATIONS 100

void init_mwc(uint32_t *state,uint32_t *c,uint32_t *n) {
    uint32_t x;
    int i;

    fflush(stdout);
    for (i=0; i<R; i++) {
        rdrand_get_uint32_retry(10,&(state[i]));
    }
    fflush(stdout);
    
    *c = rdrand_get_uint32_retry(10,&x);
    *n = 0;
}

uint32_t update_mwc(uint32_t *state,uint32_t *c,uint32_t *n) {
    uint64_t t;
    int ptr;
    *n = (*n + 1) % R;
    ptr = (*n + 1) % R;
    t = BMINUS1 - (((uint64_t)state[*n] * (uint64_t)A) + (uint64_t)*c);
    *c = (((uint64_t)state[*n] * (uint64_t)A) + (uint64_t)*c) >> 32;
    state[*n] = t & 0xffffffff;
    return state[*n];
}

int main() {
    uint32_t state[R];
    uint32_t c;
    uint32_t n;
    uint32_t result;
    int i;

    init_mwc(state, &c, &n);
    for (i=0;i<ITERATIONS;i++) {
        result = update_mwc(state, &c, &n);
        printf("%08x\n",result);
    }
}

