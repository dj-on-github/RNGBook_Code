#include<stdio.h>
#include<stdint.h>
#include<sys/stat.h> 
#include<fcntl.h>
#include<unistd.h>

int main() {
    uint32_t buffer[64];
    int f;
    int result;
    int i;

    f = open("/dev/urandom", O_RDONLY);
    if (f < 0) {
        printf("Error: open() failed to open /dev/random for reading\n");
        return -1;
    }

    result = read(f, buffer, 64*sizeof(uint32_t));

    if (result < 0) {
        printf("error, failed to read %lu bytes\n",64*sizeof(uint32_t));
        return -1;
    }

    for(i=0;i<64;i++) printf("%08x\n",buffer[i]);
    return 0;
}

