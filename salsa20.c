#include <stdio.h>
#include <stdint.h>

uint32_t rol(uint32_t x,uint32_t amount) {
    return ((x << amount ) | (x >> (32 - amount)));
}
uint32_t ror(uint32_t x,uint32_t amount) {
    return ((x >> amount) | (x << (32-amount)));
}

void quarterround(uint32_t y0,uint32_t y1,uint32_t y2,uint32_t y3,
                 uint32_t *z0,uint32_t *z1,uint32_t *z2,uint32_t *z3) {
    *z1 = y1 ^ rol((y0 + y3),7);
    *z2 = y2 ^ rol((*z1 + y0),9);
    *z3 = y3 ^ rol((*z2 + *z1),13);
    *z0 = y0 ^ rol((*z3 + *z2),18);
}

void doubleround(uint32_t *x, uint32_t *z) {
    uint32_t t[16];
    /* ARX Columns */
    quarterround(x[0],x[4],x[8],x[12],    &t[0], &t[4]  ,&t[8]  ,&t[12]);
    quarterround(x[5],x[9],x[13],x[1],    &t[5], &t[9]  ,&t[13] ,&t[1]);
    quarterround(x[10],x[14],x[2],x[6],  &t[10], &t[14] ,&t[2]  ,&t[6]);
    quarterround(x[15],x[3],x[7],x[11],  &t[15], &t[3]  ,&t[7]  ,&t[11]);    
    /* ARX  rows */
    quarterround(t[0],t[1],t[2],t[3],    &z[0], &z[1]  ,&z[2]  ,&z[3]);
    quarterround(t[5],t[6],t[7],t[4],    &z[5], &z[6]  ,&z[7]  ,&z[4]);
    quarterround(t[10],t[11],t[8],t[9],  &z[10],&z[11] ,&z[8]  ,&z[9]);
    quarterround(t[15],t[12],t[13],t[14],&z[15],&z[12] ,&z[13] ,&z[14]);      
}

uint32_t littleendian(uint8_t b0,uint8_t b1,uint8_t b2,uint8_t b3) {
    return (b0 + (b1 << 8) + (b2 << 16) + (b3 << 24)); }

void littleendian_inv(uint32_t b, uint8_t *z) {
    z[0] = (b & 0xff); z[1] = (b >> 8) & 0xff;
    z[2] = (b >> 16) & 0xff; z[3] = (b >> 24) & 0xff; }

void salsa20_hash(unsigned char *xin, unsigned char*zout) {
    uint32_t x[16];
    uint32_t z[16];
    uint32_t temp[16];
    int i;

    for(i=0;i<16;i++)
        x[i] = littleendian(xin[(4*i)],xin[(4*i)+1],xin[(4*i)+2],xin[(4*i)+3]);
    /*salsa20_inner(x,z);*/
    
    doubleround(x,temp); /* 10 Rounds */
    for(i=0;i<4;i++) {
        doubleround(temp,z);
        doubleround(z,temp);
    }
    doubleround(temp,z);
    
    for(i=0;i<16;i++) z[i] = z[i]+x[i];
    for(i=0;i<16;i++) littleendian_inv(z[i],&zout[i*4]);
}

void salsa20kn(uint8_t *k, int klen, uint8_t *n, uint8_t *result) {
    uint8_t key[64];
    int i;
    /* sigma0, tau0 */
    key[0]=101; key[1]=120; key[2]=112; key[3]=97;
    
    if (klen==16) {
        for(i=0;i<16;i++) key[i+4] = k[i];
        key[20]=110; key[21]=100; key[22]=32; key[23]=49; /*tau1*/
        for(i=0;i<16;i++) key[i+24] = n[i];
        key[40]=54; key[41]=45; key[42]=98; key[43]=121; /*tau2*/
        for(i=0;i<16;i++) key[i+44] = k[i];
    }
    else if (klen==32) {
        for(i=0;i<16;i++) key[i+4] = k[i];
        key[20]=110; key[21]=100; key[22]=32; key[23]=51; /*sigms1*/
        for(i=0;i<16;i++) key[i+24] = n[i];
        key[40]=50; key[41]=45; key[42]=98; key[43]=121; /*sigms2*/
        for(i=0;i<16;i++) key[i+44] = k[i+16];   
    }
    key[60]=116; key[61]=101; key[62]=32; key[63]=107; /*tau & sigma3*/
    
    salsa20_hash(key,result);
}

int main() {
    uint8_t key[32];
    uint8_t n[16];
    uint8_t result[64];
    uint32_t *ctr;
    int i;
    int j;

    for(i=0;i<32;i++) key[i]=(uint8_t)i;
    for(i=0;i<16;i++) n[i]=(uint8_t)i;
    ctr = (uint32_t *)n;
    for(i=0;i<4;i++) {  /* call 4 times with incrementing counter */
        ctr[0] = i;
        salsa20kn(key, 32, n, result);
        for(j=0;j<64;j++){
            printf("%02x",result[j]);
            if (j==31) printf("\n");
        }
        printf("\n");
    }

}

 

