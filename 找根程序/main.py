"""
MATH2019 CW1 main script

@author: Kris van der Zee (lecturer)
"""



#%% Question 2

# import numpy as np
# import matplotlib.pyplot as plt
# import rootsolvers as rs
 
# # Initialise
# f = lambda x: x**3 + x**2 - 2*x - 2
# a = 1
# b = 2
# Nmax = 5
#
# # Run bisection
# p_array = rs.bisection(f,a,b,Nmax)
#
# # Print output
# print(p_array)



#%% Question 3

import numpy as np
import rootsolvers as rs

# Print help description
help(rs.fp_iteration)

# Initialise
g = lambda x: 1 - 1/2 * x**2
p0 = 1
Nmax = 15

# Run fixedpoint_iteration
p_array = rs.fp_iteration(g,p0,Nmax)

# Print output
print(p_array)



#%% Question 4

import numpy as np
import rootsolvers as rs

# Print help description
help(rs.fp_iteration_stop)

# Initialise
g = lambda x: 1 - 1/2 * x**2
p0 = 1
Nmax = 50
TOL = 10**(-3)

# Run method
p_array, pdiff_array = rs.fp_iteration_stop(g,p0,Nmax,TOL)

# Print output
print(p_array)
print(pdiff_array)


#%% Question 5

import numpy as np
import rootsolvers as rs

# Print help description
help(rs.newton_stop)

# Initialise
f = lambda x: np.cos(x) - x
dfdx = lambda x: -np.sin(x) - 1
p0 = 1 
Nmax = 6
TOL = 10**(-16)

# Run method
p_array = rs.newton_stop(f,dfdx,p0,Nmax,TOL)

# Print output
print(p_array)



#%% Question 6


import numpy as np
import matplotlib.pyplot as plt 
import rootsolvers as rs

# Initialise 
f = lambda x: x - np.cos(x)
dfdx = lambda x: 1 + np.sin(x)
g = lambda x: np.cos(x)
p0 = 1
Nmax = 20
p = np.float64(0.73908513321516064165531207047)

# Plot convergence
fig, ax = rs.plot_convergence(p,f,dfdx,g,p0,Nmax)




#%% Question 7

import numpy as np
import rootsolvers as rs

# Initialise
f = lambda x: np.cos(x) - x
p0 = 1 
Nmax = 5
TOL = 10**(-14)

# Run method
p_array = rs.steffensen_stop(f,p0,Nmax,TOL)

# Print output
print(p_array)


#%% Question 8

import numpy as np
import matplotlib.pyplot as plt 
import rootsolvers as rs

# Initialise 
f = lambda x: x - np.cos(x)
dfdx = lambda x: 1 + np.sin(x)
g = lambda x: np.cos(x)
p0 = 1
Nmax = 20
p = np.float64(0.73908513321516064165531207047)

# Plot convergence
fig, ax = rs.plot_convergence3(p,f,dfdx,g,p0,Nmax)
plt.show()




