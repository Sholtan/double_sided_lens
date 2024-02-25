
import numpy as np


n = 1.5025
R1 = 1900
R2 = -1900
d = 100



f = (n - 1) * (1/R1 - 1/R2 + (n - 1)*d/(n * R1 * R2))
f = 1/f
print('f: ', f)