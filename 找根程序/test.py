import numpy as np
f = lambda x: x - np.cos(x)
dfdx = lambda x: 1 + np.sin(x)
g = lambda x: np.cos(x)
p0 = 1
Nmax = 20
p = np.float64(0.73908513321516064165531207047)

print(f(p))
print(g(p))