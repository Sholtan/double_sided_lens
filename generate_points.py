import numpy as np
import matplotlib.pyplot as plt 


n = 2000

rng = np.random.default_rng()

angles = 2*np.pi * rng.random((n,))
rs = 410* rng.random((n,))

x = []
y = []

for i in range(n):
	x.append(rs[i] * np.cos(angles[i]))
	y.append(rs[i] * np.sin(angles[i]))


ax = plt.subplot()

ax.scatter(x, y)
ax.axis('equal')
plt.show()