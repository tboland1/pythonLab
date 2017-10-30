## LAMMPS Dump: python 2 script
# This script was created to read a lammps dump file and return values to a 
# lammps run as an include in a lammps input script. 
# the script reads the dump file produced by lammps using a run 0 command
# then reads all the lines after the atoms id, line number 9. it then creates an 
# include file called celist which makes the list of atoms to be turned into ce3+
import os.path

## Define functions for use
# returns a list of elements from an array that are unique --> removes duplicates
def remove_duplicates(list):
    uniqueElements=list(set(list))
    return uniqueElements
    

## Number of Vacancies: uncomment to find dump files
# fix this with try and catch & when caught read the vacids length & return the length of the id's as the number of ceids in an array of arrays
names=["ceids1","ceids2","ceids3","ceids4","ceids5","ceids6","ceids7","ceids8","ceids9","ceids10"]
counts=[]       # count the number of Ce and O atoms
ceID=[]       # the ce ids
vacID=[]        # the vac ids

## Test for the number of ce id files
filecounter=0
for name in names:
    test=os.path.isfile(name)
    if test == True:
        filecounter+=1
names=[]
for i in range(filecounter):
    name="ceids"+str(i+1)
    names.append(name)

## read the Ce files into ceID, Count total Ce id's append to count, read vacid &  append
countsTemp=[]
for name in names:
    fpath=name
    #initialize data & matrices
    counter=0
    fileopen=open(fpath)
    for line in fileopen:
        if counter >= 9:
            line=line.strip()
            line=int(line)
            ceID.append(line)
        counter+=1
    fileopen.close()
    countsTemp.append(counter-9)
# sum up all the total number of ce id's (if multiple ceid files this is needed)
cesum=0
for number in countsTemp:
    cesum+=number
counts.append(cesum)

# fill in the Vac ids
fpath="vacids"
counter=0
fileopen=open(fpath)
for line in fileopen:
    if counter >= 9:
        line=line.strip()
        line=int(line)
        vacID.append(line)
    counter+=1
fileopen.close()
counts.append(counter-9)

## find the number of unique id's, remove non-unique ids, update counts
# initialize variables
uniqueID=0
sortedID=sorted(ceID)
# count the number of non-unique id's
for line in range(len(sortedID)-1):
    if sortedID[line] == sortedID[line+1]:
        uniqueID+=1
# if the unique id is not equal to 0 remove them
if uniqueID != 0:
    sortedID=remove_duplicates(sortedID)
    counts[0]=len(sortedID)
    
## Sort & Write data to a file called celist*: 111 surface


# This is for the (111) surface with no overlapping Ce for each vacancy group
if counts[-1] == (counts[0]-uniqueID)/float(3):
    for q in range(1,4):                        # make 3 celist files to pick from
        array=[[]]*(counts[0]/3)
        counter=0
        for i in range(counts[0]/3):                # loop over the total number of vacancy groups
            temp=[[]]*3                         # parse the data into appropriate dimensions
            for x in range(3):
                temp[x]=ceID[counter]         # place components of ceID into ce temp-array
                temp=sorted(temp)               # sort the list
                counter+=1
            ## remove the atom symmetrically from each place in temp
            temp.remove( temp[q-1] )
            array[i]=' '.join([str(x) for x in temp]) # string together each element of temp and place into array
        
        # create the new file
        fileID=str(q)                           # get the celist id number 
        includefile='celist'                    # base name for the include file
        filenew=includefile+fileID              # concatonate the file base name with file id
        listce=' '.join([str(x) for x in array]) # string together the array numbers
        fileopen=open(filenew,'w')
        fileopen.write('group ce3 id ' + listce + ' \n')
        fileopen.write('set group ce3 type 3 \n')
        fileopen.write('set type 3 charge 3 \n')
        fileopen.close()

# If there ARE overlapping ID numbers: uniqueID removes non-unique ID from Ce list & returns celist1 
elif uniqueID != 0:
    temp=[[]]*counts[0]
    for i in range(counts[0]):                  # pull out the ce ids from ceID
        temp[i]=sortedID[i]                   # put number into temp
    temp=sorted(temp)                       # sort the array
    listce=' '.join([str(x) for x in temp]) # string together each element of temp and place into array
    print("Unique ID", uniqueID)
    # create the new file
    filenew='celist'
    fileopen=open(filenew,'w')
    fileopen.write('group ce3 id ' + listce + ' \n')
    fileopen.write('set group ce3 type 3 \n')
    fileopen.write('set type 3 charge 3 \n')
    fileopen.close()

# This is for bulk vacancies
elif counts[-1] == counts[0]/float(4):
    counter=0
    cearray=[[]]*counts[0]                     # parse the data into appropriate dimensions
    for x in range(counts[0]):
        cearray[x]=ceID[counter]         # place components of ceID into cearray
        temp=sorted(cearray)               # sort the list
        counter+=1
    groups=counts[0]/4
    array=[[]]*groups                                           #for mulitple bulk vacancy groups ignore ATM
    counterfile=0                                               # counter for the number of celists ceIDed
    for q in range(3):                                          # make 6 celist files to pick from
        for x in range(q+1,4):
            temp=[[]]*2
            temp[0]=cearray[q]
            temp[1]=cearray[x]            
            counterfile+=1
            listce=' '.join([str(p) for p in temp])             # string together each element of temp and place into array
            # create the new file & construct file name
            fileID=str(counterfile)                             # get the celist id number 
            includefile='celist'                                # base name for the include file
            filenew=includefile+fileID                          # concatonate the file base name with file id
            fileopen=open(filenew,'w')
            fileopen.write('group ce3 id ' + listce + ' \n')
            fileopen.write('set group ce3 type 3 \n')
            fileopen.write('set type 3 charge 3 \n')
            fileopen.close()    

# If the previous statements are invalid then this returns a list of Ce atoms 
else :
    counter=0
    temp=[[]]*counts[0]                         # parse the data into appropriate dimensions
    for i in range(counts[0]):                  # pull out the ce ids from ceID
        temp[i]=sortedID[i]                   # put number into temp
    listce=' '.join([str(x) for x in temp]) # string together each element of temp and place into array
    # create the new file
    filenew='celist1'
    fileopen=open(filenew,'w')
    fileopen.write('group ce3 id ' + listce + ' \n')
    fileopen.write('set group ce3 type 3 \n')
    fileopen.write('set type 3 charge 3 \n')
    fileopen.write('# written in else statement \n')
    fileopen.close()





















## Future work: Find the configurations which are unique and energetically favorable
    #   span=counts[0]/5
    # sortarray=[[]]*counts[0]
    # array=[[]]*span
    # counter=0
    # # sort the list of ce values from highest to lowest and get all id's into sortarray
    # for i in range(counts[0]):      # break sortarray into x groups of 5
    #     num=int(ceID[counter])    # make each element of ceID a number
    #     sortarray[i]=num            # put number into sortarray
    #     counter+=1                  # increment the index to append sortarray
    # sortarray=sorted(sortarray)     # sort the array
    # counter=0                       # re-initialize counter
    # # split up sortarray and append to array
    # for i in range(span):
    #     temp=[[]]*5                 # initialize the temporary array to append each segment into array
    #     for x in range(5):          # loop over 5 values
    #         temp[x]=sortarray[counter]  # append 5 values from sortarray into temp
    #         counter+=1              # increment counter
    #     ## remove the atom symmetrically from each place in temp
    #     temp.remove(temp[3])
    #     # make into a string to add to new file
    #     array[i]=' '.join([str(x) for x in temp]) # string together each element of temp and place into array















