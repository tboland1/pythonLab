# This file will read any feff.inp formatted file and create another list of feff.inp
# atom coordinates which is charge neutral to run the feff.inp with a charge neutral 
# cluster. 
# The fifth element is the element of interest. Its format is 
    # AtomType_NumberOfEleInThisCoorShell_
## Variables
# filename -- the name of the file you are going to open, has the feff.inp atom data
# eleTag -- array containing each element's label. each element corresponds to the same distance in shellRad
# shellRad -- array containing the distance each atom is from the target feff atom
# shellcounter -- used to count how many shell's exists in the feff cluster, shells are defined by a change in the radii distance from the previous radii logged in the shellRad
# linecounter -- counts the lines when reading the file
# radSwitch -- array containing the index where the shell transitions to another number
# lineEle -- temp array used to parse like target atoms displacements together
# shells -- holds an array parsing the shells by target atoms distance
# eleTagParse -- corresponding array of element tags for shells


## Import libraries
import os

## Enter the location of the POSCAR/CONTCAR 
filename = '/home/tara/Dropbox/Crozier Group User- Tara Boland/scripts/PythonScripts/feff/atomscount.txt' #input("What is the full path of the feff.inp file? (try both w & w/o ' ') ")
eleTag=[]                       # what type of atoms are in the poscar
shellRad=[]                     # element shell radius (line[5])
radSwitch=[]                    # the last index of the element with the same radius       
shellcounter=0
linecounter=0                   # add the line counter

## open the file & get system info: looking for fifth line atomsTag+atomNum/shell
fileopen=open(filename)
for line in fileopen:
    linecounter+=1
    line=line.strip()
    line=line.split()
    lineEle=list(line[4])       # parameters for parsing atom type
    flag=0
    # append the atom type to the eleTag for each line in the file
    for element in range(0,len(lineEle)):
        if lineEle[element].isdigit() == True and flag==0:
            eleTag.append("".join(lineEle[0:element]))
            flag=1
    # Identify Number of Shells: append the shell radius to the array
    shellRad.append(float(line[5]))
    if float(line[5]) != shellRad[linecounter-2] and linecounter != 1:
        radSwitch.append(linecounter-1)
        shellcounter+=1
fileopen.close()

## Parse the data via Shell radii!!
shells=[[]]*(shellcounter+1)
eleTagParse=[[]]*(shellcounter+1)
for shell in range(0,shellcounter+1):
    if shell == 0:
        eleTagParse[shell]=eleTag[0:radSwitch[shell]]
        shells[shell]=shellRad[0:radSwitch[shell]]
    elif shell >= 1 and shell < shellcounter:
        eleTagParse[shell]=eleTag[radSwitch[shell-1]:radSwitch[shell]]
        shells[shell]=shellRad[radSwitch[shell-1]:radSwitch[shell]]
    elif shell == 32:
        eleTagParse[shell]=eleTag[radSwitch[shell-1]:len(shellRad)]
        shells[shell]=shellRad[radSwitch[shell-1]:len(shellRad)]
    
## Ask for Charges & Number of species; Sum up the charges
##### change back
count=2 #input('How many element types are in the file? (must be an integer) ')
atomcount=[[]]*count
# ask the user for the information
###### change back
EleChr='Ce,4;O,-2' #input("Please list all elements one by one in the following way: 'Element,Charge;Element,Charge' ")
atomscount=EleChr.split(';')                    # split the atom infor into an array
eleNum=len(atomscount)                          # number of atoms in the file
# split the info up
for element in range(0,eleNum):
    atomscount[element]=atomscount[element].split(',')
    atomscount[element][1]=int(atomscount[element][1])
# sum the charges with the user defined shell radii
### change back
radilimit=6.5 #input('What is the SCF or the maxium shell radii? ')
flag=0
indexstop=0
for i in range(0,len(shellRad)):
    if radilimit <= shellRad[i] and flag == 0:
        indexstop=i
        flag=1
# now count the number of of elements and sum the charges up to the encompassing radii
totChar=0
for index in range(0,eleNum):
    types=atomscount[index][0]
    charges=atomscount[index][1]
    for i in range(0,indexstop):
        if eleTag[i] == types:
            totChar+=charges
print(totChar)




## write the atoms.inp file
# # linecounter=0
# # # open the file to write
# # filenew=open('atoms.inp','w')
# # # add in the details for atoms246.f to write the data
# # filenew.write('title'+' '+title[0]+'\n')
# # # just remove the symmetry of the cluster
# # filenew.write('space P 1 \n')
# # filenew.write('a='+str(a)+' '+'b='+str(b)+' '+'c='+str(c)+'\n')
# # # write out a big cluster so you can delete the far atoms from the cluster
# # filenew.write('rmax=16'+' '+'core='+target+'\n')
# # filenew.write('index=t\n')
# # filenew.write('atom\n')
# # # write out the atom positions
# # for line in coordTot:
# #     filenew.write(eleType[linecounter]+'  '+coordTot[linecounter]+' '+ eleNum[linecounter]+'\n')
# #     linecounter+=1
# # filenew.write('--------------------------------------')
# # filenew.close()


## use atomsToFeff on the file generated here then copy and paste this
# into the top of the feff.inp file

# CONTROL   1   1   1     1     1
# PRINT     0   0   0     0     0
#   
# COREHOLE RPA
# SCF 7.0 0 30 0.2 1
# EXCHANGE 0 1.97 0 0
# COREECTIONS 0 0.03
# EDGE K
# S02 0.0
# 
# ELNES 4 0.02 0
# 300 1 0 1
# 2.4 0 
# 5 3
# 0 0
