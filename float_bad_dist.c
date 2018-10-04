#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>

#define MAXBINS 1000000
#define ITERATIONS 1000000

uint64_t get_random_bits(FILE *f) {
    uint64_t x;
    fread(&x,1,8,f);
    return x;
}

uint64_t choose_exponent(FILE *f) {
    uint64_t e;

    do {
        e = (get_random_bits(f) & 0x3FF); 
    } while (e > 1022);
    return e;
}

void clear_histogram(uint64_t *histogram) {
    int i;
    for (i=0;i<MAXBINS;i++) histogram[i]=0;
}

void add_to_histogram(uint64_t *histogram, int bins, double f) {
    double x;
    int i;
    x = f * (double)bins;
    for (i=0;i<bins;i++) {
        if (x <= ((double)(i+1))) {
            histogram[i] += 1;
            break;
        }
    }
    return;
}

int main(int argc, char *argv[]) {
    uint64_t start;
    uint64_t mantissa;
    uint64_t exponent;
    uint64_t sign;
    uint64_t x;
    double *fp;
    double f;
    double max;
    double min;
    int bins;
    int i;

    uint64_t histogram[MAXBINS];
    
    if (argc > 1) bins = atoi(argv[1]);
    else bins = 10;
    if (bins > MAXBINS) {
        printf("Error, to many bins. The maximum is %d\n",MAXBINS);
        exit(-1);
    }

    FILE *dur;
    dur = fopen("/dev/urandom", "rb");

    clear_histogram(histogram);
    for (i=0;i<ITERATIONS;i++) {
        mantissa = get_random_bits(dur) & 0x0fffffffffffff;
        exponent = choose_exponent(dur);
        sign = 0;
        x = (sign << 63) | (exponent << 52) | mantissa;
        fp = (double *)&x;
        f = *fp;
        add_to_histogram(histogram,bins,f);
    }

    for (i=0;i<10;i++) {
        min = (i*1.0)/bins;
        max = ((i+1)*1.0)/bins;
        printf("%1.8f to %1.8f :  %llu\n",min,max,histogram[i]);
    }
    fclose(dur);
    return 1;
}

