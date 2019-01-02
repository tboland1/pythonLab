from ovito.data import *

def modify(frame, input, output):
	############ Get the simulation parameters you can modify ####################
	#%%% print out the system atom count
	##print("The input contains %i particles." % input.number_of_particles)
	#%%% get a list /print out all the attributes for the input data
	#%%% these are the objects that constitute the modification pipeline
	in_att = list(input.keys())
	##print("The input particle keys are: ", in_att)
	#%%% these are the data objects data objects enter the modification pipeline and get modifiied
	##print("The format is inputName.objectClass['reference name'] and .marray[:] if you want an array")
	#%%% get a list of the class function/array name to call the particle properties
	call_att = input.particle_properties
	##print("To access/reference the input particle properties (the data objects type & attributes): ", call_att, '\n')
	
	############ Get Data to migrate an Oxygen atom ####################
	#%%% the position of all atoms
	pos_all = input.particle_properties['Position'].marray[:]
	##print("The position of all atoms are:", pos_all) # test if the position array works
	#%%% get the array which contains the ids for the manual selection modifier
	selection_bool = output.particle_properties['Selection'].marray[:]
	##selectedarray = output.particle_properties['Selection'] # may not be useful
	##print("The selection array is:", selectedarray)
	##print("The manual selection boolean test array for O atoms is:", selection_bool)
	#%%% get the id's for all particles to check against the selection array
	ids_all = output.particle_properties['Particle Identifier'].marray[:]
	##print("The IDs for all atoms are:", ids_all, '\n')
	
	#%%% get the atom IDs for all the selected particles
	selected_ids=[]
	for i in range(0,len(ids_all)):
		if selection_bool[i] != 0:
			selected_ids.append(ids_all[i])
	##print("The ids for the selected O atoms are:",selected_ids)
	
	## Create a dictionary with atomID keys and xyz values
	#%%% atom properties
	migration_data={}
	for i in selected_ids:
		#%%% get the array which contains the x,y,z position for the maunally selected atoms array
		##print(o_hop_counter,ids_all[i-1], pos_all[i-1])
		migration_data['migration_element'+ str(i)]={'atomID':ids_all[i-1],'v_pos':pos_all[i-1]}
	print(migration_data, '\n')
		
	###### get the keys for each hop
	higher_key=list(migration_data.keys())
	print( higher_key )
	sub_y_key=list((migration_data[higher_key[1]]).keys())
	print( sub_y_key, '\n')
	
	##### loop to get the y values from the dict to sort them from low to high
	list_y_values=[]
	for i in higher_key:
		##print("Migration element:",i,"AtomID:", migration_data[i]['atomID'], "Y-position:", migration_data[i]['v_pos'][1])
		list_y_values.append(migration_data[i]['v_pos'][1])
	list_y_values=sorted(list_y_values)
	print(list_y_values,'\n')
	
	##### get the migration higher key array sorted by y values ######
	list_migration=[]
	for i in higher_key:
		#print(i)
		list_migration.append(i)
	print(list_migration)
	
	'''
	for i in migration_data.keys():
		print(i)
		data_keys=migration_data[i].items()
		list_migration.append(i)
	print(list_migration)
	## doesnt work
	#key = next(key for key, value in migration_data[i].items() if value == y_sort[0])
	#print(key)
	'''
	