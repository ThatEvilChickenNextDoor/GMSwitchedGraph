import sys
import numpy as np
import networkx as nx
from itertools import combinations
import numba

EIGEN=2
N=19
EPS= 0.000001
EXPECTED_CLIQUE=57

mat=np.empty((N,N), 'uint8')
mat_inv=np.empty_like(mat)

vecs_prod=np.empty((1<<N,N))
verts=np.empty_like(vecs_prod)

vec_j=np.ones(N)

#seeds = np.asarray((
#(1,0,1)+(0,)*11+((1,)*4+(0,)*8)*3,
#(1,0,1)+(0,)*11+((0,)*4+(1,)*4+(0,)*4)*3,
#(1,0,1)+(0,)*11+((0,)*8+(1,)*4)*3#,
#(0,)*8+(1,)*4+(0,)*4+(1,)*4+(0,)*4+(1,)*4+(0,)*8,
#(0,)*4+(1,)*4+(0,)*4+(1,)*4+(0,)*16+(1,)*4,
#(1,)*4+(0,)*16+(1,)*4+(0,)*4+(1,)*4+(0,)*4
#), 'uint8')

def stringtomat(s):
	I=np.identity(N)
	A=nx.to_numpy_array(nx.from_graph6_bytes(s))
	mat=EIGEN*I-A
	return np.linalg.inv(mat)

@numba.jit(nopython=True, fastmath=True)
def checkVert(v, mat_inv):
	#print(v)
	prod=np.dot(mat_inv, v)
	res=np.dot(prod, vec_j)
	if abs(res+1) < EPS:
		res=np.dot(prod, v)
		if abs(res-EIGEN) < EPS:
			return v, prod
	return np.array([2.]), np.zeros(1)

@numba.jit(nopython=True)
def constructGraph(cache_size, vecs_prod, verts):
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

@numba.jit(nopython=True)
def vecgen():
	for i in range(1<<N):
		vec=np.zeros(N)
		for j in range(N):
			if i & (1<<j):
				vec[j]=1
		yield vec

def combgen():
	top=np.array((1,0,0), 'uint8')
	header=np.identity(11, 'uint8')
	combs=list(combinations(range(12),4))
	comb_vecs=np.zeros((len(combs), 12), 'uint8')
	for i in range(len(combs)):
		for pos in combs[i]:
			comb_vecs[i, pos]=1
		for head in header:
			for first in comb_vecs:
				for second in comb_vecs:
					for third in comb_vecs:
						yield np.concatenate((top,head,first,second,third))

filepath=sys.argv[1] #save input filepath
with open(filepath, 'rb') as fp: #create output file
	with open(filepath + '.out', 'wb') as op: #open input file
		s=fp.readline()
		while s:
			mat_inv=stringtomat(s.strip())
			cache_size=0
			gen=vecgen()
			for idx, v in enumerate(gen):
				results = checkVert(v, mat_inv)
				if not np.array_equiv(results[0], np.array([2.])):
					verts[cache_size], vecs_prod[cache_size] = results
					cache_size += 1
				if idx % 10000 == 0:
					print(idx, '/', 1<<N, '\t', round(idx*100/(1<<N),10), '%', '\t', cache_size, 'hits')
			A=constructGraph(cache_size, vecs_prod, verts)
			op.write(nx.to_graph6_bytes(nx.Graph(A), header=False))
			s=fp.readline()
