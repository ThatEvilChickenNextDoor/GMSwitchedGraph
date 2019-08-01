import sys
import numpy as np
import networkx as nx
from itertools import combinations

EIGEN=3
N=50
MEM=26
EPS= 0.000001

mat=np.empty((N,N), 'uint8')
mat_inv=np.empty_like(mat)

vecs=np.empty((1<< min(N,MEM),N), 'uint8')
vecs_prod=np.empty_like(vecs, 'float')
verts=np.empty_like(vecs, 'uint8')
vec_j=np.ones(N)
v=np.empty(N, 'uint8')

seeds = np.asarray((
(1,0,1)+(0,)*11+((1,)*4+(0,)*8)*3,
(1,0,1)+(0,)*11+((0,)*4+(1,)*4+(0,)*4)*3,
(1,0,1)+(0,)*11+((0,)*8+(1,)*4)*3#,
#(0,)*8+(1,)*4+(0,)*4+(1,)*4+(0,)*4+(1,)*4+(0,)*8,
#(0,)*4+(1,)*4+(0,)*4+(1,)*4+(0,)*16+(1,)*4,
#(1,)*4+(0,)*16+(1,)*4+(0,)*4+(1,)*4+(0,)*4
), 'uint8')

def stringtomat(s):
	I=np.identity(N)
	A=nx.to_numpy_array(nx.from_graph6_bytes(s))
	mat=EIGEN*I-A
	return np.linalg.inv(mat)


def checkVert(v, cache_size):
	#print(v)
	vecs_prod[cache_size]=np.dot(mat_inv, v)
	res=np.dot(vecs_prod[cache_size], vec_j)
	if abs(res+1) < EPS:
		res=np.dot(vecs_prod[cache_size], v)
		if abs(res-EIGEN) < EPS:
			verts[cache_size] = v
			#print('got one', cache_size)
			return 1
	return 0

def constructGraph(cache_size):
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

filepath=sys.argv[1] #save input filepath
with open(filepath, 'rb') as fp: #create output file
	with open(filepath + '.out', 'wb') as op: #open input file
		s=fp.readline()
		while s:
			mat_inv=stringtomat(s.strip())
			
			#print('initializing vectors')
			top=np.array((1,0,0), 'uint8')
			header=np.identity(11, 'uint8')
			combs=list(combinations(range(12),4))
			comb_vecs=np.zeros((len(combs), 12), 'uint8')
			for i in range(len(combs)):
				for pos in combs[i]:
					comb_vecs[i, pos]=1
			
			#print('checking vectors')
			cache_size=0
			counter=0
			for head in header:
				for first in comb_vecs:
					for second in comb_vecs:
						for third in comb_vecs:
							v=np.concatenate((top,head,first,second,third))
							cache_size += checkVert(v, cache_size)
					counter+=1
					print(counter*len(combs)**2, '/', len(combs)**3*11, '\t', round(counter*len(combs)**2/len(combs)**3*11,10), '%', '\t', cache_size, 'hits')
			A=constructGraph(cache_size)
			op.write(nx.to_graph6_bytes(nx.Graph(A), header=False))
			counter=0
			s=fp.readline()
