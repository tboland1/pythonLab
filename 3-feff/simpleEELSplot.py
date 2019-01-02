## plot each eels.dat data file by itself and save in the respective directory

import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import sys
from matplotlib.ticker import FuncFormatter, MaxNLocator
#from eelsGBfeff import *
from eelsGBEXPMRS import *

##
file=[]
for listdirCount in range(len(listdir)):
    # store each filelist  in an array (2d data array)
    temp=[]
    for fileNum in range(len(filelist)):
        temp.append(filesave+listdir[listdirCount]+filespace+filelist[fileNum])
    file.append(temp)

for dirindex in range(len(listdir)):
    filecount=0
    filenumber=len(filelist)
    energy=[]
    intensity=[]
    dirfiles=file[dirindex]
    saveplot=filesave+listdir[dirindex]+filespace
    for element in dirfiles:
        linecounter=0
        tempINT=[]
        tempINTGB=[]
        tempENERGY=[]
        # FEFF calculated data
        if filecount < filenumber:
            fileopen=open(element)
            for line in fileopen:
                linecounter+=1
                if linecounter >= 13:
                    line=line.split()
                    tempINT.append(float(line[1]))
                    tempENERGY.append(float(line[0]))
            fileopen.close()
        
        # experimental data
        if flag == 1:
            file=filenumber-1
            fileopen=open(element)
            for line in fileopen:
                line=line.split()
                tempINT.append(float(line[1]))
                tempINTGB.append(float(line[2]))
                tempENERGY.append(float(line[0]))
            fileopen.close()
            intensity.append(tempINTGB)
        
        # reset file number and append data
        filecount+=1
        intensity.append(tempINT) 
        energy.append(tempENERGY)
        
    normINT=[]
    for int in intensity:
        tempint=[x/max(int) for x in int]
        normINT.append(tempint)
        tempINT=[]    
    for i in range(len(energy)):
        # if plot with exp data shift the energy to match exp
        if flag == 1 and i == len(energy)-1:
            energy[i]=[x for x in energy[i] ]
        # shift the EELS by disp up the y axis
        normINT[i]=[x-disp[i] for x in normINT[i] ]    
    
    ## PLOT
    fig= plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(normINT)-1):
        # if i == 1:
        #     plt.plot(energy[i],normINT[i],label=labels[i],color=colors[i])
        # run throug all the intensities which were normalized and plot together
        plt.plot(energy[i],normINT[i],label=labels[i],color=colors[i])
    # or \mathrm    
    plt.xlim([min(energy[0])-1,max(energy[0])+1])
    plt.yticks([])
    plt.title(plottitle)
    plt.xlabel(r'Energy Loss (eV)',fontsize=14)
    plt.ylabel("Normalized Intensity (Arb Units)",fontsize=14)
    plt.legend(loc='lower right',frameon=True)
    plt.minorticks_on()
    plt.show()
    store=saveplot+figurename
    fig.savefig(store, transparent=True)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    
    
    
    
    
    
    