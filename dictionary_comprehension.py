'''
This script shows you the different ways to create a dictionary from
the very succinct method through comprehension to the overly 
verbose for loops and explicit initialization and filling

ALL ARE EQUIVALENT
'''
## MOST SUCCINCT way of making a dictionary
a={  i: chr(65+i) for i in range(4) }
#dictionary_name={   key,value "for loop list comprehension or itterable you want to populate the dict with"  }

## MORE FORMAL way of creating a dictionary: sudo list comprehnsion
a1=dict([  (i, chr(65+i)) for i in range(4)  ])
# dictionary_name=dict_def([   (key,value) "for loop list comprehension"  ])

## LONGEST6 form: no list comprehension
print 'loop key: value displaying below:'
a2={}
for i in range(4):
    print i, chr(65+i)
    a2[i]=chr(65+1)

print "\n As you can see both method 1, 2 and 3 result in the same dictionary: \n",a,'\n',a1,'\n',a2
