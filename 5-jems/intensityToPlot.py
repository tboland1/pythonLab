
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py

file="../../4-JEMS/lookuptable/wavefunctionToTiff/results/ce-surface-vac-bulk-Intensity.txt"
fileprefix="../../4-JEMS/lookuptable/wavefunctionToTiff/results/"
linecounter=0
modcounter=0
name=[]
area=[]
mean=[]
min=[]
max=[]

# SURFACE INTENSITY DATA

# LAYER
# site A is monolayer Ce
aSurfint=[]
layera=[]
# site B is the bilayer Ce
bSurfint=[]
layerb=[]

# BULK INTENSITY DATA
bulka=[]
bulkb=[]

# ATOM INTENSITY DATA
atomintensitysurfa=[]
atomintensitysurfb=[]
# ATOM's per column
atom=[]

#background intensity per slice
background=[]
flaga=0
flagb=0

fileopen=open(file)
for line in fileopen:
    #print(line)
    line=line.split()
    
    # REMOVE header lines
    if linecounter < 1:
        linecounter+=1
    # sort data
    else:
        name.append(line[1])        
        area.append(float(line[2]))
        mean.append(float(line[3]))
        min.append(float(line[4]))
        max.append(float(line[5]))

        # SURFACE INTENSITY
        if modcounter%6 == 0 or modcounter%6 == 3:
            # separate a & b
            if modcounter%6 == 0:
                layera.append(int(line[0]))
                aSurfint.append(float(line[2])*float(line[3]))
                atom.append(int(line[6]))
            elif modcounter%6 == 3:
                layerb.append(int(line[0]))
                bSurfint.append(float(line[2])*float(line[3]))
                
        # BACKGROUND INTENSITY 
        elif modcounter%6 == 1 or modcounter%6 == 4:
            BGnorm=float(line[2])*float(line[3])
            background.append(BGnorm)
            
            # NORMALIZE A SURFACE SITE
            if modcounter%6 == 1:
                aSurfint[-1]=aSurfint[-1]/BGnorm
                # set bulk a flag
                flaga = 1
            # NORMALIZE B SURFACE SITE
            elif modcounter%6 == 4:
                bSurfint[-1]=bSurfint[-1]/BGnorm
                # set bulk b flag
                flagb=1
            
        # BULK INTENSITY
        elif modcounter%6 == 2 or modcounter%6 == 5:
            if flagb == 1:
                bulkb.append(float(line[2])*float(line[3])/BGnorm)
                #print('normalizing the bulk b background', BGnorm)
                flagb=0
            elif flaga == 1:
                bulka.append(float(line[2])*float(line[3])/BGnorm)
                #print('normailizing the bulk a background', BGnorm)
                flaga=0

        modcounter+=1
# close the file
fileopen.close()


### PLOTTING PER SLICE ------------------ odd slice number are type A even are type B

# # Ce  Column Intensity per Slice Surface
fig = plt.figure()

plt.plot(layera,aSurfint,'-..',label='A',color='green',mew=3)
plt.plot(layerb,bSurfint,'-..',label='B',color='cyan',mew=3) 

plt.legend(loc='upper right')
plt.title("Surface Ce Column Intensity for Site A & B")
plt.ylabel(r'Intensity (arb. Units)',fontsize=14)
plt.xlabel("Slice Thickness (Number of layers)",fontsize=14)
plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.tight_layout()
plt.minorticks_on()
fig.show()
file=fileprefix+"Surf-Ce-A-B-sites.png"
fig.savefig(file, transparent=True,figsize=(30,30)) 


# # Ce  Column Intensity per Slice Bulk
fig = plt.figure()

plt.plot(layera,bulka,'-..',label='A',color='green',mew=3)
plt.plot(layerb,bulkb,'-..',label='B',color='cyan',mew=3) 

plt.legend(loc='upper right')
plt.title("Bulk Ce Column Intensity for Site A & B")
plt.ylabel(r'Intensity (arb. Units)',fontsize=14)
plt.xlabel("Slice Thickness (Number of layers)",fontsize=14)
plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.tight_layout()
plt.minorticks_on()
fig.show()
file=fileprefix+"Bulk-Ce-column-A-B-sites.png"
fig.savefig(file, transparent=True,figsize=(30,30)) 



### PER ATOM PLOTS ----------------------
# FOR A SITE
fig = plt.figure()

plt.plot(atom,bulka,'-..',color='red',label="Bulk",mew=3)
plt.plot(atom,aSurfint,'-..',color='purple',label="Surface",mew=3)

plt.legend(loc='upper right')
plt.title("Site A: Per Atom Ce Column Intensity")    
plt.ylabel(r'Intensity (arb. Units)',fontsize=14)
plt.xlabel("Intensity Per Atom",fontsize=14)
plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.tight_layout()
fig.show()
file=fileprefix+"A-site-bulk-surf.png"
fig.savefig(file, transparent=True,figsize=(30,30)) 

# FOR B SITE
fig = plt.figure()

plt.plot(atom,bulkb,'-..',color='red',label="Bulk",mew=3)
plt.plot(atom,bSurfint,'-..',color='purple',label="Surface",mew=3)

plt.legend(loc='upper right')
plt.title("Site B: Per Atom Ce Column Intensity")    
plt.ylabel(r'Intensity (arb. Units)',fontsize=14)
plt.xlabel("Intensity Per Atom",fontsize=14)
plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.tight_layout()
fig.show()
file=fileprefix+"B-site-bulk-surf.png"
fig.savefig(file, transparent=True,figsize=(30,30)) 




# # take images to feed to ethan's & barnaby's code
# # give us intensity of all the columns in the exp image