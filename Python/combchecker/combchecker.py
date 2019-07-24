from itertools import combinations
import numpy as np
import networkx as nx
print('imports complete')
regen=np.load('regenerate.npy')
seeds = np.asarray((
((1,)*4+(0,)*8)*3,
((0,)*4+(1,)*4+(0,)*4)*3,
((0,)*8+(1,)*4)*3#,
#(0,)*8+(1,)*4+(0,)*4+(1,)*4+(0,)*4+(1,)*4+(0,)*8,
#(0,)*4+(1,)*4+(0,)*4+(1,)*4+(0,)*16+(1,)*4,
#(1,)*4+(0,)*16+(1,)*4+(0,)*4+(1,)*4+(0,)*4
), 'uint8')
print('seeds generated')
combs = list(combinations(range(12),4))
l = len(combs)
comb_vecs=np.zeros((l, 12), 'uint8')
for i in range(l):
	for pos in combs[i]:
		comb_vecs[i, pos]=1
print('combinations generated')
first = np.repeat(comb_vecs, l**2, axis=0)
second = np.tile(
np.repeat(comb_vecs, l, axis=0),
(l,1))
third = np.tile(comb_vecs, (l**2, 1))
print('arrangements generated')
vecs = np.block([first, second, third])
print('arrangement complete')
del(first)
del(second)
del(third)
print('cleaned up')

for i in range(len(regen)):
	s=np.block([[seeds],[regen[i]]])
	comp = np.dot(vecs, s.T)
	print('comparison generated')
	mask = np.all(np.isin(comp, (4)), axis=1)
	print('mask generated')
	#np.save('output', vecs[mask])
	print(len(vecs[mask]), i)

print('done')