## Crystal data obtainer.
# This file will read the POSCAR and CONTCAR. It can detect
# whether or not you have a tag line.
# It exports lattice, basis, system tag, atom tags for each 
# atom type and the number of atoms of each type. 

# import needed libraries
import numpy as np

##! TEMP readfile name
filename='POSCAR'

# intialize the data set array's
basis=[]    # get the basis
scaling=[]  # get the universal scaling constant
lattice=[]  # get the lattice
systag=[]   # pull the first line
atominfo=[] # put together atoms type and atom number

## OPEN file, Obtain data

counter=0;
# get coordinate system and determine atom tag is present or not
fileopen=open(filename)

for line in fileopen:
    counter+=1
    line=line.strip()
    n=list(line)
    if n[0] == 'd' or line[0] == 'D':
        headerlines=counter-1

fileopen.close()

# sort all the data into the respective arrays
counter=0
fileopen=open(filename)

if headerlines == 6:
    for line in fileopen:
        if counter == 0:
            line=line.strip()
            systag.append(line)
        elif counter == 1:
            line=line.strip()
            scaling.append(line)
        elif counter >=2 and counter >= 4:
            line=line.strip()
            lattice.append(line)
        elif counter == 5:
            line=line.strip()
            line=line.split()
            atominfo.append(line)
        elif counter >= 7:
            line=line.strip()
            line=line.split()
            basis.append(line)
        counter+=0

elif headerlines == 7:
    for line in fileopen:
        if counter == 0:
            line=line.strip()
            systag.append(line)
        elif counter == 1:
            line=line.strip()
            scaling.append(line)
        elif counter >=2 and counter <= 4:
            line=line.strip()
            lattice.append(line)
        elif counter >= 5 and counter <=6:
            line=line.strip()
            line=line.split()
            atominfo.append(line)
        elif counter >= 8:
            line=line.strip()
            line=line.split()
            basis.append(line)
        counter+=1

fileopen.close()

a1b=[i[0] for i in basis]
a2b=[i[1] for i in basis]
a3b=[i[2] for i in basis]







































