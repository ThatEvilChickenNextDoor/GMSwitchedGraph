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

vec_j=np.ones(N)

#seeds = np.asarray((
#(1,0,1)+(0,)*11+((1,)*4+(0,)*8)*3,
#(1,0,1)+(0,)*11+((0,)*4+(1,)*4+(0,)*4)*3,
#(1,0,1)+(0,)*11+((0,)*8+(1,)*4)*3#,
#(0,)*8+(1,)*4+(0,)*4+(1,)*4+(0,)*4+(1,)*4+(0,)*8,
#(0,)*4+(1,)*4+(0,)*4+(1,)*4+(0,)*16+(1,)*4,
#(1,)*4+(0,)*16+(1,)*4+(0,)*4+(1,)*4+(0,)*4
#), np.uint8)

def stringtomat(s):
	I=np.identity(N)
	A=nx.to_numpy_array(nx.from_graph6_bytes(s))
	mat=EIGEN*I-A
	return np.linalg.inv(mat)

@njit(cache=True)
def constructGraph():
	cache_size=0
	verts=np.empty_like(vecs)
	for i, v in enumerate(vecs):
		if i % 10000 == 0:
			print(i, '/', len(vecs), '\t', round(i*100/len(vecs),10), '%', '\t', cache_size, 'hits')
		prod=np.dot(mat_inv, v)
		res=np.dot(prod, vec_j)
		if abs(res+1) < EPS:
			res=np.dot(prod, v)
			if abs(res-EIGEN) < EPS:
				verts[cache_size] = v
				cache_size += 1
	return verts

@njit(cache=True)
def combgen(comb):
	top=np.array((1,0,0))
	out=np.empty((11*495**3,50), np.uint8)
	comb_vecs=np.zeros((495,12), np.uint8)
	header=np.identity(11, np.uint8)
	for idx, nums in enumerate(comb):
		for n in nums:
			comb_vecs[idx, n]=1
	for head in range(11):
		for first in range(495):
			for second in range(495):
				for third in range(495):
					out[third + second*495 + first*495**2 + head*495**3]=np.concatenate((top,header[head],comb_vecs[first],comb_vecs[second],comb_vecs[third]))
			if first % 50 == 0:
				print(head, round(first*100/495,3))
	print('done')
	return out

comb=tuple(combinations(range(12),4))
vecs=combgen(comb)

filepath=sys.argv[1] #get input filepath
with open(filepath, 'rb') as fp: #open input file
	s=fp.readline()
	mat_inv[:]=stringtomat(s.strip())
	verts=constructGraph()
	np.save('verts', verts)
print('Successfuly processed: {} vectors.'.format(len(verts))
toc=time.time()-tic
print('Time elapsed: {} seconds'.format(round(toc, 3)))
