

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <stdint.h>
#include <unistd.h>
#include <getopt.h>

#define BUFSIZE 2048

void display_usage() {
fprintf(stderr,"Usage: mean_sigma [-h][-s lines_to_skip][filename]\n");
fprintf(stderr,"\n");
fprintf(stderr,"Compute mean and standard deviation of numerical data, one float per line.\n");
fprintf(stderr,"  Author: David Johnston, dj@deadhat.com\n");
fprintf(stderr,"\n");
}

int ishex(char ch) {
    if ((ch > 0x2f) && (ch < 0x3a)) return 1; /* digits */
    if ((ch > 0x40) && (ch < 0x47)) return 1; /* A-F */
    if ((ch > 0x60) && (ch < 0x67)) return 1; /* a-f */
    return 0;
}

int ishexorx(char ch) {
    if ((ishex(ch)==1) || (ch=='x')) return 1; 
    return 0;
}

int hextobyte(char *astr) {
    char cha;
    int result=0;
    int i;
    
    for (i=0;i<2;i++){ 
        cha = astr[i];
        result = result << 4;
        if ((cha > 0x2f) && (cha < 0x3a)) result += (cha - 0x30);
        else if ((cha > 0x40) && (cha < 0x47)) result += (cha + 0x0A - 0x41);
        else if ((cha > 0x60) && (cha < 0x67)) result += (cha + 0x0A - 0x61);
    }
    return result;  
}

/********
* main() is mostly about parsing and qualifying the command line options.
*/
 
int main(int argc, char** argv)
{
    int opt;
	int i;
	size_t len;
        	
	FILE *ifp;
	FILE *ofp;
	int using_outfile;
	int using_infile;
	char filename[1000];
	char infilename[1000];
    int skiplines;
    int abyte;
    
	/* Defaults */
	using_outfile = 0;      /* use stdout instead of output file*/
    using_infile = 0;       /* use stdin instead of input file*/
    skiplines = 0;
    
    filename[0] = (char)0;
	infilename[0] = (char)0;

	/* get the options and arguments */
    int longIndex;

    char optString[] = "h";
    static const struct option longOpts[] = {
    { "help", no_argument, NULL, 'h' },
    { NULL, no_argument, NULL, 0 }
    };
    
    opt = getopt_long( argc, argv, optString, longOpts, &longIndex );
    while( opt != -1 ) {
        switch( opt ) {
            case 's':
                skiplines = atoi(optarg);
                if (skiplines < 1) skiplines = 0;
                break;    
            case 'h':   /* fall-through is intentional */
            case '?':
                display_usage();
                exit(0);
                 
            default:
                /* You won't actually get here. */
                break;
        }
         
        opt = getopt_long( argc, argv, optString, longOpts, &longIndex );
    } // end while
    
    if (optind < argc) {
        strcpy(infilename,argv[optind]);
        using_infile = 1;
    }

    char errstring[100];
    
	/* open the input file if needed */
	if (using_infile==1)
	{
        ifp =  fopen(infilename, "r");
	    
		if (ifp == NULL) {
            sprintf(errstring,"failed to open input file %s for reading",infilename);
			perror(errstring);
			exit(1);
		}
	}

    unsigned char buffer[BUFSIZE+1];
    unsigned char outbuffer[BUFSIZE+1];
    int outindex = 0;
    int charcount = 0;
    char hexchars[2];
    
    /* Skip lines if requested */
    
    buffer[BUFSIZE] = 0;
    
    if (skiplines>0) {
        for (i=0;i<skiplines;i++) {
            if (using_infile==1)
                len = (size_t)fgets((char *)buffer,BUFSIZE, ifp);
            else
                len = (size_t)fgets((char *)buffer,BUFSIZE, stdin);
            if (len==0) break;
        }
    }
    
    /* state to gather two characters */
    hexchars[0] = ' ';
    hexchars[1] = ' ';
    charcount = 0;
    char achar;
    outindex = 0;
    char hexstring[3];
    int inindex;
    
    do {
        /* Read in hex data from file */
        if (using_infile==1)
            len = fread(buffer, 1, BUFSIZE , ifp);
        else
            len = fread(buffer, 1, BUFSIZE , stdin);
        
        /* End when we reach EOF */
        if (len == 0) break;
        
        /* Pick up hex char pairs and move to outbuffer until outbuffer is full
         * or we reached end of inbuffer */
        inindex=0;
        outindex = 0;
        do {
            /* Slide through the data picking up 2 hex characters, discarding trash */
            
            do {
                if (charcount < 2) 
                    achar = buffer[inindex++];
                    if (ishex(achar)) {
                        hexchars[charcount++]=achar;
                        i++;
                    }
                
                    /* Skip 0x */
                    
                    /* we last got 0 and the next is x - hence 0x */
                    if ((hexchars[0]=='0') && (achar=='x') && (charcount==1)) {
                        charcount = 0; /* skip 0x prefixes */
                    }
                    /* We have 2 hexchars in and the next is x, so discard it */
                    else if ((achar=='x') && (charcount==2)) {
                        charcount = 0;
                    }
                    
                    /* Use if we have two hex chars, turn into binary */
                    
                    if (charcount == 2) {
                        hexstring[0] = hexchars[0];
                        hexstring[1] = hexchars[1];
                        hexstring[2] = '0';
                        abyte = hextobyte(hexstring);
                        outbuffer[outindex++]=abyte;
                    }
                
                /* until we have two hexchars or we run out of input data */
            } while ((charcount < 2) && (inindex < len));
            if (charcount == 2) {
                charcount = 0;
            }
            /* until we run out of output buffer or run out of input data */
        } while ((outindex < BUFSIZE) && (inindex<BUFSIZE));

        /* Now we have a binary buffer outbuffer with outindex chars.
         * Output it.
         */

        if (using_outfile == 1)
            fwrite(outbuffer, 1, outindex, ofp);
        else
            fwrite(outbuffer, 1, outindex, stdout);
            
        outindex = 0;
        
    } while (1==1);
    
    if (using_outfile==1) fclose(ofp);
    
}


