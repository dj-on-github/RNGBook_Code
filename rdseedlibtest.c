#include<stdio.h>
#include<stdint.h>
#include "rdrand_stdint.h"

int main() {

    int i;
    uint64_t buffer[32];
    int result;
    i = 0;

    if (rdseed_check_support() == 1) {
        for(i=0;i<32;i++) {
            do result = rdseed_get_uint64_retry(1000,&buffer[i]);
            while (result == 0);
        }
        for(i=0;i<32;i++) printf("%016llx\n",buffer[i]);
    }
    else printf("RdRand instruction not supported\n");
    
}
