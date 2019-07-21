/* 
   Compile as

   gcc compGraph2graph6.c -O2 -lgsl -lgslcblas -o compGraph2graph6
*/   
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include <gsl/gsl_linalg.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_eigen.h>
#include <gsl/gsl_blas.h>

/* Order of input graphs - note this code will only work for orders smaller than 62 */
#define N 19

/* Maximum order we expect for the the comparability graph */
#define MAX_ORDER 75000

/* Forbidden eigenvalue of the star complement */
#define SC_EIG 2 

/* Specified precision used while doing floating point operations we treat EPS as zero */
#define EPS 0.000001

#define EXPECTED_CLIQUE 57

/* graph6 related things */

#define SIZELEN(n) ((n)<=SMALLN?1:((n)<=SMALLISHN?4:8))
#define G6LEN(n) (SIZELEN(n) \
         + ((size_t)(n)/12)*((size_t)(n)-1) + (((size_t)(n)%12)*((size_t)(n)-1)+11)/12)

#define SMALLN 62
#define BIAS6 63
#define TOPBIT6 32
#define SMALLISHN 258047
#define MAXBYTE 126
#define C6MASK 63

static gsl_matrix *mat, *mat_inv;
static gsl_permutation *perm;

static gsl_vector *vecs[1<<N]; //vecs and vecs_prod are arrays of vectors with size 2^N
static gsl_vector *vecs_prod[1<<N];

static gsl_vector *vec_j;

/* storing the current graph6 string of our graph */
static char line[G6LEN(N)+2];

static char gcode[G6LEN(MAX_ORDER)+3]; //gcode is string with enough room to store graph of order MAX_ORDER

/* number of currently processed graphs. */ 
static unsigned nproc = 0;
static unsigned skipped = 0;

static FILE *outFile;

static void stringtomat(char *s) {

	char *p;
	int i,j,k,x = 0;

    /* Clear the adjacency matrix */
    gsl_matrix_set_zero(mat);

    p = s + 1;

    k = 1;
    
    gsl_matrix_set(mat, 0, 0, SC_EIG);

    for (j = 1; j < N; ++j) {
        gsl_matrix_set(mat, j, j, SC_EIG);
        for (i = 0; i < j; ++i) {
            if (--k == 0) {
        		k = 6;
		        x = *(p++) - BIAS6;
            }
	    
            if (x & TOPBIT6) {
                gsl_matrix_set(mat, i, j, -1);
                gsl_matrix_set(mat, j, i, -1);
            }
            x <<= 1;
        }
    }

    int signum;
    gsl_linalg_LU_decomp(mat, perm , &signum);
    gsl_linalg_LU_invert(mat, perm, mat_inv);

}

/* Some graph6 string thingie */
static void encodegraphsize(const int n, char **pp) {
    char *p;

    p = *pp;
    if (n <= SMALLN) 
        *p++ = BIAS6 + n;
    else {
        *p++ = MAXBYTE;
        *p++ = BIAS6 + (n >> 12);
        *p++ = BIAS6 + ((n >> 6) & C6MASK);
        *p++ = BIAS6 + (n & C6MASK);
    }
    *pp = p;
}

/* Given that mat_inv is the M = SC_EIG*I - A we 
   compute all binary vectors x such that x M x^t == SC_EIG
   and x M j^t == -1. 

   Finally for any pair x,y of such vectors we add an edge to our 
   graph if x M y^t is either 0 or -1.
*/

/* This is a global thingie since declaring it localy as 
 * an array of size 1<<N breaks the stack limit */
gsl_vector *verts[1<<N];

static void constructGraph(void) {

    double res; //allocate memory for double-sized result
    unsigned i, j; //declare variables used for looping

    /* After the first iteration this holds the number of 
       vertices of the obtained graph. The respective vertices
       are stored in vecs_prod[0]...vecs_prod[cache_size-1].
    */ 
    unsigned cache_size = 0; //initialize cache_size to 0

    for (i = 0; i < 1<<N; i++) { //loop through all 2^N vectors in vecs, looking to fill in the vertices
        gsl_blas_dsymv(CblasUpper, 1, mat_inv, vecs[i], 0, vecs_prod[cache_size]); //set vecs_prod[cache_size] to mat_inv*vecs[i], assuming mat_inv is symmetrical and using upper triangle ((rI-A_H)^-1*u), this is the bilinear form <u,_>

        gsl_blas_ddot(vecs_prod[cache_size], vec_j, &res); //calculate <u,j> and store it in space allocated for result
    
        if (fabs(res+1) < EPS) { //if <u,j> = -1 (within EPS precision)
            gsl_blas_ddot(vecs_prod[cache_size], vecs[i], &res); //calculate <u,u> and store it in space allocated for result

            if (fabs(res-SC_EIG) < EPS) { //if <u,u> = r (within EPS precision)
                verts[cache_size] = vecs[i]; //it's a vertex, store vecs[i] in verts
                cache_size+=1; //search for the next vector
            }                
        }
    }
    //we now have matched arrays vert[] and vec_prod[], with valid vertices in the former and <u,_> in the latter
    if (cache_size < EXPECTED_CLIQUE) { //if there aren't enough elements to form target clique, no point in continuing, skip to next star complement candidate
        skipped++;
        return;
    }

    assert(cache_size < MAX_ORDER); //check if order is less than maximum allowed order
	//prepare to output compatibility graph
    char *p = gcode; //point *p at start of gcode
    encodegraphsize(cache_size, &p);

    int k = 6, x = 0; //initialize bit written counter and bit to be written

    for (i = 1; i < cache_size; i++) { //loop through all vertices u_i
        for (j = 0; j < i; j++) { //loop through <u_i,u_1> up to <u_i,u_i>, since <u,v> = <v,u> we don't have to check the rest as they will be checked in a later iteration
            x <<= 1; //ready next bit
            gsl_blas_ddot(vecs_prod[i], verts[j], &res); //calculate <u_i,u_j> and store it in space allocated for result

            /* We have an edge */
            if (fabs(res) <= EPS || fabs(res+1) <= EPS) { //if <u_i,u_j> = 0 or -1 (it's an edge)
                x |= 1; //set last bit of x to 1
            } 
            if (--k == 0) { //decrease bit written counter
                *p++ = BIAS6 + x; //if we wrote 6 bits, add padding for ASCII character and write byte to where *p is pointing and advance pointer *p forward by 1 character
                k = 6; //reset counters
                x = 0;
            }
 
        }
    }
	//all full bytes written to gcode, prepare to write to file
    if (k != 6) { //if last byte is incomplete (still waiting to be written)
        *p++ = BIAS6 + (x << k); //push last bits to front, add padding, write to *p, advance *p
    }        
    *p++ = '\n'; //stitch on newline, advance *p
    *p = '\0'; //stitch on null (to end string)

    fputs(gcode, outFile); //write to output file
}


static void init_vectors(void) {
    
    unsigned i,j;

    vec_j = gsl_vector_alloc(N); //allocate memory for vec_j with size N

    assert(vec_j); //check if vec_j was created successfully

    gsl_vector_set_all(vec_j, 1); //initialize vec_j as all 1's

    for (i = 0; i < 1<<N; i++) { //loop through all 2^N vectors in vecs[] and vecs_prod[]
        vecs[i] = gsl_vector_calloc(N); //initialize each vecs[i] to all 0
        vecs_prod[i] = gsl_vector_alloc(N); //allocate memory for vectors of size N

        assert(vecs[i] && vecs_prod[i]); //check if vectors were initialized successfully        

        /* We fill the i'th vector of vecs */
        for (j = 0; j < N; j++) { //loop through length of vecs[i]
            if ( i & (1<<j) ) { //set vecs[i] to binary representation of i
                gsl_vector_set(vecs[i], j, 1);
            }
        }
    }   
}


int main(int argc, char **argv) { //start here
    
    static FILE *infile; //declare pointer to input file

    assert (argc > 1); //check if arguments were provided (you can provide multiple, only the first will be used though)
    
    infile = fopen(argv[1], "r"); //open first argument in read mode and point *infile at it
    mat = gsl_matrix_alloc(N, N); //allocate memory for mat as NxN matrix (not initialized yet, contents are garbage)
    mat_inv = gsl_matrix_alloc(N, N); //allocate memory for mat_inv as NxN matrix
    perm = gsl_permutation_calloc(N); //initialize perm as identity permutation of length N

    char buf[512]; //declare string of 511+1 characters

    snprintf(buf, sizeof(buf), "%s.out", argv[1]); //fill buf with name of input file, append .out to the name
    outFile = fopen(buf, "w"); //create file with name contained in buf in write mode, point *outFile at it

    assert (outFile && infile && mat && mat_inv && perm); //check if everything exists
    
    init_vectors();

    while (1) {
        if (!fgets(line, sizeof(line), infile)) 
            break;
        stringtomat(line);
        constructGraph();
        nproc++;
	}
    
    printf("Successfuly processed: %u graphs. Skipped: %u\n" , nproc, skipped);

    return 0;
}
