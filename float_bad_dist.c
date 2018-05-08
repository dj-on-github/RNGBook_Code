#include <stdio.h>
#include <stdint.h>
#include <math.h>

uint64_t histogram[100];

uint64_t get_random_bits() {
    FILE *f;
    uint64_t x;
    f = fopen("/dev/urandom", "rb");
    fread(&x,1,8,f);
    fclose(f); 
    return x;
}

uint64_t choose_exponent() {
    uint64_t e;

    do {
        e = (get_random_bits() & 0x3FF); 
    } while (e > 1022);
    return e;
}

void clear_histogram() {
    int i;
    for (i=0;i<100;i++) histogram[i]=0;
}

void add_to_histogram(double f) {
    double x;
    int i;
    x = f * 100.0;
    for (i=0;i<100;i++) {
        if (x <= ((double)(i+1))) {
            histogram[i] += 1;
            break;
        }
    }
    return;
}

int main() {
    uint64_t start;
    uint64_t mantissa;
    uint64_t exponent;
    uint64_t sign;
    uint64_t x;
    double *fp;
    double f;
    int i;
    clear_histogram();
    for (i=0;i<1000000;i++) {
        mantissa = get_random_bits() & 0x0fffffffffffff;
        exponent = choose_exponent();
        sign = 0;
        x = (sign << 63) | ((exponent & 0x7ff) << 52) | mantissa;
        fp = (double *)&x;
        f = *fp;
        add_to_histogram(f);
    }
    for (i=0;i<100;i++) printf("%d\n",histogram[i]);
}

