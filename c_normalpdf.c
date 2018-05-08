#include <math.h>
#include <stdio.h>

double standard_normalpdf(double x) {
    double p;
    double pi = M_PI;
    p = (exp((-0.5)*x*x))/(sqrt(2.0*pi));
    return p;
}

double normalpdf(double x, double mu, double sigma) {
    double p;
    p  = standard_normalpdf((x-mu)/sigma)/sigma;
    return p;
}

double standard_normalcdf(double x) {
    double p;

    p = (1.0 + erf(x/sqrt(2.0)))/2.0;
    return p;
}

double normalcdf(double x, double mu, double sigma) {
    double p;

    p = standard_normalcdf((x-mu)/sigma);;
    return p;
}

int main() {
    double x;

    for (x=-4.0; x <= 4.001; x+=0.1) {
        printf("%0.2f  %1.8f\n",x,standard_normalpdf(x));
    } 
    for (x=-4.0; x <= 4.001; x+=0.1) {
        printf("%0.2f  %1.8f\n",x,normalpdf(x,-1.0,0.6));
    } 
    for (x=-4.0; x <= 4.001; x+=0.1) {
        printf("%0.2f  %1.8f\n",x,standard_normalcdf(x));
    } 
    for (x=-4.0; x <= 4.001; x+=0.1) {
        printf("%0.2f  %1.8f\n",x,normalcdf(x,1.0,0.25));
    } 
}

