# This file is made to fit the bulk modulus data from the shell script file 
# called bulkmod.sh. The data file generated from this is read and fit to 
# the Birch Murnigahan Equation of State. You must supply the file with an
# appropriate guess for a0 to get the fitting to start.

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import normal
from scipy.optimize import curve_fit
from scipy.optimize import fmin
import math

## import the latice constant vs energy, give a0 guess
#path_to_file = 
#y_data = (-92.2633,-96.7030,-97.8697,-97.8931,-96.8223);
#x_data = (5.1000,5.3000,5.4640,5.5000,5.7000);
y_data = (-87.570846, -94.317084, -97.168428, -97.492224, -97.493942, -96.537746, -93.999292);
x_data = (5.0,5.2,5.4,5.494,5.5,5.7,5.9);
a0=5.494;

# define the equation of state Birch Murnaghan
def func(x, b0, b01,E0):
    return E0 + 9*a0**3*b0/(16) *( ((a0/x)**2 -1)**3*b01 + ((a0/x)**2-1)**2*(6 - 4*(a0/x)**2) );

# pass the parameters to the curve_fit func & define output
parameter, covariance_matrix = curve_fit(func, x_data, y_data);

# set up graph: data points and curve fit input defined as x
x = np.linspace(5.0,5.95,50);
plt.plot(x_data, y_data, 'rx', label='data');
plt.plot(x, func(x, *parameter), 'b-', label='fit');  # the star is to unpack the parameter array
plt.show()

# initialize the returned parameters from minimization of equation
b0=parameter[0];
E0=parameter[2];
b01=parameter[1];

# check if the E0 and the equation agree with each other: Self Consisitency
def f(x):
    Energy = E0 + 9*a0**3*b0/(16) *( ((a0/x)**2 -1)**3*b01 + ((a0/x)**2-1)**2*(6 - 4*(a0/x)**2) )
    return E0 + 9*a0**3*b0/(16) *( ((a0/x[0])**2 -1)**3*b01 + ((a0/x[0])**2-1)**2*(6 - 4*(a0/x[0])**2) )
    
E_sc = func(a0,b0,b01,E0)
fmin(f,np.array([0,0]))
print 'Bulk modulus (eV/A^3) =', parameter[0]
print 'Bulk Modulus (GPa) =', 160.217*parameter[0]
print 'Equilibrium Energy (eV) = ', E0
print 'Equilibrium Energy by BM EOS (eV) =',E_sc
print 'Done'
