import sys
import os
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import math

## intitial bond distances
obond1_i=[9.94432, 18.7512, 5.74135]
obond2_i=[9.94432,18.7512,1.91378]
obond3_i=[13.2591,18.7512,0]
obond4_i=[16.5739,18.7512,1.91378]
obond5_i=[16.5739,18.7512,5.74135]
obond6_i=[13.2591,18.7512,7.65514]

# O vacancy location
ovacbond=[13.2591, 18.7512, 3.82757]
ovacnumber=[1,2,3,4,5,6]
## final bond distances
obond1_f=[9.77384,18.9028,5.91097]
obond2_f=[9.74851,18.8673,1.73793]
obond3_f=[13.376,18.8538,(15.1631-15.3103)]
obond4_f=[16.6657,18.8517,1.7425]
obond5_f=[16.8333,18.8698,5.80708]
obond6_f=[13.1968,18.9017,7.86962]


obond_f=[obond1_f,obond2_f,obond3_f,obond4_f,obond5_f,obond6_f]
obond_i=[obond1_i,obond2_i,obond3_i,obond4_i,obond5_i,obond6_i]


# print original bond distance
disp_bond_init=np.power(  np.sum(np.power(np.subtract(ovacbond,obond1_i),2))    ,0.5)
print(('The original bond distance is ', disp_bond_init))

## get the change in the O atoms from the 
# take sqrt(x^2+y^2+z^2)
for (element,ovac) in zip(obond_f,ovacnumber):    
    change_bond=np.power(    np.sum(np.power(    np.subtract(element,ovacbond)  ,2))   ,0.5)
    print(('The new bond distance is ', change_bond, ' for oxygen atom', ovac))
print('')


start=list(range(0,6))
stagger=(list(range(1,6)))
stagger.append(0)
#stagger=[1,2,3,4,5,0]
counter=0
for (i,f) in zip(start,stagger):
    o_o_bonds=np.power(    np.sum(np.power(    np.subtract(obond_i[i],obond_f[f])  ,2))   ,0.5)
    print(('The new bond distance is ', o_o_bonds))
    print(('The oxygen atoms are', i+1, 'and ', f+1))
    counter+=1