#include <stdio.h>
#include <string.h>
#include "aes128k128d.h"
 
int main(int argc, char** argv) {
    FILE *fp;
    char filename[256];
    unsigned char buffer[64];
    int c,i;
    int finished = 0;
    unsigned char feedforward[16];
    char output[64];
    unsigned char key[16];
    unsigned char initdata[16];
    
    // Clear start value and compute key
    for (i=0;i<16;i++){
        feedforward[i] = 0;
        key[i] = 0;
        initdata[i] = 0;
    }
    initdata[0] = 1;
    aes128k128d(key,initdata,key);
    
    // Get the file name
    if (argc == 2) {
        strcpy(filename,argv[1]);
    }    
    else {
        printf("Error: Enter single filename as argument\n");
        exit(1);
    }
    
    // Loop through the file, running CBC-MAC.
    fp = fopen(filename,"rb");
    while (finished == 0) {
        c = fread(buffer,1,64,fp);
        if (c==64) {
            for (i=0;i<4;i++) {
                xor_128(buffer+(i*16), feedforward, feedforward);
                aes128k128d(key,feedforward, feedforward); 
            }
            for (i=0;i<16;i++) sprintf(&output[i*2],"%02X",feedforward[i]);
            output[32] = 0; 
            printf("%s\n",output);
        }
        else finished = 1;
    }
    fclose(fp);
    exit(0);
}
