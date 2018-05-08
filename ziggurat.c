#include <stdio.h>
#include <stdlib.h>
#include <math.h>

static unsigned long iz,jz,jsr=123456789,kn[128];
static long hz;
static double wn[128],fn[128];

unsigned long shr3() {
    jz=jsr;
    jsr^=(jsr<<13);
    jsr^=(jsr>>17);
    jsr^=(jsr<<5);
    
    jsr = jsr & 0xffffffff;
    jz = jz   & 0xffffffff;
    return jz+jsr;
}

double uni() {
    unsigned long umm;
    umm=shr3();
    return (.5 + ((signed) umm) * .2328306e-9);
}

float nfix(void) {
    const double r = 3.442620;
    static double x, y;

    for(;;) {
        x=hz*wn[iz];
        if(iz==0) {
            do {
                x=-log(uni())*0.2904764;
                y=-log(uni());
            }
            while((y+y)<(x*x));
        
            if (hz>0)
                return(r+x);
            else
                return(-r-x);
        }

        if (fn[iz]+uni()*(fn[iz-1]-fn[iz]) < exp(-.5*x*x))
            return x;

        hz = shr3();
        iz = hz & 127;
        if (abs(hz)<kn[iz])
            return (hz*wn[iz]);
    }
}

#define RNOR (hz=SHR3, iz=hz&127, (abs(hz)<kn[iz])? hz*wn[iz] : nfix())
double rnor() {
    hz = shr3_signed();
    iz = hz & 127;
    if (abs(hz)<kn[iz]) {
        return hz*wn[iz];
    }
    else {
        return nfix();
    }
}

/*--------This procedure sets the seed and creates the tables------*/
void zigset(unsigned long jsrseed) {
    const double m1 = 2147483648.0, m2 = 4294967296.0;
    double dn=3.442619855899,tn=dn,vn=9.91256303526217e-3, q;
    int i;
    
    jsr=jsrseed;

/* Tables for RNOR: */
    q=vn/exp(-.5*dn*dn);
    kn[0]=(dn/q)*m1;
    kn[1]=0;
    wn[0]=q/m1;
    wn[127]=dn/m1;
    fn[0]=1.;
    fn[127]=exp(-.5*dn*dn);
    
    for(i=126;i>=1;i--) {
        dn=sqrt(-2.*log(vn/dn+exp(-.5*dn*dn)));
        kn[i+1]=(dn/tn)*m1;
        tn=dn;
        fn[i]=exp(-.5*dn*dn);
        //printf("dn=%f   m1=%f   dn/m1 = %1.20f\n",dn,m1,(dn/m1));
        wn[i]=dn/m1;
    }
    
    //printf("KN\t\t\tfn\t\twn\n");
    //for (i=0; i<128;i++) {
    //    printf("%016lX\t%0.8f\t%1.20f\n",kn[i],fn[i],wn[i]);
    //}
}

int main() {
    int i;
    zigset(17235321);

    //printf("UNI\n");
    //for (i=0;i<3;i++) {
    //    printf("%0.8f\n",uni());
    //}
    //printf("\n");
    //printf("\n SHR3 \n");
    //for (i=0;i<20;i++) {
    //    printf("%016lX\n",shr3());
    //}
    //
    //printf("\n UNI \n");
    //for (i=0;i<20;i++) {
    //    printf("%0.8f\n",uni());
    //}
    //
    printf("\n RNOR\n");
    for (i=0;i<20;i++) {
        printf("%0.8f\n",rnor());
    }
    
}
