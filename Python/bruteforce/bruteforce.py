import sys
import numpy as np
import networkx as nx

EIGEN=2
N=19
MEM=26
EPS= 0.000001

mat=np.empty((N,N), 'uint8')
mat_inv=np.empty_like(mat)

vecs=np.empty((1<<MEM,N), 'uint8')
vecs_prod=np.empty_like(vecs, 'float')
verts=np.empty_like(vecs, 'uint8')
vec_j=np.ones(N)
v=np.empty(N, 'uint8')
counter=0

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
			print('got one', cache_size)
			return 1
	return 0

#def findVerts():
#	cache_size=0
	#print('processing candidate vectors')
#	for i in range(1<<N):
#		vecs_prod[cache_size]=np.dot(mat_inv, vecs[i])
#		res=np.dot(vecs_prod[cache_size], vec_j)
#		if abs(res+1) < EPS:
#			res=np.dot(vecs_prod[cache_size], vecs[i])
#			if abs(res-EIGEN) < EPS:
#				verts[cache_size] = vecs[i]
#				cache_size += 1
#	return cache_size

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
	
#def init_vectors():
#	for i in range(1<<N):
#		for j in range(N):
#			if i & (1<<j):
#				vecs[i,j]=1

def nextV():
	global v
	global counter
	if counter < 1<<N:
		v=np.zeros(N, 'uint8')
		for i in range(N):
			if np.bitwise_and(counter, 1<<i):
				v[i]=1
		counter += 1
		return True
	return False

#print('initializing vectors')
#init_vectors()

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
			cache_size=0
			while nextV():
			#for v in vecs:
				#print(v)
				if counter % 10000 == 0:
					print(counter, '/', 1<<N)
				cache_size += checkVert(v, cache_size)
			A=constructGraph(cache_size)
			op.write(nx.to_graph6_bytes(nx.Graph(A), header=False))
			counter=0
			s=fp.readline()
