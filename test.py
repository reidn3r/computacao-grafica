import numpy as np

a = np.array([[1,3],[7,2],[5,5]])
b = np.array([[2,0],[0,2]])
c = np.array([[1,2],[3,4]])

print(np.dot(a,b))
print(c.T)

for i, j in c:
    print(i, j)