# This file was made to read the dump files and get 1NN and 2NN cation
# and anion displacements. It only works for the specified format for the 
# 111 in.vacsurf dump file. It is listed below which order the 
# displacements must come in.

# import needed modules
import sys
import os
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import math

## Toss out unneeded values of dump file
def tail(list):
    return list[5:]  # for 1NN & 2NN & Step Edge

## Atom computed properties
# MSD for each atom per file        MSDo
# MSD for each atom per file        MSDce3
# MSD for each atom per file        MSDce4
# RMSD for each atom per file       RMSDo
# RMSD for each atom per file       RMSDce3
# RMSD for each atom per file       RMSDce4


## Dump file Order
    # 0=atom id
    # 1=atom type
    # 2=x
    # 3=y
    # 4=z
    # 5=c_1NN_disp_ce[1]x
    # 6=c_1NN_disp_ce[2]y
    # 7=c_1NN_disp_ce[3]z

## Atomic Displacements MD run
    # 0=thermal_disp (x)
    # 1=thermal_disp (y)
    # 2=thermal_disp (z)
    # 3=atom id
    # 4=atom type
    

## Dump file list: To be filled into an array with file location attached
#============================================================================================

# things to change are listed below
#'Dropbox/Crozier Group User- Tara Boland'
prefix='../../lammps/3_vacancysurf/111/2_vacancyline/1_100percent/2_dump/1_celist1/'
#'../../lammps/3_vacancysurf/111/2_vacancyline/1_100percent/2_dump/1_celist1/'
filename="111-md-thermal-disp-"
filecount=range(0,510,50)

# prefix to save the data: the directory from prefix, surface defined, file name
surfaceID='111'         # what is the surface's name
fileprefix=prefix+"../../1_data/"+surfaceID

# The plot title's
title1NN="Thermal Displacement: (111) Surface"

#====================== Set up file matrix =======================================================

# Get the file name for the MD runs 
files=[]
for line in range(0,len(filecount)):
    files.append(filename+str(filecount[line]))

# combine file name with file path
filelist=[]
for input in files:
    file=prefix+input
    filelist.append(file)
    
filelen=len(filelist)

# MSD for each timestep
MSDo=[0]*filelen                                   ## DEFINE MSD MATRIX
MSDce3=[0]*filelen                                       
MSDce4=[0]*filelen                            
#squared displacement x,y
ce3disp2=[]
ce4disp2=[]
odisp2=[]           
# the x,y,z,atom id displacement values for each timestep
ce3xyz=[]
ce4xyz=[]
oxyz=[]

# MSD = <(x-x_0)^2> = 1/N SUM[ {x_n(t)-x_n(0)}^2  ] (from n=1 to N)
# from MD runs I have {x_n(t)-x_n(0)} (displace/atom exports this)
# I append {x_n(t)-x_n(0)}^2 to MSD matrix

## Read Files APPEND DATA to ARRAY
counterfile=0
for file in filelist:
    fileopen=open(file)                      # open file
    linecounter=0                            # count the lines for reading dump file
    NN=[]                                    # array of arrays for each atoms NN data
    ## READ the DUMP file 
    for line in fileopen:
        # remove the header lines from dump file
        if linecounter < 9:
            linecounter+=1
        else:
            # Get data from file 
            NNint=tail(line.split())    # remove unneeded information & append to NNint
            # turn NNint's elements into a number
            i=range(0,len(NNint))       # get index range for NNint array
            counter=0                   # initialize counter index of NNint
            for i in NNint:
                NNint[counter]=float(NNint[counter])
                counter+=1
            ## i think this is decreptid 
            # Separate out displaced atoms from atoms not in the displaced atoms group using 0 filled numbers
            j=[0,0]                                     # there are 2 displace/atoms to track: o and ce
            if j != NNint:                              # if criteria is met append it to NN and append atom id and type
                NNint.append(line.split()[0])           # add atom id into the array
                NNint.append(line.split()[1])           # add the atom type into array
                NN.append(NNint)                        # append NNint to NN array
    # close the file
    fileopen.close()
    
    #================================ Parse Data into groups to make Histogram
    # CAUTION this code is for Ce 4+ = type 1 and Ce 3+ = type3 and O = type 2
    atomnum=len(NN)                             # number of atoms to keep track of in NN
    groupce4=[]                                 # Ce4+
    groupce3=[]                                 # Ce3+ 
    groupo=[]                                   # O group
    
    #===================== Universal group assignment: parsing NN array by atom type ================
    for i in NN:
        # assign each element of NN to the variable i
        atomTypeIndex=len(NN[1])-1
        group=i[atomTypeIndex]         # pick out the atom id from the NN list
        if group == '1':
            groupce4.append(i)
        elif group == '2':
            groupo.append(i)
        elif group == '3':
            groupce3.append(i)
    
    ##=============================== find the x^2+y^2 sqrt ========================
    # EACH ATOMS in plane displacement squared array (same structure as NN)
    ce3=[]
    ce4=[]
    o=[]
    # EACH ATOMS total displacement squared array
    ce3tot=[]
    ce4tot=[]
    otot=[]
    # EACH ATOMS temp xyz variable array
    ce3xyzt=[]
    ce4xyzt=[]
    oxyzt=[]
    # track if ID's are non-unique (overlapping groups in the MD simulation)
    doubleID=[]
    
    # calculate atomic displacement values for each atom group
    for i in groupce3:
        planeDisp=i[0]**2+i[1]**2
        disptot=i[0]**2+i[1]**2+i[2]**2
        coord=[i[0],i[1],i[2],i[3]]
        ce3xyzt.append(coord)
        ce3.append(planeDisp)
        ce3tot.append(disptot)
    for i in groupce4:
        planeDisp=i[0]**2+i[1]**2
        disptot=i[0]**2+i[1]**2+i[2]**2
        coord=[i[0],i[1],i[2],i[3]]
        ce4xyzt.append(coord)
        ce4tot.append(disptot)
        ce4.append(planeDisp)
    for i in groupo:
        planeDisp=i[0]**2+i[1]**2
        disptot=i[0]**2+i[1]**2+i[2]**2
        coord=[i[0],i[1],i[2],i[3]]
        oxyzt.append(coord)
        o.append(planeDisp)
        otot.append(disptot)
    
    #============================================ SORT DATA OUT OF THE FOR LOOP
    # append out the 2D squared displacement
    ce3disp2.append(ce3)
    ce4disp2.append(ce4)
    odisp2.append(o)
    # append out the 3D displacements 
    oxyz.append(oxyzt)
    ce4xyz.append(ce4xyzt)
    ce3xyz.append(ce3xyzt)
    
    #========================================= MSD of Each Timestep track stability =================
    # Get the number of particles summed over
    Nce3=len(ce3)
    Nce4=len(ce4)
    No=len(o)
    # NOW MAKE THEM THE MSD plane array
    for i in range(0,No):
        MSDo[counterfile]=np.sum(o)/No
    for i in range(0,Nce3):
        MSDce3[counterfile]=np.sum(ce3)/Nce3
    for i in range(0,Nce4):
        MSDce4[counterfile]=np.sum(ce4)/Nce4
    counterfile+=1


##============================ GET RMSD values per Atom ===================================
ce3count=len(ce3disp2[1])
ce4count=len(ce4disp2[1])
ocount=len(odisp2[1])

RMSDo=[0]*ocount     #counterfile
RMSDce3=[0]*ce3count # counterfile
RMSDce4=[0]*ce4count #counterfile

MSDmatrix=[ce3disp2,ce4disp2,odisp2]
filecount=0

# for disp2 in MSDmatrix:
#     elementcount=0
#     for timenum in disp2:
#         if filecount == 0:
#             RMSDce3.append(timenum)
#         elif filecount == 1:
#             RMSDce4.append(timenum)
#         elif filecount == 2:
#             RMSDo.append(timenum)
#         elementcount+=1
#     filecount+=1

#for i in range(0,len(ce3disp2[0])):
timestepindex=0
for timestep in ce3disp2:
    index=0
    for atominfo in timestep:
        if timestepindex == 0:
            RMSDce3[index]=atominfo
        else :
            atomsum=RMSDce3[index]+atominfo
            RMSDce3[index]=atomsum
        index+=1
    timestepindex+=1
print(RMSDce3)
    # if filecount == 0:
    #     RMSDce3[index]=atominfo
    # elif filecount == 1:
    #     RMSDce4[index]=atominfo
    # elif filecount == 2:
    #     RMSDo[index]=atominfo
    # index+=1

##------------------------- Collect Max disp for each species --------------------

# ----------------collect number of each type for graph
if len(ce3) > 0:
    maxce3=max(ce3)
    print ("MAX for Ce3+ is: " + str(maxce3))
    print ("Total Number of Ce3+ is: "+str(len(ce3)))

if len(ce4) > 0:
    maxce4=max(ce4)
    print ("MAX for Ce4+ is: "+str(maxce4))
    print ("Total Number of Ce4+ is: "+str(len(ce4)))

if len(o) > 0:
    maxo=max(o)        
    print ("MAX for O is: " + str(maxo))
    print ("Total Number of O is: "+str(len(o)))

##========================= Plot Histogram of RMSD for each ATOM over the period of the simulation ===========================================
# Both
x1=ce3
x2=ce4
y1=o

bins=np.linspace(0,maxo, 40)       
x=[x1,x2,y1]
labels=[r'Ce$^{\rm 3+}$ ('+str(len(ce3))+')',r'Ce$^{\rm 4+}$ ('+str(len(ce4))+')',r'O$^{\rm 2-}$  ('+str(len(o))  +')']
colors=['blue','cyan','lightgray']

fig = plt.figure()
plt.hist(x,bins,label=labels,color=colors,rwidth=0.75,linewidth=1,edgecolor="black",stacked=True)

plt.legend(loc='upper right')
plt.minorticks_on()
plt.title(title1NN)     # 1NN
plt.xlabel(r'Total Displacement ($\AA$)',fontsize=14)
plt.ylabel("Atom Count",fontsize=14)
plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.tight_layout()
fig.show()
file=fileprefix+".1NN.png"
fig.savefig(file, transparent=True,figsize=(30,30))

#########  Ce
x1=ce3
x2=ce4
bins=np.linspace(0, maxce4+0.1, 40)        
x=[x1,x2]
labels=[r'Ce$^{\rm 3+}$ ('+str(len(ce3))+')',r'Ce$^{\rm 4+}$ ('+str(len(ce4))+')']
colors=['blue','cyan']

fig = plt.figure()
plt.hist(x,bins,label=labels,color=colors,rwidth=0.75,linewidth=1,edgecolor='black',stacked=True)
plt.legend(loc='upper right')
plt.minorticks_on()
plt.title(title1NN+" for Cations")     # 1NN
plt.xlabel(r'Total Displacement ($\AA$)',fontsize=14)
plt.ylabel("Atom Count",fontsize=14)
plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.tight_layout()
fig.show()
file=fileprefix+"_ce.1NN.png"
fig.savefig(file, transparent=True,figsize=(30,30)) 

######### O
y1=o
bins=np.linspace(0,maxo, 40)  

fig = plt.figure()
plt.hist(y1,bins,label=r'O$^{\rm 2-}$ ('+str(len(o))+')',edgecolor="black",linewidth=1,color='lightgray',rwidth=.75)
plt.legend(loc='upper right')
plt.minorticks_on()
plt.title(title1NN+" for Anions")     # 1NN
plt.xlabel(r'Total Displacement ($\AA$)',fontsize=14)
plt.ylabel("Atom Count",fontsize=14)
plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.tight_layout()
fig.show()
file=fileprefix+"_o.1NN.png"
fig.savefig(file, transparent=True,figsize=(30,30)) 





# SMALL_SIZE = 8
# MEDIUM_SIZE = 10
# BIGGER_SIZE = 12
# 
# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
# plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
# plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
# plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
# plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
# plt.rc('font', size=SMALL_SIZE)
# pltt.rc('axes', titlesize=SMALL_SIZE)















