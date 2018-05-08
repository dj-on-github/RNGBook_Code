#include<stdio.h>
#include<stdint.h>
#include "rdrand_stdint.h"

int main() {

    int i;
    uint64_t buffer[32];

    i = 0;

    if (rdrand_check_support() == 1) {
        for(i=0;i<32;i++) rdrand_get_uint64_retry(10,&buffer[i]);

        for(i=0;i<32;i++) printf("%016llx\n",buffer[i]);
    }
    else printf("RdRand instruction not supported\n");
    
}
