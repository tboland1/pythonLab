# This file was made to read the dump files and get 1NN and 2NN cation
# and anion displacements. It only works for the specified format for the 
# 111 in.vacsurf dump file. It is listed below which order the 
# displacements must come in.

# import needed modules
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import math

## This is the newest most up to date version

## Toss out unneeded values of dump file
def tail(list):
    return list[5:]  # for 1NN & 2NN & Step Edge

## For file format please indicate the format type
format_flag = 1 # :        | 2:          | 3: 

## Dump file Order type 1
    # 0=atom id
    # 1=atom type
    # 2=x
    # 3=y
    # 4=z
    # 5=c_1NN_disp_ce[1]x
    # 6=c_1NN_disp_ce[2]y
    # 7=c_1NN_disp_ce[3]z
    # 8=c_2NN_disp_o[1]x
    # 9=c_2NN_disp_o[2]y
    # 10=c_2NN_disp_o[3]z
## Vacancies on 111: NN order RECENT UPDATED
    # 0=1NN_disp_ce[1](x)
    # 1=1NN_disp_ce[2](y)
    # 2=1NN_disp_ce[3](z)
    # 3=1NN_disp_o[1] (x)
    # 4=1NN_disp_o[2] (y)
    # 5=1NN_disp_o[3] (z)
    # 6=atom id
    # 7=atom type
## Atomic Displacements MD run
    # 0=atomic_disp (x)
    # 1=atomic_disp (y)
    # 2=atomic_disp (z)
    # 3=atom id
    # 4=atom type
    
    
## Dump file list: To be filled into an array with file location attached
# change the labels below

##------------------------------------------------------------------------------
# locations and name of the lammps data file
#prefix="/home/tara/Dropbox/Crozier Group User- Tara Boland/2-lammps/7-step/0-oxidize110/3-final/"
#filecount=['']

#prefix="/home/tara/Dropbox/Crozier Group User- Tara Boland/2-lammps/7-step/1-reduced-line/large/3-final/"
#filecount=['']


##
#prefix='/home/tboland1/Dropbox/Crozier Group User- Tara Boland/2-lammps/7-step/1-reduced-line/large/3-final/'
#filecount=['59']
#filename=['111-minimization-reducedLine-1NN-']

# in tex
#prefix="/home/tboland1/Dropbox/Crozier Group User- Tara Boland/2-lammps/7-step/3-single-vacancy/3-final/"
#filecount=['110']
#filename=['minimize-1-1NN-']

##
#prefix="/home/tara/Dropbox/Crozier Group User- Tara Boland/2-lammps/3-vacancysurf/111/2_vacancyline/1_100percent/3-final/"
#filecount=['57']
#filename=['111-minimization-1NN-']

#prefix="/home/tara/Dropbox/Crozier Group User- Tara Boland/2-lammps/3-vacancysurf/111/2_vacancyline/2_50percent/2-small/3-final/1/"
#filecount=['82']
#filename=['111-minimization-1NN-']

#prefix="/home/tara/Dropbox/Crozier Group User- Tara Boland/2-lammps/3-vacancysurf/111/2_vacancyline/3_25percent/1-large/3-final/"
#filecount=['44']
#filename=["vacancy_surf_111_1NN_"]

#prefix="/home/tara/Dropbox/Crozier Group User- Tara Boland/2-lammps/3-vacancysurf/111/2_vacancyline/4_2vac2/1-large/3-final/2_celist/"
#filecount=['26']
#filename=["vacancy_surf_111_1NN_"]

#error be careful
#prefix="/home/tboland1/Dropbox/Crozier Group User- Tara Boland/2-lammps/3-vacancysurf/111/1_singleVacancy/3-final/1/"
#filecount=['67']
#filename=["111-minimization-1NN-"]

## to get 1NN & 2NN plots (enter 1# for if only one data file is need. data is parsed identically)
#filename=["vacancy_surf_111_1NN_"]
#filename=["111-minimization-1NN-"]
#filename=["111-minimization-disp-"]
#filename=['111-minimization-1NN-']
#filename=['minimize-1-111-reduced-1NN-']

## prefix to save the plot
surfaceID='111 Step Edge'         # what is the surface's name
vacNid='Vacancy '           # how many vacancies are there
ceID='celist1'                 # if there are multiple configuration for a give vacancie identify them
# Name to save the plots as
fileprefix=prefix+"../0-data/"+ceID+"_"+surfaceID+"_"+vacNid

# The plot title's
title1NN="Step Edge Vacancy 1NN Displacement on (111) Terrace Site"
title2NN="Vacancy 2NN Displacement on (111) Terrace Site"
#----------------------------------------------------------------

# Gather the data files
files=[]
for line in range(0,len(filecount)):
    files.append(filename[line]+str(filecount[line]))

# combine file name with file path
filelist=[]
for input in files:
    file=prefix+input
    filelist.append(file)


## Read both files in and plot them.
counterfile=0
for file in filelist:
    fileopen=open(file)
    linecounter=0                            # count the lines for reading dump file
    i=0                                      # index counter for NN data
    NN=[]                                    # array of arrays for each atoms NN data
    # READ the DUMP file 
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
    
    ## Universal group assignment: for loop parsing NN by atom type: ce 3 | ce 4  | o 
    for i in NN:
        atomTypeIndex=len(NN[1])-1
        group=i[atomTypeIndex]         # pick out the atom id from the NN list
        if group == '1':
            groupce4.append(i)
        elif group == '2':
            groupo.append(i)
        elif group == '3':
            groupce3.append(i)
            
    ## find the sqrt(x^2+y^2)
    # THE IN PLANE DISPLACEMENT GROUP
    ce3=[]
    ce4=[]
    o=[]
    # THE TOTAL DISPLACEMENT GROUP
    ce3tot=[]
    ce4tot=[]
    otot=[]
    # IDENTIFY NON UNIQUE ATOM ID'S
    doubleID=[]
    
    # loop for the NN
    for i in groupce3:
        if format_flag == 1:
            planeDisp=math.sqrt(i[0]**2+i[1]**2)
            planeDisptot=math.sqrt(i[0]**2+i[1]**2+i[2]**2)
            ce3.append(planeDisp)
            ce3tot.append(planeDisptot)
        elif format_flag == 2:
            planeDisp=math.sqrt(i[0]**2+i[1]**2)
            planeDisptot=math.sqrt(i[0]**2+i[1]**2+i[2]**2)
            ce3.append(planeDisp)
            ce3tot.append(planeDisptot)
    for i in groupce4:
        if format_flag == 1:
            planeDisp=math.sqrt(i[0]**2+i[1]**2)
            planeDisptot=math.sqrt(i[0]**2+i[1]**2+i[2]**2)
            ce4tot.append(planeDisptot)
            ce4.append(planeDisp)
        elif format_flag == 2:
            planeDisp=math.sqrt(i[0]**2+i[1]**2)
            planeDisptot=math.sqrt(i[0]**2+i[1]**2+i[2]**2)
            ce4tot.append(planeDisptot)
            ce4.append(planeDisp)
    for i in groupo:
        if format_flag == 1:
            # for 1NN where the ce xyz coord comes first
            planeDisp=math.sqrt(i[3]**2+i[4]**2)
            planeDisptot=math.sqrt(i[3]**2+i[4]**2+i[5]**2)
            o.append(planeDisp)
            otot.append(planeDisptot)
        elif format_flag == 2:
            # for Minimization runs of later scripts: see tex notes
            planeDisp=math.sqrt(i[0]**2+i[1]**2)
            planeDisptot=math.sqrt(i[0]**2+i[1]**2+i[2]**2)
            o.append(planeDisp)
            otot.append(planeDisptot)

    
    #------------------------------ File Parse for plots: 1NN from 2NN Data --------------------
    if counterfile == 0:
        # ----------------collect number of each type for graph
        ceMAX=[]
        numce3=len(ce3)
        if len(ce3) > 0:
            maxce3=max(ce3)
            ceMAX.append(maxce3)
            print "MAX for Ce3+ is: " + str(maxce3)
            print "Total Number of Ce3+ is: "+str(len(ce3))
        numce4=len(ce4)
        if len(ce4) > 0:
            maxce4=max(ce4)
            ceMAX.append(maxce4)
            print "MAX for Ce4+ is: "+str(maxce4)
            print "Total Number of Ce4+ is: "+str(len(ce4))
        numo=len(o)
        if len(o) > 0:
            maxo=max(o)        
            print "MAX for O is: " + str(maxo)
            print "Total Number of O is: "+str(len(o))+'\n'
        maxce=max(ceMAX)
        #============================== PLOT HISTOGRAM: 1NN =============================================
        ##============================ BOTH PLOT DATA: 1NN 
        x1=ce3
        x2=ce4
        y1=o
        
        bins=np.linspace(0,maxo, 40)     
        x=[x1,x2,y1]
        labels=[r'Ce$^{\rm 3+}$ ('+str(len(ce3))+')',r'Ce$^{\rm 4+}$ ('+str(len(ce4))+')',r'O$^{\rm 2-}$  ('+str(len(o))  +')']
        colors=['cyan','blue','lightgray']
          
        fig = plt.figure()
        plt.hist(x,bins,label=labels,color=colors,rwidth=0.75,linewidth=1,edgecolor="black",stacked=True)
        plt.legend(loc='upper right')
        plt.minorticks_on()
        plt.title(title1NN)    
        plt.xlabel(r'Total Displacement ($\AA$)',fontsize=14)
        plt.ylabel("Atom Count",fontsize=14)
        plt.rc('xtick',labelsize=12)
        plt.rc('ytick',labelsize=12)
        plt.tight_layout()
        fig.show()
        file=fileprefix+".1NN.png"
        fig.savefig(file, transparent=True,figsize=(30,30)) 
        ##============================ Ce PLOT DATA: 1NN
        #ce3=[[0.3824],[0.64]]*32
        #ce4=[]
        x1=ce3
        x2=ce4
        
        bins=np.linspace(0, 0.6+0.1, 40)   
        x=[x1,x2]
        labels=[r'Ce$^{\rm 3+}$ ('+str(len(ce3))+')',r'Ce$^{\rm 4+}$ ('+str(len(ce4))+')']
        colors=['cyan','blue']     
        
        fig = plt.figure()
        plt.hist(x,bins,label=labels,color=colors,rwidth=0.75,linewidth=1,edgecolor='black',stacked=True)
        plt.legend(loc='upper right')
        plt.minorticks_on()
        #plt.title(title1NN+" for Cations")     # 1NN
        #plt.xlabel(r'Total Displacement ($\AA$)',fontsize=14)
        plt.ylabel("Atom Count",fontsize=14)
        plt.rc('xtick',labelsize=12)
        plt.rc('ytick',labelsize=12)
        plt.tight_layout()
        fig.show()
        file=fileprefix+"_ce.1NN.png"
        fig.savefig(file, transparent=True,figsize=(30,30)) 
        ##============================ OXYGEN PLOT DATA: 1NN
        y1=o
        bins=np.linspace(0,maxo, 40)  
        fig = plt.figure()
        plt.hist(y1,bins,label=r'O$^{\rm 2-}$ ('+str(numo)+')',edgecolor="black",linewidth=0.4,color='lightgray',rwidth=.75)
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
        numce3=len(ce3)
        if len(ce3) > 0:
            maxce3=max(ce3)
            print "MAX for Ce3+ is: " + str(maxce3)
            print "Total Number of Ce3+ is: "+str(len(ce3))
        numce4=len(ce4)
        if len(ce4) > 0:
            maxce4=max(ce4)
            print "MAX for Ce4+ is: "+str(maxce4)
            print "Total Number of Ce4+ is: "+str(len(ce4))
        numo=len(o)
        if len(o) > 0:
            maxo=max(o)        
            print "MAX for O is: " + str(maxo)
            print "Total Number of O is: "+str(len(o))
            
        #============================== PLOT HISTOGRAM: 2NN =============================================
        ##============================ BOTH PLOT DATA: 2NN 
        x2=ce4
        y1=o
        
        x=[x1,y1]
        labels=[r'Ce$^{\rm 4+}$ ('+str(len(ce4))+')',r'O$^{\rm 2-}$  ('+str(len(o))  +')']
        colors=['blue','lightgray']
        bins=np.linspace(0,maxo, 40)       
        
        fig = plt.figure()
        plt.hist(x,bins,label=labels,color=colors,rwidth=0.75,linewidth=1,edgecolor='black',stacked=True)
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
        ##============================ Ce PLOT DATA: 2NN 
        x2=ce4
        
        bins=np.linspace(0, maxce4+0.1, 40)        
        
        fig = plt.figure()
        plt.hist(x2,bins,label=r'Ce$^{\rm 4+}$ ('+str(numce4)+')',edgecolor="black",linewidth=0.4,color='blue',rwidth=.75)
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
        ##============================ OXYGEN PLOT DATA: 2NN
        y1=o
        
        bins=np.linspace(0,maxo, 40)  
        
        fig = plt.figure()
        plt.hist(y1,bins,label=r'O$^{\rm 2-}$ ('+str(numo)+')',edgecolor="black",linewidth=0.4,color='lightgray',rwidth=.75)
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















