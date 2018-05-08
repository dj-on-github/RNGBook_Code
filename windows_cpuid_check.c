#include <stdio.h>
#include "stdafx.h"
#include <string.h>
#include <stdlib.h>
#include <intrin.h>
 
#define BUFFERSZ 128
 
int check_is_intel() {
       int regs[4];
 
       __cpuid(regs, 0);
 
       if (memcmp((char *)(&regs[1]), "Genu", 4) == 0 &&
              memcmp((char *)(&regs[2]), "ineI", 4) == 0 &&
              memcmp((char *)(&regs[3]), "ntel", 4) == 0) {
              return 1;
       }
       return 0;
}
 
int check_is_amd() {
       int regs[4];
 
       __cpuid(regs, 0);
 
       if (memcmp((char *)(&regs[1]), "Auth", 4) == 0 &&
              memcmp((char *)(&regs[2]), "enti", 4) == 0 &&
              memcmp((char *)(&regs[3]), "cAMD", 4) == 0) {
              return 1;
       }
       return 0;
}
 
int check_rdrand() {
       int regs[4];
 
       __cpuid(regs, 1);
 
       if ((regs[2] & 0x40000000) == 0x40000000) return 1;
       return 0;
}
 
int check_rdseed() {
       int regs[4];
 
       __cpuid(regs, 7);
 
       if ((regs[1] & 0x00040000) == 0x00040000) return 1;
       return 0;
}

