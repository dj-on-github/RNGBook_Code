
#include <stdio.h>
#include <math.h>

#define MAXIT 100
#define EPS 3.0e-7
#define FPMIN 1.0e-50

// Used by betai: Evaluates continued fraction for incomplete beta function by modified Lentz’s method (§5.2).
double betacf(double a, double b, double x)
{
    void nrerror(char error_text[]);
    int m,m2;
    double aa,c,d,del,h,qab,qam,qap;
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
    if (m > MAXIT) printf("a or b too big, or MAXIT too small in betacf");
    return h;
}


//Returns the incomplete beta function Ip(a, b).
double betai(double a, double b, double p)
{
    double result;
    //printf("  Betai(a=%f, b=%f, p=%f)\n",a,b,p);
    //double betacf(double a, double b, double p);
    //double lgamm(double pp);
    //void nrerror(char error_text[]);
    double bt;

    if (p < 0.0 || p > 1.0) printf("Bad p in routine betai");
    if (p == 0.0 || p == 1.0)
        bt=0.0;
    else // Factors in front of the continued fraction.
        bt=exp(lgamma(a+b)-lgamma(a)-lgamma(b)+a*log(p)+b*log(1.0-p));

    if (p < (a+1.0)/(a+b+2.0)) { //Use continued fraction directly.
        result = bt*betacf(a,b,p)/a;
        //printf("  Return %f\n",result);
        return result;
    }
    else { //Use continued fraction after making the symreturn
        result = 1.0-bt*betacf(b,a,1.0-p)/b; //metry transformation.
        //printf("  Return %f\n",result);
        return result;
    }
}

/* Binomial CDF */
double B(int n, int  k, double p) {
   double result;
   result = 1.0 - betai((double)(k+1),(double)(n-k),p);
   return result;    
}

/* Find smallest k where B(n,k,p) > alpha */
/* Equivalent to Excel CRITBINOM function */
int binomial_critical_value(int n, double p, double alpha) {
    int min;
    int max;
    int mid;
    int newmid;
    double b;
    int finished;

    min = 0;
    max = n;
    mid = min + ((max-min) >> 1);

    finished = 0;
    while (finished == 0) {
        b = B(n,mid,p);
        if (b > alpha) {
            max = mid;
        }
        else if (b < alpha) {
            min = mid;
        }
        else if (b == alpha) {
            finished = 1;
        }
 
        newmid = min + ((max-min) >> 1);
        if (newmid == mid) finished = 1;
        mid = newmid;
    }
    if (b < alpha) mid += 1;
    return mid;
}

int main() {
    double p;
    //for (p=0.4;p < 0.6; p += 0.005) {
    //    printf("binom_crit(1024,512,%f) = %f\n",p,binom_crit(1024,512,p));
    //}

    printf("\nBINOMCRIT(100,0.3,0.7) = %d\n", binomial_critical_value(100,0.3,0.7));   
    printf("\nBINOMCRIT(1024,pow(2,-0.2),1.0-pow(2,-40)) = %d\n", binomial_critical_value(1024,pow(2,-0.2),1.0-pow(2,-40)));
    printf("\nBINOMCRIT(1024,pow(2,-0.2),1.0-pow(2,-64)) = %d\n", binomial_critical_value(1024,pow(2,-0.2),1.0-pow(2,-64)));
   
    //printf("\nW=1024,H=0.2, alpha = 2^-40) = %f \n",binom_crit(1024, pow(2,-0.2), 1-(pow(2,-40))));

}

