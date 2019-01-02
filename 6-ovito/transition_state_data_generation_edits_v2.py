from ovito.data import *

def modify(frame, input, output):
	'''
	# input is the dictionary
	# in_keys gives the keys for the dictionary; ovito calls this attributes
	############ Get the simulation parameters you can modify ####################
	print("The input contains %i particles." % input.number_of_particles)
	in_keys = list(input.keys())		## Get the keys for the dictionary
	print("The input particle keys are: ", in_keys,'\n')
	#%%% How to modify & call ovito data objects so they the modification pipeline and get modifiied
	print("Call the value for the key by input['key']. Like input['Simulation Cell'] gives ",input['Simulation cell'],'\n')
	print("The format is inputName.objectClass['reference name'] and .marray[:] if you want an array")
	#%%% get a list of the class function/array name to call the particle properties
	call_att = input.particle_properties
	print("To access/reference the input particle properties (the data objects type & attributes): ", call_att,'\n')
	'''
	#################### Get Data to migrate an Oxygen atom ####################
	all_pos=input.particle_properties['Position'].marray[:]				# position of all atoms
	##print("The position of all atoms are:", all_pos,'\n') # test if the position array works
	all_ids=output.particle_properties['Particle Identifier'].marray[:] # atom IDS for all particles 
	##print("The IDs for all atoms are:", all_ids,'\n')
	selection_bool = output.particle_properties['Selection'].marray[:]	# atom IDS for manual selection modifier
	##print("The manual selection boolean test array for O atoms is:", selection_bool,'\n')
	selected_ids=sorted([all_ids[i] for i in range(0,len(all_ids)) if selection_bool[i] !=0 ])	# atom IDs for all the selected particles
	print("The ids for the selected Oxygen atoms are:",selected_ids,'\n')
	
	#################### Create dictionary for modification pipeline ####################
	''' LONG ASS WAY
	migration_data={}
	for current_id in selected_ids:
		for match_id in all_ids:
			# get the array which contains the x,y,z position for the maunally selected atoms array
			if current_id == match_id:
				print(all_ids[counter], all_pos[counter])
	print(migration_data, '\n')
	'''
	migration_data={'migration_element'+ str(current_id): {'atomID':current_id,'v_pos':match_pos}
	for current_id in selected_ids 
	for match_id, match_pos in zip(all_ids,all_pos) 
	if current_id == match_id }
	print('The migration data dict is:', migration_data)
	higher_key=list(migration_data.keys())
	print('The first level directory keys are:', higher_key )
	sub_d_key=list((migration_data[higher_key[1]]).keys() )
	print('The section level directory keys are:', sub_d_key,'\n')
		
	#################### Pull and sort from greatest to smallest the Y values for each atom ID ####################
	list_y_values=sorted([ migration_data[i]['v_pos'][1] for i in higher_key])
	##print('The sorted y values are:', list_y_values )
	migration_order=[ higher_key for match_y in list_y_values for higher_key in migration_data if migration_data[higher_key]['v_pos'][1] == match_y]
	##print(migration_order)
	
	