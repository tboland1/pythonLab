## LAMMPS Dump: python 2 script
# This script was created to read a lammps dump file and return values to a 
# lammps run as an include in a lammps input script. 
# the script reads the dump file produced by lammps using a run 0 command
# then reads all the lines after the atoms id, line number 9. it then creates an 
# include file called celist which makes the list of atoms to be turned into ce3+

# find the dump files   
names=["ceids1","vacids"]
#names=["ceids1","ceids2","vacids"]
#names=["ceids1","ceids2","ceids3","vacids"]
#names=["ceids1","ceids2","ceids3","ceids4","vacids"]
counts=[]
export=[]

# read the files into export
for name in names:
    fpath=name
    counter=0
    fileopen=open(fpath)
    for line in fileopen:
        if counter >= 9:
            line=line.strip()
            line=int(line)
            export.append(line)
        counter+=1
    fileopen.close()
    counts.append(counter-9)

# parse out export into ceidslist ( all the cerium ids )
idlength=3*(len(names)-1)
cesum=0
for i in range( len(names)-1 ):
    ce=counts[i]
    cesum+=ce
# find the number of unique id's
uniqueID=0
sortedID=sorted(export)
for line in range(len(sortedID)-1):
    if sortedID[line] == sortedID[line+1]:
        uniqueID+=1

## if statement for the 101 surface 
if counts[0] == 11:
    array=[[]]*counts[1]
    counter=0
    for i in range(counts[1]-1):
        temp=[[]]*3
        for x in range(3):
            num=int(export[counter])
            temp[x]=num
            counter+=1
            array[i]=sorted(temp)
    temp=[[]]*3
    for x in range(2):
        num=int(export[counter])
        temp[x]=num
        counter+=1
    temp=sorted(temp)
    temp[2]=0
    array[3]=temp
    fill=[[]]*counts[1]
    for i in range(counts[1]):
        array[i].remove(array[i][2])
        temp=array[i]
        # make into a string to add to new file
        fill[i]=' '.join([str(x) for x in temp]) # string together each element of temp and place into array
    # create the new file
    filenew='celist'
    listce=' '.join([str(x) for x in fill])
    fileopen=open(filenew,'w')
    fileopen.write('group ce3 id ' + listce + ' \n')
    fileopen.write('set group ce3 type 3 \n')
    fileopen.write('set type 3 charge 3 \n')
    fileopen.close()
# if there is no overlap between ce 1NN lists
elif counts[-1] == (cesum-uniqueID)/float(3):
    counterq=0
    for q in range(1,4):                        # make 3 celist files to pick from
        array=[[]]*(cesum/3)
        counter=0
        for i in range(cesum/3):                # loop over the total number of vacancy groups
            temp=[[]]*3                         # parse the data into appropriate dimensions
            for x in range(3):                  # make each group x number of ce atoms long
                temp[x]=export[counter]         # place components of export into ce temp-array
                counter+=1
                temp=sorted(temp)               # sort the list
            ## remove the atom symmetrically from each place in temp
            temp.remove(temp[q-1])
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
# hard coded: delete ce3+ from list
elif (cesum-uniqueID)%3 != 0:
    temp=[[]]*cesum
    for i in range(cesum):                  # pull out the ce ids from export
        temp[i]=export[i]                   # put number into temp
    temp=sorted(temp)                       # sort the array
    listce=' '.join([str(x) for x in temp]) # string together each element of temp and place into array
    
    # create the new file
    filenew='celist'
    fileopen=open(filenew,'w')
    fileopen.write('group ce3 id ' + listce + ' \n')
    fileopen.write('set group ce3 type 3 \n')
    fileopen.write('set type 3 charge 3 \n')
    fileopen.close()
  









## elif statement Future work
# counts[0]%5 == 0:
#     # 101 
#     span=counts[0]/5
#     sortarray=[[]]*counts[0]
#     array=[[]]*span
#     counter=0
#     # sort the list of ce values from highest to lowest and get all id's into sortarray
#     for i in range(counts[0]):      # break sortarray into x groups of 5
#         num=int(export[counter])    # make each element of export a number
#         sortarray[i]=num            # put number into sortarray
#         counter+=1                  # increment the index to append sortarray
#     sortarray=sorted(sortarray)     # sort the array
#     counter=0                       # re-initialize counter
#     # split up sortarray and append to array
#     for i in range(span):
#         temp=[[]]*5                 # initialize the temporary array to append each segment into array
#         for x in range(5):          # loop over 5 values
#             temp[x]=sortarray[counter]  # append 5 values from sortarray into temp
#             counter+=1              # increment counter
#         ## remove the atom symmetrically from each place in temp
#         temp.remove(temp[3])
#         # make into a string to add to new file
#         array[i]=' '.join([str(x) for x in temp]) # string together each element of temp and place into array
#     
#     # create the new file
#     filenew='celist'
#     listce=' '.join([str(x) for x in array])
#     fileopen=open(filenew,'w')
#     fileopen.write('group ce3 id ' + listce + ' \n')
#     fileopen.write('set group ce3 type 3 \n')
#     fileopen.write('set type 3 charge 3 \n')
#     fileopen.close()























