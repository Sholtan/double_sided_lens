import numpy as np
import matplotlib.pyplot as plt 




rng = np.random.default_rng()






def generate_points(n):
	x_square = (rng.random((n,)) - 0.5)*820.
	y_square = (rng.random((n,)) - 0.5)*820
	x = []
	y = []
	r_in = []
	count = 0
	for i in range(n):
		r = np.sqrt(x_square[i]*x_square[i] + y_square[i]*y_square[i])
		if r < 410.:
			x.append(x_square[i])
			y.append(y_square[i])
			r_in.append(r)
			count+=1
	return (x, y, r_in, count)


#x = []
#y = []

#for i in range(n):
#	x.append(rs[i] * np.cos(angles[i]))
#	y.append(rs[i] * np.sin(angles[i]))


#ax = plt.subplot()

#ax.scatter(x, y)
#ax.axis('equal')
#plt.show()
