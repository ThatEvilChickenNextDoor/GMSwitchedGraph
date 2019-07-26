import sys
import numpy as np
import networkx as nx
from itertools import combinations
from numba import njit
import time

tic=time.time()
#print('imports complete')

EIGEN=3
N=50
EXPECTED_CLIQUE=196
EPS= 0.000001

mat=np.empty((N,N))
mat_inv=np.empty_like(mat)

vecs=np.empty((121287375,50), 'B')

vec_j=np.ones(N)

nproc = skipped = 0
#print('global constants initialized')

def stringtomat(s):
	I=np.identity(N)
	A=nx.to_numpy_array(nx.from_graph6_bytes(s))
	mat=EIGEN*I-A
	return np.linalg.inv(mat)

#@njit
def constructGraph(mat_inv, size):
	cache_size=0
	vecs_prod=np.empty_like(vecs)
	verts=np.empty_like(vecs)
	#print('processing candidate vectors')
	for i in range(size):
		if i % 10000 == 0:
			print(i, '/', size, '\t', round(i*100/(size),10), '%', '\t', cache_size, 'hits')
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
	global vecs
	combs = list(combinations(range(12),4))
	l = len(combs)
	comb_vecs=np.zeros((l, 12), 'uint8')
	for i in range(l):
		for pos in combs[i]:
			comb_vecs[i, pos]=1
	print('combinations generated')
	header = np.tile(np.array([1,0,0,0,1,0,0,0,0,0,0,0,0,0], 'uint8'), (len(vecs),1))
	vecs[:,:14]=header
	del(header)
	first = np.repeat(comb_vecs, l**2, axis=0)
	vecs[:,14:26]=first
	del(first)
	second = np.tile(
	np.repeat(comb_vecs, l, axis=0),
	(l,1))
	vecs[:,26:38]=second
	del(second)
	third = np.tile(comb_vecs, (l**2, 1))
	vecs[:,38:]=third
	del(third)
	print('arrangement complete')
	print(len(vecs))

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
			A=constructGraph(mat_inv, len(vecs))
			if A.size != 1:
				op.write(nx.to_graph6_bytes(nx.Graph(A), header=False))
			else:
				skipped+=1
			nproc+=1
			s=fp.readline()
print('Successfuly processed: {} graphs. Skipped: {}'.format(nproc, skipped))
toc=time.time()-tic
print('Time elapsed: {} seconds'.format(round(toc, 3)))