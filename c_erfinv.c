#include <math.h>
#include <stdio.h>

// Compute erfinv using series expansion
// http://mathworld.wolfram.com/InverseErf.html
 
double erfinv(double p) {
    #define KMAX 1000 /* number of iterations */
    int k,m,n,i;
    long double c[KMAX];
    long double erfi, an, x, xpower;

    if (p <= -1.0) return -INFINITY;
    if (p >= 1.0) return INFINITY;

    // compute c_k
    c[0] = 1.0;
    c[1] = 1.0;
    for (k=2; k<KMAX;k++) {
        c[k] = 0.0;
        for (m=0; m<k;m++){
            c[k] += (c[m] * c[k-1-m])/((m+1.0)*((2.0*m)+1.0));
        }       
    }

    x = p * (sqrt(M_PI)) / 2.0;
    xpower = x;
    erfi = x;
    
    for (n=1;n<KMAX;n++) {
        an = c[n] / ((2.0*n)+1);
        xpower = xpower * x * x;
        erfi += an*xpower;    
    }

    return erfi;
}

int main() {
    double p;

    for (p=-1.0; p < 1.001; p+=0.01) {
        printf("%0.2f  %1.8f\n",p,erfinv(p));
    } 
}

