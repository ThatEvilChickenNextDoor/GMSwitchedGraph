import sys
import numpy as np
import networkx as nx
from numba import njit

EIGEN=2
N=19
EPS= 0.000001

mat=np.zeros((N,N))
mat_inv=np.zeros_like(mat)

vecs=np.zeros((1<<N,N))
vecs_prod=np.zeros_like(vecs)

vec_j=np.ones(N)

verts=np.zeros_like(vecs)

def stringtomat(s):
	I=np.identity(N)
	A=nx.to_numpy_array(nx.from_graph6_bytes(s))
	
	mat=EIGEN*I-A
	return np.linalg.inv(mat)

def constructGraph():
	cache_size=0
	for i in range(1<<N):
		vecs_prod[cache_size]=np.dot(mat_inv, vecs[i])
		res=np.dot(vecs_prod[cache_size], vec_j)
		
		if abs(res+1) < EPS:
			res=np.dot(vecs_prod[cache_size], vecs[i])
			
			if abs(res-EIGEN) < EPS:
				verts[cache_size] = vecs[i]
				cache_size += 1
	A=np.zeros((cache_size, cache_size))
	
	for i in range(1, cache_size):
		for j in range(i):
			res=np.dot(vecs_prod[i], verts[j])
			
			if abs(res) <= EPS or abs(res+1) <= EPS:
				A[i,j]=1
				A[j,i]=1
	return nx.to_graph6_bytes(nx.Graph(A), header=False)
	
def init_vectors():
	for i in range(1<<N):
		for j in range(N):
			if i & (1<<j):
				vecs[i,j]=1

init_vectors()

filepath=sys.argv[1] #save input filepath
with open('output.g6', 'wb') as op: #create output file
	with open(filepath, 'rb') as fp: #open input file
		s=fp.readline()
		while s:
			mat_inv=stringtomat(s.strip())
			op.write(constructGraph())
			s=fp.readline()
