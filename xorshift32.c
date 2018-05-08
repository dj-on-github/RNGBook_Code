#include <stdio.h>
#include <stdint.h>

void init_xorshift32(uint32_t* state) {
    *state  = 0xA634716A;
}

uint32_t xorshift32(uint32_t* state) {
    uint32_t x;

    x = *state;
    x = x ^ (x << 13);
    x = x ^ (x >> 17);
    x = x ^ (x << 5);
    *state = x;
    return x;
}

int main() {
    int i;
    uint32_t x;
    uint32_t state;
    init_xorshift32(&state);
    for (i=0;i<10;i++) {
        x = xorshift32(&state);
        printf("%08x\n",x);
    }
}

