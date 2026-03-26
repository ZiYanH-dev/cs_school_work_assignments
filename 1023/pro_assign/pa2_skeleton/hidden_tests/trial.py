import numpy as np

arr=np.array([1,2,3],)
a=np.array([1,2,3])

a2=np.array([[1,2,1],[3,2,4]])

shape=a2.shape
newarr=np.full(shape,True)
newarr2=np.full_like(a2,True)


print(arr is None,)
if arr is None:
    1