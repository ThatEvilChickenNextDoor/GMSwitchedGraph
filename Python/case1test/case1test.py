import sys
import time
from itertools import combinations
import numpy as np
import networkx as nx
from numba import njit

tic=time.time()

EIGEN=3
N=50
EPS= 0.000001

mat_inv=np.empty((N,N), np.float32)

vec_j=np.ones(N, np.float32)

seeds = np.array((
(1,0,1)+(0,)*11+((1,)*4+(0,)*8)*3,
(1,0,1)+(0,)*11+((0,)*4+(1,)*4+(0,)*4)*3,
(1,0,1)+(0,)*11+((0,)*8+(1,)*4)*3#,
#(0,)*8+(1,)*4+(0,)*4+(1,)*4+(0,)*4+(1,)*4+(0,)*8,
#(0,)*4+(1,)*4+(0,)*4+(1,)*4+(0,)*16+(1,)*4,
#(1,)*4+(0,)*16+(1,)*4+(0,)*4+(1,)*4+(0,)*4
), np.float32)

def stringtomat(s):
	I=np.identity(N)
	A=nx.to_numpy_array(nx.from_graph6_bytes(s))
	mat=EIGEN*I-A
	return np.linalg.inv(mat)

@njit
def constructGraph():
	cache_size=0
	verts=np.asarray(np.empty_like(vecs))
	for i in range(len(vecs)):
		if i % 10000000 == 0:
			print(i, '/', len(vecs), '\t', round(i*100/len(vecs),10), '%', '\t', cache_size, 'hits')
		v=np.asarray(vecs[i], np.float32)
		prod=np.dot(mat_inv, v)
		if abs(np.dot(prod, vec_j)+1) < EPS:
			if abs(np.dot(prod, v)-EIGEN) < EPS:
				res = np.dot(prod, seeds[0])
				if (abs(res) < EPS) or (abs(res + 1) < EPS):
					res = np.dot(prod, seeds[1])
					if (abs(res) < EPS) or (abs(res + 1) < EPS):
						res = np.dot(prod, seeds[2])
						if (abs(res) < EPS) or (abs(res + 1) < EPS):
							verts[cache_size] = vecs[i]
							cache_size += 1
	return verts[:cache_size]

filepath=sys.argv[1] #get input filepath
vecspath=sys.argv[2]
with open(filepath, 'rb') as fp: #open input file
	s=fp.readline()
	mat_inv[:]=stringtomat(s.strip())
	vecs=np.load(vecspath)
	verts=constructGraph()
	np.save('verts', verts)
print('Successfuly processed: {} vectors.'.format(len(verts)))
toc=time.time()-tic
print('Time elapsed: {} seconds'.format(round(toc, 3)))
