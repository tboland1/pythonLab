# file to read in FEFF data and plot the data
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py

# import files
#file='/home/tara/eelsMD.dat'
file='/home/tara/eelsDFT.dat'
fileenergy='/home/tara/expEELS.txt'


# define loop parameters and data collected
energy=[]
intensity=[]
energyexp=[]
intensityexp=[] # oxidized 
intGBreduced=[] # reduced GB like
linecounter=0

# open the FEFF data and read through the lines
fileopen=open(file)
for line in fileopen:
    linecounter+=1
    if linecounter >= 13:
        line=line.split()
        intensity.append(float(line[3]))
        energy.append(float(line[0]))
# close file
fileopen.close()

##! open the experimental data and read through
fileopen=open(fileenergy)
for line in fileopen:
    line=line.split()
    intensityexp.append(float(line[1]))
    intGBreduced.append(float(line[2]))
    energyexp.append(float(line[0]))
# close file
fileopen.close()

# normailze the intensity of all data
maxintEXP=max(intensityexp)
maxintGB=max(intGBreduced)
maxint=max(intensity)

intensity=[x/maxint for x in intensity]
intensityexp=[x/maxintEXP for x in intensityexp]
intGBreduced=[x/maxintGB for x in intGBreduced]

## MD intensity shift
# # shift the FEFF data
# energy=[x-1 for x in energy]
# intensityexp=[x+.8 for x in intensityexp]
# intensity=[x-.7 for x in intensity]

## DFT intensity shift
# shift the FEFF data
energy=[x for x in energy]
intensityexp=[x+.8 for x in intensityexp]
intensity=[x-.7 for x in intensity]


#! The DFT tail
def tail(list):
    return list[30:]
    
# ## for the MD tail
# def tail(list):
#     return list[30:]
    
intensity=tail(intensity)
energy=tail(energy)

##! MD EELS plot
# # plot the data together and save FEFF-MD and 
# fig= plt.figure()
# plt.plot(energyexp,intensityexp,label='Exp-Oxidized GB like')
# plt.plot(energyexp,intGBreduced,label='Exp- Reduced GB like')
# plt.plot(energy,intensity,label='FEFF-MD',color='red')
# plt.legend(loc='lower right')
# plt.xlim([530,550])
# plt.yticks([])
# plt.title("Core-Loss EELS: (210) Grain Boundary")
# plt.xlabel(r'Energy Loss (eV)',fontsize=14)
# plt.ylabel("Normalized Intensity",fontsize=14)
# plt.minorticks_on()
# plt.show()
# 
# 
# fig.savefig('210_corelossEELS-MD.png', transparent=True)


##! dft EELS plot
#plot the data together and save FEFF-MD and 
fig= plt.figure()
plt.plot(energyexp,intensityexp,label=r'Oxidized $CeO_2$')
plt.plot(energyexp,intGBreduced,label=r'Reduced CeO$_{\rm 2}$')
# or \mathrm
plt.plot(energy,intensity,label='FEFF-DFT')
plt.legend(loc='lower right')
plt.xlim([530,550])
plt.yticks([])
plt.title("Core-Loss EELS: (210) Grain Boundary")
plt.xlabel(r'Energy Loss (eV)',fontsize=14)
plt.ylabel("Normailized Intensity",fontsize=14)
plt.minorticks_on()
plt.show()


fig.savefig('210_corelossEELS-DFT.png', transparent=True)











