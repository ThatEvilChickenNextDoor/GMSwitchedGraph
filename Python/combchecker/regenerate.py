import numpy as np

un=np.load('unique.npy')
q=np.load('q.npy')

temp=np.empty(36, 'uint8')
out=np.empty((664,3,36), 'uint8')

def regenerate(n, flip=False):
	counter = 0
	for p in un[n]:
		if not flip:
			for i in range(p):
				temp[counter]=1
				counter+=1
		for i in range(4-p):
			temp[counter]=0
			counter+=1
		if flip:
			for i in range(p):
				temp[counter]=1
				counter+=1
				
for i in range(len(q)):
	regenerate(q[i,0])
	out[i,0]=temp
	regenerate(q[i,1], True)
	out[i,1]=temp
	out[i,2]=np.ones(36)-out[i,0]-temp
np.save('regenerate', out)