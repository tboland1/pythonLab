import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import math
from matplotlib.ticker import MaxNLocator


hop_count=np.linspace(1,11,11)
r_o_normalized=[-0.1481245663,-0.1144011935,-0.1847672446,0.04017416236,-0.1630698067,0.9999999999,0.9999999999,0.08287602452,-0.04990312141,-0.09554201348,-0.1652227039]
E_mig_normalized=[0.09363321799,0.07598615917,0.1492041522,-0.003529411765,-0.3821453287,0.2339792388,1,0.5724567474,0.2794463668,0.1609688581,0.1499653979]
ce_within_rc=[3,7,10,10,13,13,14,10,10,8,6]

#print(hop_count,r_o_normalized,E_mig_normalized)


## plot activation energy and change in lat constant
y=[r_o_normalized,E_mig_normalized]
x=[hop_count,hop_count]
## plot the 0.0 line guide
x1=np.linspace(1,11,11)
y1=[0]*11

fig = plt.figure()

# the plotting functions
# line guide
plt.plot(x1,y1,color='red',linestyle='dashed')
# ce-ce interatomic distance
plt.plot(hop_count,r_o_normalized,marker='*',markersize=12,linestyle='',color='red',label=r'r $^{Ce-Ce}_{o}$')
# the migration energy
plt.plot(hop_count,E_mig_normalized,marker='D',markersize=6,linestyle='',color='blue',label=r'E $_{migration}$')

# the graph display settings
plt.legend(loc='upper right',fontsize=16)
ax = plt.axes()
plt.xticks([1*i for i in x1],fontsize=16) 
plt.yticks(fontsize=16)

plt.tight_layout()
fig.show()
fig.savefig("activation_e-ce_ce_bond_distance.png", transparent=True,figsize=(30,30))


fig = plt.figure()

## ce3+ wihtin r_c
plt.plot(hop_count,ce_within_rc,marker='^',markersize=8,linestyle='',color='blue',label=r'Ce $^{3+}$')

plt.xticks([1*i for i in x1],fontsize=16)
plt.yticks([1*i for i in range(1,15)],fontsize=16)
plt.legend(loc='upper right',fontsize=16)
ax = plt.axes()
 

plt.tight_layout()
fig.show()
fig.savefig("ce_within_rc.png", transparent=True,figsize=(30,30))










