from ovito.data import *

def modify(frame, input, output):
	print("The input contains %i particles." % input.number_of_particles)
	print(input.attributes.keys())
	print(input.particle_properties.keys())
	selected = output.particle_properties['Selection'].marray[:]
	ids = output.particle_properties['Particle Identifier'].marray[:]
	pos = output.particle_properties['Position']
	
	print(selected,ids)
	for i in range(0,len(ids)):
		if selected[i] != 0:
			with open('/home/tboland1/ovito.file.dat','a+') as f:
				f.write('{}\t{}\n'.format(input.particle_properties['Position'].marray[i],ids[i]))
