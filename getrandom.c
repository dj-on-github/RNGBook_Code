#include<stdio.h>
#include<stdint.h>
#include<unistd.h>
#include<syscall.h>
#include<errno.h>
#include<linux/random.h>

int main() {

    unsigned char buffer[64];
    int i;
    int result;
    result = syscall(SYS_getrandom, buffer, 64, 0);

    if (result > 0) {
        printf("%d bytes returned\n",result);
        for(i=0;i<result;i++) {
            printf("%02x",buffer[i]);
            if ((i > 0) && (((i+1) % 4) == 0)) printf("\n");
        }
        if ((i%4) != 0) printf("\n");
    }
    else {
        printf("Error. getrandom() returned errno %d\n",errno);
        return -1;
    }
    return 0;
}

