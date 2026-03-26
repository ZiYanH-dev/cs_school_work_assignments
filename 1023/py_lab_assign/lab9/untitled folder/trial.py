import numpy as np

sample_l=[1,2,3]
arr=np.arange(1,4)
a=np.array([1,2,2.,5.])
two_d=np.array([[1,2,2],[3,4,1]])
padded2=np.pad(two_d,((1,1),(1,1)),mode='edge',)

print(a.reshape(2,2))
print(arr.astype(np.int32)+arr)