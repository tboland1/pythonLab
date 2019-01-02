# file to read in FEFF data and plot the data
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py

## Enter the data files to be read
files=['/home/tboland1/DOSCAR']
filenumber=len(files)
# systemName gets the system name from DOS
# atoms -- pulls the total number of atoms from the cell
# fermi -- tells you the fermi level 
# Emin -- the energy min of the plot
# Emax -- the energy max of the plot

## plotting variables
labels=['Up DOS','Down DOS','Up Integrated DOS','Down Integrated DOS','Fermi Level']
colors=['red','blue','green','black','gray']
figurenames=['Total-DOS.png','integrated-DOS.png']
plottitle="VASP DOS"
ybounds=[0,120]

## variable to store the data
energy=[]*filenumber
upDOS=[]*filenumber
downDOS=[]*filenumber
intupDOS=[]*filenumber
intdownDOS=[]*filenumber

## code to read and store data
filecount=0
for file in files:
    # LOOP OVER ALL THE FILES
    linecounter=0
    tempupDOS=[]
    tempdownDOS=[]
    tempintupDOS=[]
    tempintdownDOS=[]
    tempEN=[]
    # APPEND DATA FROM EACH LINE IN ONE FILE
    if filecount < filenumber:
        fileopen=open(file)
        for line in fileopen:
            linecounter+=1
            if linecounter == 1:
                line=line.strip()
                line=line.split()
                atoms=line[0]
            if linecounter == 5:
                systemName=line.strip()
                plottitle=plottitle+systemName
            if linecounter == 6:
                line=line.strip()
                fermi=float(line.split()[3])
                Emin=float(line.split()[1])
                Emax=float(line.split()[0])
            if linecounter > 6:
                line=line.split()
                tempEN.append(float(line[0]))
                tempupDOS.append(float(line[1]))
                tempdownDOS.append(float(line[2]))
                tempintupDOS.append(float(line[3]))
                tempintdownDOS.append(float(line[4]))
        fileopen.close()
    
# reset file number and append data
    filecount+=1
    upDOS.append(tempupDOS)
    downDOS.append(tempdownDOS)
    intupDOS.append(tempintupDOS)
    intdownDOS.append(tempintdownDOS)
    energy.append(tempEN)

list=[sDOS,pDOS,dDOS,fDOS]
## PLOT BAND DECOMPOSED DOS
fig= plt.figure()
for i in range(len(list)):
    plt.plot(energy[0],list[i][0],label=labels[i],color=colors[i])
plt.plot([fermi,fermi],[0,120],label=labels[i+1],color=colors[i+1])
# or \mathrm
plt.legend(loc='upper left')
plt.title(plottitle)
plt.ylim(ybounds)
plt.xlim([Emin,Emax+1])
plt.xlabel(r'Energy (eV)',fontsize=14)
plt.ylabel("Number of States/Unit Cell",fontsize=14)
plt.minorticks_on()
plt.show()
fig.savefig(figurename, transparent=True)
    


