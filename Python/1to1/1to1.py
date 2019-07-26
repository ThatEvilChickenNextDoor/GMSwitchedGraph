import sys
import numpy as np
import networkx as nx
from numba import njit
import time

tic=time.time()
#print('imports complete')

EIGEN=2
N=19
EXPECTED_CLIQUE=57
EPS= 0.000001

mat=np.empty((N,N))
mat_inv=np.empty_like(mat)

vecs=np.empty((1<<N,N))

vec_j=np.ones(N)

nproc = skipped = 0
#print('global constants initialized')

def stringtomat(s):
	I=np.identity(N)
	A=nx.to_numpy_array(nx.from_graph6_bytes(s))
	mat=EIGEN*I-A
	return np.linalg.inv(mat)

@njit
def constructGraph(mat_inv):
	cache_size=0
	vecs_prod=np.empty_like(vecs)
	verts=np.empty_like(vecs)
	#print('processing candidate vectors')
	for i in range(1<<N):
		if i % 10000 == 0:
			print(i, '/', 1<<N, '\t', round(i*100/(1<<N),10), '%', '\t', cache_size, 'hits')
		vecs_prod[cache_size]=np.dot(mat_inv, vecs[i])
		res=np.dot(vecs_prod[cache_size], vec_j)
		
		if abs(res+1) < EPS:
			res=np.dot(vecs_prod[cache_size], vecs[i])
			
			if abs(res-EIGEN) < EPS:
				verts[cache_size] = vecs[i]
				cache_size += 1
	if cache_size < EXPECTED_CLIQUE:
		return np.array([[0.]])

	#print('finding edges')
	A=np.zeros((cache_size, cache_size))
	for i in range(1, cache_size):
		for j in range(i):
			res=np.dot(vecs_prod[i], verts[j])
			
			if abs(res) <= EPS or abs(res+1) <= EPS:
				A[i,j]=1
				A[j,i]=1
	#print('writing graph')
	return A
	
def init_vectors():
	for i in range(1<<N):
		for j in range(N):
			if i & (1<<j):
				vecs[i,j]=1


#print('initializing vectors')
init_vectors()

#print('creating output file')
filepath=sys.argv[1] #save input filepath
with open(filepath, 'rb') as fp: #create output file
	#print('opening input file')
	with open(filepath + '.out', 'wb') as op: #open input file
		s=fp.readline()
		while s:
			#print('processing line')
			mat_inv=stringtomat(s.strip())
			#print('constructing graph')
			A=constructGraph(mat_inv)
			if A.size != 1:
				op.write(nx.to_graph6_bytes(nx.Graph(A), header=False))
			else:
				skipped+=1
			nproc+=1
			s=fp.readline()
print('Successfuly processed: {} graphs. Skipped: {}'.format(nproc, skipped))
toc=time.time()-tic
print('Time elapsed: {} seconds'.format(round(toc, 3)))