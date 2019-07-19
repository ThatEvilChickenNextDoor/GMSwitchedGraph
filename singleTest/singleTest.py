import sys
import time
import numpy as np
import networkx as nx
from numba import jit, prange

EIGEN=2
N=19
EPS=0.000001

#@jit(nopython=True, parallel=True)
def calculate(M,vecs):
	cache_size=0
	verts=np.empty((2, 1<<N, N))
	j=np.ones(N)

	for i in range(len(vecs)):

		bilin=np.dot(M, vecs[i])

		if abs(np.dot(vecs[i], bilin)-EIGEN)<EPS and abs(np.dot(j, bilin)+1)<EPS:
			verts[0][cache_size]=vecs[i]
			verts[1][cache_size]=bilin
			#print(cache_size, vecs[i])
			cache_size+=1
	#print(verts[0][50], verts[1][50])
	return (verts, cache_size)

def construct(verts, cache_size):
	A=np.zeros((cache_size, cache_size))
	#print(verts[0][50], verts[1][50])
	for i in range(1, cache_size):
		for j in range(i):
			print(i, verts[0][i], j, verts[1][j])
			if abs(np.dot(verts[1][i], verts[0][j])) < EPS or abs(np.dot(verts[1][i], verts[0][j])+1) < EPS:
				A[i,j]=1
				A[j,i]=1
	return A
tic=time.time() #record time at beginning

if len(sys.argv) != 2: #check if argument is given
	print('expect one input')
	sys.exit()
	
filepath=sys.argv[1] #save input filepath
toTest=list()
with open(filepath, 'rb') as fp: #open input file
	s=fp.readline()
	while s:
		toTest.append(nx.from_graph6_bytes(s.strip()))
		s=fp.readline()
with open('output.g6', 'wb') as op: #create output file
	iter=[np.fromiter(("{0:b}".format(i).zfill(N)), 'float') for i in range (2**N)] #create vectors to test
	vecs=np.asarray(iter)
	for G in toTest: #test which vecs are in compatibility graph of G
		A=nx.to_numpy_array(G)
		M=np.linalg.inv(EIGEN*np.identity(N)-A)
		results=calculate(M, vecs)
		verts, cache_size = results
		#out=np.empty((2, cache_size, N))
		#print(verts[0][50], verts[1][50])
		#out[0]=np.resize(verts[0],(cache_size, N))
		#out[1]=np.resize(verts[1],(cache_size, N))
		#print(verts[0][50], verts[1][50])
		#print(verts)
		#print(verts[0])
		#print(verts[1])
		outgraph=nx.Graph(construct(verts, cache_size))
		print(nx.to_graph6_bytes(outgraph, header=False))
		#op.write(nx.to_graph6_bytes(construct(verts, vecs_prods), header=False))

toc=time.time()-tic #calculate running time
print(toc)