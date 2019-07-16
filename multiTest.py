import sys
import time
from multiprocessing import Pool
import numpy as np
import networkx as nx

def calculate(g6):
	pass
	
if __name__ == "__main__":
	tic=time.time() #record time at beginning
	if len(sys.argv) != 2: #check if argument is given
		print('expect one input')
		sys.exit()
	filepath=sys.argv[1] #save input filepath
	with open(filepath, 'rb') as fp: #open input file
		toTest=nx.read_graph6(fp.name)
	with open('output.g6', 'wb') as op: #create output file
		for G in toTest:
			op.write(nx.to_graph6_bytes(G, header=False))
	toc=time.time()-tic #calculate running time
	print(toc)