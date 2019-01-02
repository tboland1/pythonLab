'''
This script shows you the method by which you can create and access 
keys and values of nested dictionaries for data manipulation
'''
'''
#################  Basic (non-nested) Dictionary Properties & Syntax #################
dd={'migration1':1,'migration2':2,'migration3':3}
# Accessing keys
dd_keys=list(dd.keys())
print 'The un-nested keys are \n', dd_keys
# Accessing VALUES
dd_values=list(dd.values())
print 'The un-nested values are \n', dd_values, '\n'
#####################################################################################


#################  Basic (nested) Dictionary Properties & Syntax ####################
print 'For nested dictionaries'
# Figuring out list comprehension with nested dictionaries
d={'migration1':{'atoms':1},'migration2':{'atoms':2},'migration3':{'atoms':3}}
# Accessing Higher level keys
d_keys=list(d.keys())
print 'The higher level keys are \n',d_keys
# Accessing VALUES
d_values=list(d.values())
print 'The highest level (nested dictionary) values are \n',d_values, '\n'
# Accessing the SUB-KEYS (LONG) 
sub_d_key=[]
for higher_key in d:
    value_d=(d[higher_key]).keys()
    #if value_d[0] not in sub_d_key:
    #    sub_d_key.append(value_d[0])
    if (d[higher_key]).keys()[0] not in sub_d_key:
        sub_d_key.append( (d[higher_key]).keys()[0] )
#sub_d_key=[ for higher_key in d if (d[higher_key]).keys()[0] not in ]
print "The unique sub-dictionary keys are \n", sub_d_key,'\n'
#####################################################################################
###################### WORK IN PROGRESS ABOVE TUTORIAL ##############################


#####################################################################################
# Get the Y values un-sorted
unsort_list_value=[]
for higher_key in d:
    #print higher_key
    value_d=(d[higher_key]).values()[0]                     # the nested value element
    unsort_list_value.append((d[higher_key]).values()[0])
    # if statement to do sub-directory comparison for y values
    #if value_d == 3:
    #    print value_d, higher_key
print "The unsorted list of key values is: ", unsort_list_value,'\n'
#####################################################################################

################### Perform Actual Objective ########################################
# Get the Y values sorted via list comprehension
list_y_values=sorted([  (d[higher_key]).values()[0] for higher_key in d  ])
print 'The list of sorted y values are',list_y_values,'\n'     # test list comprehension

migration_tags=[]
for match_y in list_y_values:
    #print 'match y value is currently:', match_y
    for higher_key in d:
        if  d[higher_key].values()[0] == match_y:
            migration_tags.append(higher_key)
            #print 'match'
print migration_tags
#list_mig_order=[higher_key for higher_key in d if d[higher_key].values()[0] == match_y]
#print(list_mig_order)                                  # check the appension of the migration order
print
#####################################################################################
'''

#####################################################################################
#####################################################################################
migration_data={'migration1':{'atoms':1,'v_pos':[10,11]},'migration2':{'atoms':2,'v_pos':[12,13]},'migration3':{'atoms':3,'v_pos':[14,15]}}
list_y_values=sorted([  (migration_data[higher_key]).values()[0] for higher_key in migration_data  ])
print list_y_values
list_migration=[higher_key for match_y in list_y_values for higher_key in migration_data if migration_data[higher_key].values()[0] == match_y]
print list_migration




#x = [i for i in range(10)]
#print x



'''
################ Attempt More Succinct List Comprehension ###########################
list_y_values=sorted([ (d[higher_key]).values()[0] for higher_key in d])
print( list_y_values )

#test=[ for match_y in list_y_values [higher_key for higher_key in d if d[higher_key].values()[0] == match_y] ]

print
#####################################################################################


################ Attempt Massive List Comprehension #################################
#list_mig_order=next([   (d[higher_key]).values()[0] for higher_key in d if sort_y_values
'''