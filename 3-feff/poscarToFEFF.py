# This file will read any POSCAR / CONTCAR formatted file and create an
# atoms.inp file (atom location pre-FEFF file) which can be turned into a feff.inp input file using the 
# gfortran compiled file atoms246.f 
# You must have the atoms element tag line in the POSCAR/CONTCAR in order
# to tag the atoms properly.
# FORMAT of POSCAR: Needs to have atom type lines to parse data corrects!! 
    # AtomTypeTag X Y Z AtomTag+AtomNum
## Import libraries
import os

## Enter the location of the POSCAR/CONTCAR 
# POSCAR1unit'
filename = input("What is the full path of the POSCAR/CONTAR? (try both w & w/o ' ') ")
# title
title=[]
eleTag=[]
# number of each element in the poscar
eleCount=[]
# get all the coordinates unparsed by type
coordTot=[]
# add the line counter
linecounter=0

## Enter the target atom
target=str(input("What is the Target atom? (add in the element type) "))        # get the target

# open the file & get system info: # of atoms, type of atoms, lattice params, pull atom coords into coordTot
fileopen=open(filename)
for line in fileopen:
    linecounter+=1
    line=line.strip()
    
    # get the system tag name
    if linecounter == 1:
        line=line.replace(" ","")
        title.append(line.strip())
    # get the a,b,c lattice vectors has to be cubic
    elif linecounter > 2 and linecounter < 6:
        if linecounter == 3:
            varA=line.split()
            a=float(varA[0])
        elif linecounter == 4:
            varB=line.split()
            b=float(varB[1])
            #print(b)
        elif linecounter == 5:
            varC=line.split()
            c=float(varC[2])
    # get the elements tags
    elif linecounter == 6:
        eleTag=line.split()    
    elif linecounter == 7:
        eleCount=[int(x) for x in line.split()]
        #print(eleCount)
    elif linecounter >= 9:
        coordTot.append(line)
        #print(coordTot)
fileopen.close()

## Now construct the extra data types
# count the number of atom types
countType=len(eleCount)
# element type tag 
eleType=[]
# number of each type of element + tag
eleNum=[]
# count total number of atoms
countAtoms=0 #sum(eleCount)-1
loopNum=0

# read the data and fill in the atoms246.f required tags
for element in eleCount:
    for i in range(1,element+1):
        # add in the data needed for atoms246.f file
        eleType.append(eleTag[loopNum])
        eleNum.append(str(eleTag[loopNum]+str(i)))
    # sum up all the atoms currently counted
    countAtoms+=element
    # find array position to pick atoms from arrays
    loopNum+=1


##! Uncomment for cart coords
# linecounter=0
# fileopen=open(file)
# for line in fileopen:
#     linecounter+=1
#     if linecounter < 9:
#         cat=1
#     elif linecounter >= 9 and linecounter <=  numO[0]+numCe[0]+9:
#         # normalize the coordinates
#         if linecounter >=9 and linecounter <= 9+numO[0]-1:
#             coord=line.split()
#             x1=float(coord[0])/a
#             x2=float(coord[1])/b
#             x3=float(coord[2])/c
#             #disp goes here
#             ocoord.append([x1,x2,x3])
#         elif linecounter > 9+numO[0]-1 and linecounter <= numO[0]+numCe[0]+9-1:
#             coord=line.split()
#             x1=float(coord[0])/a
#             x2=float(coord[1])/b
#             x3=float(coord[2])/c
#             #total= ((x1-xtar[0])**2+(x2-xtar[1])**2+(x3-xtar[2])**2)**(1/2.0) #disp goes here
#             cecoord.append([x1,x2,x3])
# fileopen.close()

##! Uncomment for fractional coords
# linecounter=0
# fileopen=open(file)
# for line in fileopen:
#     linecounter+=1
#     if linecounter < 9:
#         cat=1
#     elif linecounter >= 9 and linecounter <=  numO[0]+numCe[0]+9:
#         # normalize the coordinates
#         if linecounter >=9 and linecounter <= 9+numO[0]-1:
#             coord=line.split()
#             x1=float(coord[0])
#             x2=float(coord[1])
#             x3=float(coord[2])
#             ocoord.append([x1,x2,x3])
#         elif linecounter > 9+numO[0]-1 and linecounter <= numO[0]+numCe[0]+9-1:
#             coord=line.split()
#             x1=float(coord[0])
#             x2=float(coord[1])
#             x3=float(coord[2])
#             cecoord.append([x1,x2,x3])
# fileopen.close()
# # # # # 
## write the atoms.inp file
linecounter=0
# open the file to write
filenew=open('atoms.inp','w')
# add in the details for atoms246.f to write the data
filenew.write('title'+' '+title[0]+'\n')
# just remove the symmetry of the cluster
filenew.write('space P 1 \n')
filenew.write('a='+str(a)+' '+'b='+str(b)+' '+'c='+str(c)+'\n')
# write out a big cluster so you can delete the far atoms from the cluster
filenew.write('rmax=13'+' '+'core='+target+'\n')
filenew.write('index=t\n')
filenew.write('atom\n')
# write out the atom positions
for line in coordTot:
    filenew.write(eleType[linecounter]+'  '+coordTot[linecounter]+' '+ eleNum[linecounter]+'\n')
    linecounter+=1
filenew.write('--------------------------------------')
filenew.close()


## use atomsToFeff on the file generated here then copy and paste this
# into the top of the feff.inp file

# CONTROL   1   1   1     1     1
# PRINT     0   0   0     0     0
#   
# COREHOLE RPA
# SCF 7.0 0 30 0.2 1

# COREECTIONS 0 0.03
# EDGE K
# S02 0.0
# 
# ELNES 4 0.02 0
# 300 1 0 1
# 2.4 0 
# 5 3
# 0 0
