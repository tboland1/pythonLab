from ovito.data import *
from ovito.io import *


def modify(frame, input, output):
	##############################################################################################################################
	#################################### Get the simulation parameters you can modify ############################################
	##############################################################################################################################
	#%%% print out the system atom count
	print("The input contains %i particles." % input.number_of_particles,'\n')
	in_att = list(input.keys())
	##print("The input particle keys are: ", in_att)
	#%%% these are the data objects data objects enter the modification pipeline and get modifiied
	##print("The format is inputName.objectClass['reference name'] and .marray[:] if you want an array")
	#%%% get a list of the class function/array name to call the particle properties
	call_att = input.particle_properties
	##print("To access/reference the input particle properties (the data objects type & attributes): ", call_att, '\n')
	
	############ Get Data to migrate an Oxygen atom ####################
	all_pos= input.particle_properties['Position'].marray[:] 				# position of all atoms
	##print("The position of all atoms are:", pos_all) # test if the position array works
	selection_bool = output.particle_properties['Selection'].marray[:] 		# ids for the manual selection modifier
	##print("The manual selection boolean test array for O atoms is:", selection_bool)
	all_ids= output.particle_properties['Particle Identifier'].marray[:] 	# id's for all particles 
	##print("The IDs for all atoms are:", ids_all, '\n')
	
	############ get the atom IDs for all the selected particles ############
	selected_ids=[]
	for i in range(0,len(all_ids)):
		if selection_bool[i] != 0:
			selected_ids.append(all_ids[i])
	##print("The ids for the selected O atoms are:",selected_ids,'\n')
	
	#############################################################################################################################
	#################################### Create a dictionary with atomID keys and xyz values ####################################
	#############################################################################################################################
	# atom properties
	migration_data={}
	for current_id in selected_ids:
		for match_id,match_pos in zip(all_ids,all_pos):
			# x,y,z position for the maunally selected atoms array
			if current_id == match_id:
				##print(match_id, match_pos)
				migration_data['migration_element'+ str(current_id)]={'atomID':current_id,'v_pos':match_pos}
	##print('The migration data dict is:', migration_data)
	
	############ get the keys for each hop ############ 
	higher_key=list(migration_data.keys())
	##print('The first level directory keys are:',  higher_key )
	sub_y_key=list((migration_data[higher_key[1]]).keys())
	##print( 'The section level directory keys are:', sub_y_key, '\n')
	
	############ loop to get the y values from the dict to sort them from low to high ############
	list_y_values=[]
	for i in higher_key:
		##print("Migration element:",i,"AtomID:", migration_data[i]['atomID'], "Y-position:", migration_data[i]['v_pos'][1])
		list_y_values.append(migration_data[i]['v_pos'][1])
	list_y_values=sorted(list_y_values)
	##print('The sorted y values are:', list_y_values)
	
	############ get the migration higher key array sorted by y values ############
	migration_order=[]
	for match_y in list_y_values:
		for higher_key in migration_data:
			if migration_data[higher_key]['v_pos'][1] == match_y:
				##print(migration_data[higher_key]['v_pos'][1], higher_key)
				migration_order.append(higher_key)
	migration_order=list(reversed(migration_order))
	##print('The sorted migration higher keys are:',migration_order)
	
	#############################################################################################################################
	####################################    Write the include files for each migration hop   ####################################
	#############################################################################################################################
	migration_hop=0
	mig_len=len(migration_order)-1
	print('The length of the migration order matrix is:', mig_len,'\n')
	print('This is the start of the file writing code \n###########################################')
	for counter in range(0,len(migration_order)-1):
		fileopen_i='/home/tboland1/migration_hop_'+str(migration_hop)+'.dat'
		fileopen_t='/home/tboland1/migration_hop_trans_'+str(migration_hop)+'.dat'
		print('----------------\nMain for loop counter for the migration order matrix:',counter)
		##print('migration hop modulus ',migration_hop%2)
		###############################
		# get the initial state ready
		###############################
		# first odd hop
		if counter == 0:
			mig_key_d	=migration_order[counter]
			mig_key_t	=migration_order[counter+1]
			atom_ID_d	=migration_data[mig_key_d]['atomID']
			atom_ID_t	=migration_data[mig_key_t]['atomID']
			print('The migration key for deleting oxygen from FIRST if statement:', mig_key_d, 'with atom id',atom_ID_d)
			print('The migration key for migrating oxygen from FIRST if statement:', mig_key_t, 'with atom id',atom_ID_t)
			print('Initial migration hop file name is:',migration_hop,'and name is:', fileopen_i,'\n')
		# Create the intital state by moving the atom_prev by the pos_prev the rest of the typical hops
		elif migration_hop > 0:
			mig_key_old	=migration_order[counter]
			mig_key_t	=migration_order[counter+1]
			atom_ID_new	=migration_data[mig_key_t]['atomID']
			atom_ID_old	=migration_data[mig_key_old]['atomID']
			temp		=[]
			for x1,x2 in zip(migration_data[mig_key_old]['v_pos'],migration_data[mig_key_t]['v_pos']):
				##print( (x1-x2)/2 )
				temp.append((x1-x2)/2)
			atom_pos	=(' '.join([str(x) for x in temp]))
			##print(' '.join([str(x) for x in temp]))
			print('Atom disp creating the initial state for the next hop is:',atom_pos_prev,'moving atom',atom_ID_old)
			print('Atom disp creating the transition state for the next hop is:', atom_pos, 'moving atom', atom_ID_new)
			print('Initial migration hop file number:',migration_hop,'and name is:',fileopen_i,'\n')
		###############################
		# create the transition state
		###############################
		if counter == 0:
			temp		=[]
			for x1,x2 in zip(migration_data[mig_key_d]['v_pos'],migration_data[mig_key_t]['v_pos']):
				##print( (x1-x2)/2 )
				temp.append((x1-x2)/2)
			atom_pos	=(' '.join([str(x) for x in temp]))
			##print(' '.join([str(x) for x in temp]))
			print('For the transition state include file')
			print('The atom displacement elemets are:',atom_pos,'for the atom',atom_ID_t)
			print('Transition state file name and number is:',migration_hop, fileopen_t,'\n')
		#elif migration_hop < mig_len and counter != 0:
			#mig_key 	=migration_order[counter]
			#mig_key_p	=migration_order[counter+1]
			#atom_ID		=migration_data[mig_key]['atomID']
			#temp		=[]
			#for x1,x2 in zip(migration_data[mig_key_old]['v_pos'],migration_data[mig_key_t]['v_pos']):
			#	##print( (x1-x2)/2 )
			#	temp.append((x1-x2)/2)
			#atom_pos=(' '.join([str(x) for x in temp]))
			###print(' '.join([str(x) for x in temp]))
			#print('The old migrating atom id is',atom_ID_old,'and the new migrating atom id is',atom_ID_new)
			#print('Atom disp for the new elemets are:',atom_pos)
			#print('Migration hop file number:',migration_hop, fileopen_t,'\n')
		###############################
		#  Write out the include migration hop files 
		###############################
		# odd start for the first initial state
		if counter == 0:
			# writing the initial state 
			with open(fileopen_i,'w+') as f:
				f.write('{}{}\n'.format('group Mobile id ', atom_ID_d))
				f.write('{}\n'.format('delete_atoms group Mobile'))
				f.write('{}\n'.format(' '))
				##f.write('{}{}{}\n'.format('group ce3p id',ce3[0],ce3[1]) )
				##f.write('{}'.format('set group ce3p type 3') )
				##f.write('{}'.format('set type 3 charge 3') )
				f.close()
			# writing the transition state
			with open(fileopen_t,'w+') as f:
				f.write('{}{}\n'.format('group hop id ', atom_ID_t))
				f.write('{}{}{}\n'.format('displace_atoms hop move ', atom_pos,' units box'))
				f.close()
		# writing the typical initial state & trans state include files
		elif migration_hop > 0:
			# writing the initial state 
			with open(fileopen_i,'w+') as f:
				f.write('{}{}\n'.format('group hop id ', atom_ID_old))
				f.write('{}{}{}\n'.format('displace_atoms hop move ', atom_pos_prev,' units box'))
				#f.write('{}{}{}\n'.format('group ce3p id',ce3[0],ce3[1]) )
				##f.write('{}{}{}\n'.format('group ce4p id',ce4[0],ce4[1]) )
				##f.write('{}'.format('set group ce3p type 3') )
				##f.write('{}'.format('set group ce4p type 4') )
				##f.write('{}'.format('set type 3 charge 3') )
				##f.write('{}'.format('set type 4 charge 4') )
				f.close()
			# writing the transition state
			with open(fileopen_t,'w+') as f:
				f.write('{}{}\n'.format('group hop id ', atom_ID_new))
				f.write('{}{}{}\n'.format('displace_atoms hop move ', atom_pos,' units box'))
				f.close()
		atom_pos_prev=atom_pos
		if migration_hop > 0:
			del atom_pos
		migration_hop+=1
		