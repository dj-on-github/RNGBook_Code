#include <stdio.h>
#include <stdint.h>
#include <sys/random.h>

int main() {
    uint32_t buffer[64];
    int i;  
    int result;  
    result = getentropy(buffer, 64*sizeof(uint32_t));

    if (result == 0) {
        for(i=0;i<64;i++) printf("%08x\n",buffer[i]);
    }
    return result; 
}

