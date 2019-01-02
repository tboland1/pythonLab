'''
Tara Boland
10/21/16
Code to take a file from VASP's output and turn it into an importable for for matlab to make plots out of: strip the letters off, write to a new file with specific output as follows: 2 headlines, which consist of anything needed to describe the values in the file, followed by rows of only numbers because matlab cannot read in characters and numbers in the same line. This is for the OSZICAR FILES. Script contains the lines which had 'DAV:' in front of them.
'''
## put import file and make big import files
import numpy as np
import os.path


## ask for the file name
#fileName = input( "Vasp File Name? ") # file ask choice 1 
stLatCon = 220;
endLatCon = 400;
step = 5;
filelist = [];
missingfile = [];
for i in range( stLatCon, endLatCon + 1, step):
	i = str(i)
	i = i.strip('0')
	i= int(i)
	#print(i)
	file = 'OSZICAR'+ str(i);
	filelist.append(file);

#[1]
#read the file and test to make sure it isnt empty this will run through the list
#print(filelist)
for i in range( 0, len(filelist) ):
	fileName = filelist[i]
	
	
## INITIALIZE EVERYTHING FOR LOOPS	
	theData = []								#initialized the list to fill head line with
	Data = [];									#initialized list to fill with new variables without spaces all over
	header = [ 'N', 'F', 'E0', 'dE', 'E' ];		#create second header for last line
	
	
##  1 READ the file and append to theData 
	#[2]
	#test if path exists to prevent errors
	if os.path.exists(fileName) ==  True:
		print('PATH FOUND TO BE TRUE for ', fileName, ' Proceeding with program.')
		readMe = open( fileName, 'r' )
		for line in readMe:
			theData.append(line.strip())
		readMe.close()
	else:
		print('The file ',fileName, ' does not exist or was not found. Breaking loop for this file.') 
		missingfile.append(fileName)
		continue;
	print( 'MIssing Files are: ', missingfile )
	
##  2 start a loop to read through all the elements in the array theData
	for i in list(range( 0, len(theData) )):
		dat=theData[i].split(' ')				# i-th element of the messy data file, splits up file creating an array of each element of the array (even the spaces)
	#[3]
												# takes theData.split(' ') Removes '' from array & appends letters to new array 
	#[4]
		datI = []; 								#append to intermediate array to make 2D array
		for l in list( range( 0, len(dat) )):
			if len(dat[l]) >= 1:
				p = dat[l]
				datI.append(p) 					#append each element to an array
		Data.append(datI)						#append the 1D array to the 2D array
	# end of the main for loop
	
	
##  3 REMOVE ANY UNEEDED DATA FROM THE MATRIX so matlab can tollerate it
	lenElm = [];								#find and return the length of each array element
	flag = 0;									#set up the flag b/c i am removing to much from arrays
	davRm = [];									#tells array index all the lines which had DAV infront of them aka which lines had it
	for i in range( 0, len(Data) ):
		#print()
		#print('loop itteration i',i)
		for l in range( 0, len(Data[i]) ):
			if flag == -1:
				break;
			# This formats the headline (1st line in the file)
			if len( Data[i] ) == 8 and Data[i][0] == 'N': # mk d eps-> deps avoid editing other array elements
				Data[0][3] = Data[0][3] + Data[0][4]
				del(Data[0][4])
				lenElm.append( len(Data[i]) )   #return the 2nd level len of array after removed vales
				break;							#need to break b/c the len(Data[i]) index is not the same
			# This will format the data pretaining to the OSZICAR file N E dE deps ncg rms rms(c)
			elif Data[i][l] == 'DAV:':			#leave as 0 only that one is ever DAV
				del(Data[i][l])
				davRm.append(i)
				lenElm.append( len(Data[i]) ) 	#return the 2nd level len of array
				#print( lenElm )		
				break;
			# This will format the ground Sate energy it is the format N F E0 dE E
			elif Data[i][l] == 'F=':			#all fomatting work for each array element is contained within each elif statement
				for p in range( 0, len(Data[i])-5 ):
					p += 1;
					if Data[i][p] == 'F=':
						del(Data[i][p])
						#print(Data[i])
					elif Data[i][p] == 'd' :
						del(Data[i][p])
						del(Data[i][3])
						#print(Data[i])
					elif Data[i][p] == 'E0=':
						del(Data[i][p])
						#print(Data[i])
					#[5]
					if p >= 3:
						print('LOOP EDIT SUCCESSFUL."Index out of range error" IMMINENT')
						#print()
						flag = -1;
						lenElm.append( len(Data[i]) )
						Data[len(Data)-1][3] = Data[len(Data)-1][3].strip('=')
						break;
						
	Data.insert(1,header)						# Insert the last line header into Data
	headerlen = len(header);					# Get length of header
	lenElm.insert(1,headerlen)					# Insert len of header into lenElm
	print('Data successfully stripped.')
	print()
	
## 4 Make all the data symmetric so fill blanks with 0's
	long = lenElm[0]; 									#find the value of the longest element in array
	samelen = [];
	#lenElm[0] = 3; #remove later
	a = lenElm[0];								#dont override the actual array element values need dummy indice
	# make sure the long is longest array element
	for i in range( 1, len( lenElm ) ):			#compare with 1st element (should always be the longest)
		if a < lenElm[i]:
			long = lenElm[i]
			a = lenElm[i]
	# add in the amount of 0's missing from each array
	for i in range( 0, len(lenElm) ):
	
		if lenElm[i] < long:
			diff = long - lenElm[i];
			for l in range( 0, diff ):
				myZeros = 0;
				Data[i].append(myZeros)
	
	
##  5  Export the data
	#remove the . out of the filel name
	l = list(fileName);
	#rm = l.index('.')
	#del(l[rm])
	#fileName = ''.join(l)
	fileName = fileName + '.txt'				# make it a text file
	fileopen = open( fileName,'w' )
	for index in range( 0, len(Data) ):
		for element in range( 0, len(Data[index]) ):
			fileopen.write( str(Data[index][element]) )
			fileopen.write(' ')
		fileopen.write('\n')
	fileopen.close()
		
	
	
	
	
	
	
	


'''	
#print('data',Data)

[1] FUTURE WORK
future addition take a list of file, separate them fill and array and use that to open many files at once so i can pass multiple files to the function
[2] FUTURE WORK: try to strip white space between letters here. may be able to do this ````` split and strip in combination with each other. maybe be as simple as moving the loop which strips into the reading of the file.
[3] FUTURE WORK: to get the d eps which is separated by a space use an if & statement to test for d eps and use string.replace(s,old,new[,maxreplace] to fix it.. maybe... 
[4] FUTURE WORK combine this step into the for loop which reads them in. more concise code
[5] take the loop break and put test condition so it will break automatically when the indices dont match instead of having to manually input the number in
[6]  create an if statement at beginning to ask for running a single file which the user can input
[7] make the program ask for the input to run like a program :::::))))))))
'''








