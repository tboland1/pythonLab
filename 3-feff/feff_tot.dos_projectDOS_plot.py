# file to read in FEFF data and plot the data
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import sys

## IMPORT location & script data
#from dosfeff import *
from mrsDOS import *

## hard code plotting
# import files
#filesave='/home/tara/Dropbox/Crozier Group User- Tara Boland/1-DFT/Ceria/5-gb/1-210-GB/1'
# directorypath='/home/tara/Dropbox/Crozier Group User- Tara Boland/3-FEFF/ceria/6-gb/'
# listdir=['0.0-1.4-md-O131','0.4-1.4-md-O139','1.2-1.4-dft-O144','0.2-1.4-md-O144','1.0-1.4-dft-O131','1.4-1.4-dft-O139','0.1-1.4-md-O141','0.5-1.4-md-O138','1.3-1.4-dft-O132','0.3-1.4-md-O132','1.1-1.4-dft-O141','1.5-1.4-dft-O138']
# filespace='/'
#------------------------------------------------------------
# not normally plotted - for absorbing atom
#file0=directorypath+'/ldos00.dat'
# first ATOM DOS data file
#file1=directorypath+'/ldos01.dat'
# second Atom DOS data file
#file2=directorypath+'/ldos02.dat'
# thirst Atom DOS data file
#file3=directorypath+'/ldos03.dat'
#-------------------------------------------------------------



# populated with the absolute path of each file according to each directory. 
#ref directory by [i] and each file by [i][j]


## Combine the list of files with location/file name & number of data file type ( 00, 01 etc) to sum over
file=[]
for listdirCount in range(len(listdir)):
    # store each filelist  in an array (2d data array)
    temp=[]
    for fileNum in range(len(filelist)):
        temp.append(filesave+listdir[listdirCount]+filespace+filelist[fileNum])
    file.append(temp)
    
for dirindex in range(len(listdir)):
    # initialize all variables before starting new loop | define loop parameters and data collected
    energy=[]
    s=[]
    p=[]
    d=[]  
    f=[] 
    fermi=[]
    data=[energy,s,p,d,f]
    saveplot=filesave+listdir[dirindex]+filespace
    dirfiles=file[dirindex]
    
    # Open and read the data files append data to list
    for element in dirfiles:
        fileopen=open(element)
        linecounter=0
        for line in fileopen:
            linecounter+=1
            if linecounter == 1:
                line=line.split()
                fermi.append(float(line[4]))
                #print(line)
            elif linecounter > 11:
                line=line.split()
                #print line
                energy.append(float(line[0]))
                s.append(float(line[1]))
                p.append(float(line[2]))
                d.append(float(line[3]))
                f.append(float(line[4]))
        # close file
        fileopen.close()
    
    # split the data up & add together
    eleLen=int(len(s)/len(dirfiles))
    sums=[[]]*5
    totDOS=[0]*eleLen
    counter=0
    for element in data:
        if counter == 0:
            sums[counter]=element[0:eleLen]
            counter+=1
        else :
            combo=[element[0:eleLen],element[eleLen:len(s)]]
            sums[counter]=[sum(x) for x in zip(*combo)]
            temp=[sums[counter],totDOS]
            totDOS=[sum(x) for x in zip(*temp)]
            counter+=1
    counter=0
    
    ## General notation comments here
    # \mathrm or \rm to remove non-standard font from using math library
    # https://pythonhosted.org/lineid_plot/ line id plot doc
    
    ## Plotting here!!
    # PLOT: DOS orbital projected
    yax=range(0,12,2)
    xax=range(-20,11,1)
    spanx=len(xax)
    span=len(yax)
    fig= plt.figure(figsize=(6.2,5))            # make the figure box bigger 
    plt.plot(sums[0],sums[1],label=r's DOS CeO$_{\rm 2}$')
    plt.plot(sums[0],sums[2],label=r'p DOS CeO$_{\rm 2}$')
    plt.plot(sums[0],sums[3],label=r'd DOS CeO$_{\rm 2}$')
    plt.plot(sums[0],sums[4],label=r'f DOS CeO$_{\rm 2}$')
    plt.plot([fermi[0]]*span,yax,'--',label='Fermi Level')
    plt.legend(loc='upper right')
    plt.xlim([-30,10])
    plt.yticks()
    plt.title(SCFval + r'Projected DOS: CeO$_{\rm 2}$')
    plt.xlabel(r'Energy (eV)',fontsize=14)
    plt.ylabel("Counts",fontsize=14)
    plt.minorticks_on()
    plt.grid()
    plt.show()
    filesaves=saveplot + 'feff_projected_DOS.png'
    fig.savefig(filesaves, transparent=True)
    
    fig= plt.figure(figsize=(6.2,5))            # make the figure box bigger display figure
    plt.plot(sums[0],totDOS,label=r'DOS CeO$_{\rm 2}$')
    plt.plot([fermi[0]]*span,yax,'--',label='Fermi Level')
    plt.plot(xax,[0]*spanx,color='r')
    plt.legend(loc='upper right')               # make the plot legend
    plt.xlim([-30,10])                          # the x limits
    plt.yticks()                                # add y ticks
    plt.title(SCFval + r'Total DOS: CeO$_{\rm 2}$')      # plot title
    plt.xlabel(r'Energy (eV)',fontsize=14)      # x plot label
    plt.ylabel("Counts",fontsize=14)            # y plot label
    plt.minorticks_on()                         # turn on the ticks btwn #'s
    plt.grid()
    plt.show()                                  # display the plot
    filesaves=saveplot +'feff_total_DOS.tiff'     # locations & name of figure to save
    fig.savefig(filesaves, transparent=True)     # saves the figure with a tranparent background
    sums=[]





