import sys
import time
from multiprocessing import Pool
import numpy as np
import networkx as nx

def calculate(G,vecs):
	print(id(vecs))
	return G
	
if __name__ == "__main__":
	tic=time.time() #record time at beginning
	if len(sys.argv) != 2: #check if argument is given
		print('expect one input')
		sys.exit()
	filepath=sys.argv[1] #save input filepath
	with open(filepath, 'rb') as fp: #open input file
		toTest=nx.read_graph6(fp.name)
		
	iterable=list("{0:b}".format(i).zfill(19) for i in range(2**19))
	vecs=np.asarray([np.fromiter(i, int) for i in iterable])
	pool=Pool(processes=10) #start mp pool
	toPrint = pool.starmap(calculate, [(i,vecs) for i in toTest])
	with open('output.g6', 'wb') as op: #create output file
		for G in toPrint:
			op.write(nx.to_graph6_bytes(G, header=False))
	toc=time.time()-tic #calculate running time
	print(toc)