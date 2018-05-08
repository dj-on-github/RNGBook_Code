
#include <stdio.h>
#include <math.h>

#define MAXIT 100
#define EPS 3.0e-7
#define FPMIN 1.0e-30

// Used by betai: Evaluates continued fraction for incomplete beta function by modified Lentz’s method (§5.2).
float betacf(float a, float b, float x)
{
    void nrerror(char error_text[]);
    int m,m2;
    float aa,c,d,del,h,qab,qam,qap;
    qab=a+b;   //These q’s will be used in factors that occur
    qap=a+1.0; //in the coefficients (6.4.6).
    qam=a-1.0;
    c=1.0;     // First step of Lentz’s method.
    d=1.0-qab*x/qap;
    if (fabs(d) < FPMIN) d=FPMIN;
    d=1.0/d;
    h=d;
    for (m=1;m<=MAXIT;m++) {
        m2=2*m;
        aa=m*(b-m)*x/((qam+m2)*(a+m2));
        d=1.0+aa*d; // One step (the even one) of the recurrence.
        if (fabs(d) < FPMIN) d=FPMIN;
        c=1.0+aa/c;
        if (fabs(c) < FPMIN) c=FPMIN;
        d=1.0/d;
        h *= d*c;
        aa = -(a+m)*(qab+m)*x/((a+m2)*(qap+m2));
        d=1.0+aa*d; // Next step of the recurrence (the odd one).
        if (fabs(d) < FPMIN) d=FPMIN;
        c=1.0+aa/c;
        if (fabs(c) < FPMIN) c=FPMIN;
        d=1.0/d;
        del=d*c;
        h *= del;
        if (fabs(del-1.0) < EPS) break; // Are we done?
    }
    if (m > MAXIT) nrerror("a or b too big, or MAXIT too small in betacf");
    return h;
}


//Returns the incomplete beta function Ix(a, b).
float betai(float a, float b, float x)
{
    float betacf(float a, float b, float x);
    float gammln(float xx);
    void nrerror(char error_text[]);
    float bt;

    if (x < 0.0 || x > 1.0) nrerror("Bad x in routine betai");
    if (x == 0.0 || x == 1.0)
        bt=0.0;
    else // Factors in front of the continued fraction.
        bt=exp(gammln(a+b)-gammln(a)-gammln(b)+a*log(x)+b*log(1.0-x));

    if (x < (a+1.0)/(a+b+2.0)) //Use continued fraction directly.
        return bt*betacf(a,b,x)/a;
    else //Use continued fraction after making the symreturn
        1.0-bt*betacf(b,a,1.0-x)/b; //metry transformation.
}


