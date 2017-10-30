# This file was made to read the dump files and get 1NN and 2NN cation
# and anion displacements. It only works for the specified format for the 
# 111 in.vacsurf dump file. It is listed below which order the 
# displacements must come in.

# import needed modules
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py

## Toss out unneeded values of dump file
def tail(list):
    return list[5:]  # for 111 surface list 1NN & 2NN 1 vacancy

## Dump file Order
    # 0=atom id
    # 1=atom type
    # 2=x
    # 3=y
    # 4=z
    # 5=q
    # 6=c_PE
    # 7=c_1NN_disp_ce[4]
    # 8=c_1NN_disp_o[4]
## Vacancies on 111: NN order
    # 0=1NN_disp_ce
    # 1=1NN_disp_o
    # 2=atom id
    # 3=atom type
    
    
## Make the dump file list array with file location attached
## change these three things
prefix="../../lammps/3_vacancysurf/111/1_singleVacancy/2_dump/1_celist/"
files=["vacancy_surf_111_1NN_27","vacancy_surf_111_2NN_27"]
ceID='celist1'

filelist=[]
for input in files:
    file=prefix+input
    filelist.append(file)

## prefix to save the data: the celist number, directory from prefix, file name
surfaceID='111'
vacNid='1vac'
fileprefix=prefix+"../../1_data/"+ceID+"_"+surfaceID+"_"+vacNid
##
title1NN="List 1: 1 Vacancy 1NN Displacement on (111) Surface"
title2NN="List 1: 1 Vacancy 2NN Displacement on (111) Surface"


## Read both files in and plot them.
counterfile=0
for file in filelist:
    fileopen=open(file)
    # initialize variables
    linecounter=0                            # count the lines for reading dump file
    i=0                                      # index counter for NN data
    NN=[]                                    # array of arrays for each atoms NN data
    ## READ the DUMP file 
    for line in fileopen:
        # if to: remove the header lines from dump file
        if linecounter < 9:
            linecounter+=1
        else:
            # Get the 1NN and 2NN data from file & turn into number
            NNint=tail(line.split())    # remove unneeded information from each line and append to NNint
            # start the loop over NNint's individual elements to turn into a number
            i=range(0,len(NNint))       # get the index for the NNint array length
            counter=0                   # initialize counter for the index of NNint
            for i in NNint:             # run over NNint and turn into a number
                NNint[counter]=float(NNint[counter])
                counter+=1
            # Separate out the list of displaced atoms from atoms not in the displaced atoms group by removing all 0 filled numbers
            j=[0,0]                                     # there are 2 displace/atoms to track: o and ce
            if j != NNint:                              # if criteria is met append it to NN and append atom id and type
                NNint.append(line.split()[0])           # add atom id into the array
                NNint.append(line.split()[1])           # add the atom type into array
                NN.append(NNint)                        # append NNint to NN array
    # close the file
    fileopen.close()
    ## Parse Data into groups to make Histogram
    # CAUTION this code is for Ce 4+ = type 1 and Ce 3+ = type3 and O = type 2
    atomnum=len(NN)                             # number of atoms to keep track of in NN
    groupce4=[]                                 # Ce4+
    groupce3=[]                                 # Ce3+ 
    groupo=[]                                   # O group
    ## Universal group assignment: for loop parsing NN by atom type: ce 3 and 4 group 1 | o group 2
    for i in NN:
        # assign each element of NN to the variable i
        group=i[3]         # pick out the atom id from the NN list
        if group == '1':
            groupce4.append(i)
        elif group == '2':
            groupo.append(i)
        elif group == '3':
            groupce3.append(i)
    ## loops to parse 1NN ce from o for 111: up to 4 vacancies vacancies
    ce3=[]
    ce4=[]
    o=[]
    doubleID=[]
    # loop for the NN
    for i in groupce3:
        # if for groupce3
        if i[0] != 0:
            ce3.append(i[0])
        elif i[2] != 0:
            ce3.append(i[2])
        elif i[4] != 0:
            ce3.append(i[4])
        elif i[6] != 0:
            ce3.append(i[6])
    for i in groupce4:
        # if for groupce4
        if i[0] != 0:
            ce4.append(i[0])
        elif i[2] != 0:
            ce4.append(i[2])
        elif i[4] != 0:
            ce4.append(i[4])
        elif i[6] != 0:
            ce4.append(i[6])
    for i in groupo:
        if i[1] != 0:
            o.append(i[1])
        elif i[3] !=0:
            o.append(i[3])
        elif i[5] != 0:
            o.append(i[5])
        elif i[7] !=0:
            o.append(i[7])
    
    ################### ------------------------ File Parse: 1NN from 2NN Data --------------------
    if counterfile == 0:
        # ----------------collect number of each type for graph
        numce3=len(ce3)
        maxce3=max(ce3)
        print "MAX for Ce3+ is: " + str(maxce3)
        print "Total Number of Ce3+ is: "+str(numce3)
        numce4=len(ce4)
        maxce4=max(ce4)
        numo=len(o)
        maxo=max(o)
        print "MAX for Ce4+ is: "+str(maxce4)
        print "Total Number of Ce4+ is: "+str(numce4)
        print "MAX for O is: " + str(maxo)
        print "Total Number of O is: "+str(numo)
        #####!!!!!!!!!!!!! Plot Histogram 111 VACANCIES: 1NN
        # Both
        x1=ce3
        x2=ce4
        y1=o
        bins=np.linspace(0,maxo, 40)       
        fig = plt.figure()
        plt.hist(x1,bins,alpha=0.5,label=r'Ce$^{\rm 3+}$ ('+str(numce3)+')',edgecolor="black",linewidth=0.4,color='cyan') # 1NN
        plt.hist(x2,bins,alpha=0.5,label=r'Ce$^{\rm 4+}$ ('+str(numce4)+')',edgecolor="black",linewidth=0.4,color='darkgreen')
        plt.hist(y1,bins,alpha=0.5,label=r'O$^{\rm 2-}$ ('+str(numo)+')',edgecolor="black",linewidth=0.4,color='red')
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
        fig = plt.figure()
        plt.hist(x1,bins,alpha=0.5,label=r'Ce$^{\rm 3+}$ ('+str(numce3)+')',edgecolor="black",linewidth=0.4,color='cyan') # 1NN
        plt.hist(x2,bins,alpha=0.5,label=r'Ce$^{\rm 4+}$ ('+str(numce4)+')',edgecolor="black",linewidth=0.4,color='darkgreen')
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
        plt.hist(y1,bins,alpha=0.5,label=r'O$^{\rm 2-}$ ('+str(numo)+')',edgecolor="black",linewidth=0.4,color='red')
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
        
    elif counterfile == 1:
        # ----------------collect number of each type for graph
        numce4=len(ce4)
        maxce4=max(ce4)
        numo=len(o)
        maxo=max(o)
        print "MAX for Ce4+ is: "+str(maxce4)
        print "Total Number of Ce4+ is: "+str(numce4)
        print "MAX for O is: " + str(maxo)
        print "Total Number of O is: "+str(numo)
        #####!!!!!!!!!!!!! Plot Histogram 111 VACANCIES: 2NN
        #########  BOTH 
        x2=ce4
        y1=o
        bins=np.linspace(0,maxo, 40)       
        fig = plt.figure()
        plt.hist(x2,bins,alpha=0.5,label=r'Ce$^{\rm 4+}$ ('+str(numce4)+')',edgecolor="black",linewidth=0.4,color='darkgreen')
        plt.hist(y1,bins,alpha=0.5,label=r'O$^{\rm 2-}$ ('+str(numo)+')',edgecolor="black",linewidth=0.4,color='red')
        plt.legend(loc='upper right')
        plt.minorticks_on()
        plt.title(title2NN)     
        plt.xlabel(r'Total Displacement ($\AA$)',fontsize=14)
        plt.ylabel("Atom Count",fontsize=14)
        plt.rc('xtick',labelsize=12)
        plt.rc('ytick',labelsize=12)
        plt.tight_layout()
        fig.show()
        file=fileprefix+".2NN.png"
        fig.savefig(file, transparent=True,figsize=(30,30))  
        ## Ce
        x2=ce4
        bins=np.linspace(0, maxce4+0.1, 40)        
        fig = plt.figure()
        plt.hist(x2,bins,alpha=0.5,label=r'Ce$^{\rm 4+}$ ('+str(numce4)+')',edgecolor="black",linewidth=0.4,color='darkgreen')
        plt.legend(loc='upper right')
        plt.minorticks_on()
        plt.title(title2NN+" for Cations")    # 2NN
        plt.xlabel(r'Total Displacement ($\AA$)',fontsize=14)
        plt.ylabel("Atom Count",fontsize=14)
        plt.rc('xtick',labelsize=12)
        plt.rc('ytick',labelsize=12)
        plt.tight_layout()
        fig.show()
        file=fileprefix+"_ce.2NN.png"
        fig.savefig(file, transparent=True,figsize=(30,30)) 
        ######### Automated with max O: No Ce
        y1=o
        bins=np.linspace(0,maxo, 40)  
        fig = plt.figure()
        plt.hist(y1,bins,alpha=0.5,label=r'O$^{\rm 2-}$ ('+str(numo)+')',edgecolor="black",linewidth=0.4,color='red')
        plt.legend(loc='upper right')
        plt.minorticks_on()
        plt.title(title2NN+" for Anions")    # 2NN
        plt.xlabel(r'Total Displacement ($\AA$)',fontsize=14)
        plt.ylabel("Atom Count",fontsize=14)
        plt.rc('xtick',labelsize=12)
        plt.rc('ytick',labelsize=12)
        plt.tight_layout()
        fig.show()
        file=fileprefix+"_o.2NN.png"
        fig.savefig(file, transparent=True,figsize=(30,30))  
    counterfile+=1
        
        
    
    
    
    
    
    
    
    
    
    
    
    












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















