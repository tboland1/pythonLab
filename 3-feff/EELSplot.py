
# file to read in FEFF data and plot the data
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import sys
from matplotlib.ticker import FuncFormatter, MaxNLocator
## IMPORT VARIABLE PARAMETERS#
#from compressionEELSData import *              # plot of all uni,bi,hydrostatic compression eels data
#from compressiveEELSData import *              # plot of just hydrostatic compressive eels data
#from tenscompnormEELSData import *              # plot of normal tensile and compressive eels data
#from normalEELSData import *                   # plot of just the normal eels data
#from eelmrsplot import *
#from mrsOsiteMissingeels import *

## manually enter the file path
#file='/home/tara/eelsMD.dat'
from mrsexpeels import *

#from normalEELSData import *

##
#fileloc='/home/tboland1/Dropbox/Crozier Group User- Tara Boland/1-DFT/Ceria/5-gb/1-210-GB/'
#files=['2-49/eels.dat','3-47/eels.dat','4-13/eels.dat']
#files=['/home/tboland1/eelsnormal.dat','/home/tboland1/eelscadopedce.dat','/home/tboland1/eelsexp.txt']

##
filecount=0
filenumber=len(files)
flag=1
energy=[]
intensity=[]
for file in files:
    
    file = fileloc + file
    # define loop parameters and data collected
    linecounter=0
    tempINT=[]
    tempINTGB=[]
    tempENERGY=[]
    # FEFF calculated data
    if filecount < filenumber:
        fileopen=open(file)
        for line in fileopen:
            linecounter+=1
            if linecounter >= 13:
                line=line.split()
                tempINT.append(float(line[1]))
                tempENERGY.append(float(line[0]))
        fileopen.close()
    
    # experimental data
    if flag == 1 and filecount == len(files)-1:
        fileopen=open(file)
        for line in fileopen:
            line=line.split()
            tempINT.append(float(line[1]))
            tempENERGY.append(float(line[0]))
        fileopen.close()

    
    # reset file number and append data
    filecount+=1
    intensity.append(tempINT) 
    energy.append(tempENERGY)

# normailze the intensity of all data
normINT=[]
for int in intensity:
    tempint=[x/max(int) for x in int]
    normINT.append(tempint)
    tempINT=[]

    
## displacement along the normalized axis y
for i in range(len(energy)):
    # if plot with exp data shift the energy to match exp
    if flag == 1 and i == len(energy)-1:
        energy[i]=[x for x in energy[i] ]
    # shift the EELS by disp up the y axis
    normINT[i]=[x-disp[i] for x in normINT[i] ]

## PLOT
fig= plt.figure()
for i in range(len(normINT)-1):
    
    plt.plot(energy[i],normINT[i],color=colors[i])#,label=labels[i])
# or \mathrm:

ax = fig.add_subplot(111)
plt.xlim([530,550])
plt.ylim([-0.069948461393528311, 1.5747594505425491])     
plt.yticks([])
#plt.title(plottitle)
plt.xlabel(r'Energy Loss (eV)',fontsize=14)
plt.ylabel("Normalized Intensity (Arb Units)",fontsize=14)
plt.legend(loc='lower right',frameon=True)
plt.xticks(fontsize=12)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.minorticks_on()
plt.show()
store=filesave+figurename
fig.savefig(store, transparent=True)
    


#=========================================================================================
## MD intensity shift
# # shift the FEFF data
# energy=[x-1 for x in energy]
# intensityexp=[x+.8 for x in intensityexp]
# intensity=[x-.7 for x in intensity]

## DFT intensity shift
# shift the FEFF data
#energy=[x for x in energy]
#intensityexp=[x+.8 for x in intensityexp]
#intensity=[x-.7 for x in intensity]


#! The DFT tail
#def tail(list):
#    return list[30:]
    
# ## for the MD tail
# def tail(list):
#     return list[30:]
#intensity=tail(intensity)
#energy=tail


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