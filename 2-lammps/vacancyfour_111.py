# This file was made to read the dump files and get 1NN and 2NN cation
# and anion displacements. It only works for the specified format for the 
# 111 in.vacsurf dump file. It is listed below which order the 
# displacements must come in.

# import needed modules
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py

## Enter the location of the dump file which you want to import 


## Toss out unneeded values of dump file: Uncomment for 1 vac or 2 vac
def tail(list):
    return list[7:]  # for 111 surface list 1NN 2NN 1 vacancy

##! Enter file location: 1 vacancy on 111: 14 indicies
# single vacancy on 111 surface 

#fileopen=open(filelist[0])


##! 2 vacancy on 111: 13 indicies  
# two vacancies 1NN-vacancy on 111 @ asu computer
#filelist=['/home/tboland1/Dropbox/"Crozier Group User- Tara Boland"/2-lammps/7-step/1-reduced-line/large/']
#fileopen=open(filelist[1])
    # 0=1NN_disp_ce
    # 1=1NN_disp_o
    # 2=1NN2_disp_ce 
    # 3=1NN2_disp_o
    # 4=1NN_disp_ce
    # 5=1NN_disp_o
    # 6=1NN_disp_ce
    # 7=1NN_disp_o
    # 8=atom id
    # 9=atom type


## read the dump file and put relavant data into NN list
file='/home/tboland1/Dropbox/Crozier Group User- Tara Boland/2-lammps/7-step/1-reduced-line/large/3-final/111-minimization-reducedLine-1NN-59'

#file='vacancy_surf_111_1NN_43'
fileopen=open(file)
#fileopen=open(filelist[0])
# initialize variables
linecounter=0                            # count the lines
i=0                                      # index counter for NN data
NN=[]                                    # array of arrays for each atoms NN data
# read the file line by line using a for loop
for line in fileopen:
    # remove the header lines
    if linecounter < 9:
        linecounter+=1
    else:
        # Get the 1NN and 2NN data from the read data into an array
        NNint=tail(line.split())
        # turn NN into an array of numbers
        i=list(range(0,len(NNint)))
        counter=0
        for i in NNint:
            NNint[counter]=float(NNint[counter])
            counter+=1
        # remove all 0 filled numbers
        j=[0,0,0,0,0,0,0,0]
        if j != NNint: 
            NNint.append(line.split()[0])           # add atom id into the array
            NNint.append(line.split()[1])           # add the atom type into array
            NN.append(NNint)                        # append NNint to NN array
# close the file
fileopen.close()


## Parse Data into group to make !!!!!! Histogram the data!!!!
# CAUTION this code is for Ce 4+ = type 1 and Ce 3+ = type3 and O = type 2
atomnum=len(NN)                             # number of atoms
i=list(range(0,atomnum))                          # range of NN array
groupce4=[]                                  # Ce4+
groupce3=[]                                 #  3+ 
groupo=[]                                   # O group

## Universal group assignment: for loop parsing NN by atom type: ce 3 and 4 group 1 | o group 2
for i in NN:
     group=i[9]
     if group == '1':
        groupce4.append(i)
     elif group == '2':
        groupo.append(i)
     elif group == '3':
        groupce3.append(i)
    # 0=1NN_disp_ce
    # 1=1NN_disp_o
    # 2=1NN2_disp_ce 
    # 3=1NN2_disp_o
    # 4=1NN_disp_ce
    # 5=1NN_disp_o
    # 6=1NN_disp_ce
    # 7=1NN_disp_o
    # 8=atom id
    # 9=atom type

##! loops to parse 1NN ce from o for 111 with 2 vacancies
ce3=[]
ce4=[]
o=[]

# loop for the 1NN with 2 vacancies
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

##! Plot Histogram 111 2 VACANCIES: 2NN and 1NN

# define data for 2 Vacancies 1NN's
x1=ce3
x2=ce4
y1=o
bins=np.linspace(0, 2,100)
#define the figure with name
fig = plt.figure()
# plot/label the data
plt.hist(x1,bins,alpha=0.5,label=r'Ce$^{3+}$',edgecolor="c",linewidth=0.15,color='cyan')
plt.hist(x2,bins,alpha=0.5,label=r'Ce$^{4+}$',edgecolor="c",linewidth=0.15,color='green')
plt.hist(y1,bins,alpha=0.5,label='O',edgecolor="b",linewidth=0.15,color='red')
plt.legend(loc='upper right')
plt.minorticks_on()
plt.title("1NN Displacement on (101) Surface: 4 Vacancies")
plt.xlabel(r'Total Displacement ($\AA$)',fontsize=14)
plt.ylabel("Atom Count",fontsize=14)
# display and save data/fig
fig.show()
fig.savefig('101_ce3_ce4_4vac.1NN.png', transparent=True)
 
# # Plot for 2NN
# 
# # define data
# x2=twoNNce
# y2=twoNNo
# bins=np.linspace(0, .5,100)
# # define the figure with name
# fig = plt.figure()
# # plot/label the data
# plt.hist(x2,bins,label=r'Ce$^{4+}$',edgecolor="k",linewidth=0.2,color='green')
# plt.hist(y2,bins,label='O',edgecolor="b",linewidth=0.2,color='red')
# plt.legend(loc='upper right')
# plt.minorticks_on()
# plt.title("2NN Displacement on (111) Surface: 1 Vacancy")
# plt.xlabel(r'Total Displacement ($\AA$)',fontsize=14)
# plt.ylabel("Atom Count",fontsize=14)
# #plt.grid(True)
# # display and save data/fig
# fig.show()
# fig.savefig('2NN_111_1vac_1group.png', transparent=True)

















