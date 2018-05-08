#include <stdio.h>
#include <stdint.h>

void init_xorshift128(uint32_t* state) {
    state[0] = 0xA634716A;
    state[1] = 0x998FCD1F;
    state[2] = 0x6A9B90FE;
    state[3] = 0x7344E998;
}

uint32_t xorshift128(uint32_t* state) {
    uint32_t x;

    x = state[3];

    x = x ^ (x << 11);
    x = x ^ (x >> 8);

    state[3] = state[2];
    state[2] = state[1];
    state[1] = state[0];

    x = x ^ state[0];;
    x = x ^ (state[0] >> 19);
    state[0] = x;
    return x;
}

int main() {
    int i;
    uint32_t x;
    uint32_t state[4];
    init_xorshift128(state);
    for (i=0;i<10;i++) {
        x = xorshift128(state);
        printf("%08x\n",x);
    }
}

