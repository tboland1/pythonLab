import sys
import os
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import math


## Create all possible combinations of vacancy configurations
vac_comb=[129, 127, 309 ,307 ,628 ,626 ,1040 ,55]
vac_1=[x for x in vac_comb for counter in range(0,5)]
vac_2=[]
for x in range(0,8):
    for counter in range(0,5):
        if counter+x+2 > 7:
            countermod=counter-6
        else :
            countermod=counter+2
        vac_2.append(vac_comb[x+countermod])

## Remove duplications and append to matrix
temp_hold=[]
for vac1,vac2 in zip(vac_1,vac_2):
    temp_hold.append([vac1,vac2])
vac_no_dup=[]
for vac1,vac2 in zip(vac_1,vac_2):
    flag=0
    for i in vac_no_dup:
        print(i,vac1,vac2)
        if [vac1,vac2]==i or [vac2,vac1]==i:
            
            flag=1
    print 'the final flag is set next is append or dont append if flag =1: ',flag
    if flag == 0:
        print 'appending value'
        vac_no_dup.append([vac1,vac2])

## write out the variable
filename='vacancy_include'
fileopen=open(filename,'w')
vac_one=' '.join([str(i[0]) for i in vac_no_dup ])
vac_two=' '.join([str(i[1]) for i in vac_no_dup ])
#print vac_one,'\n',vac_two,'\n'
fileopen.write('variable vac1 '+vac_one+'\n')
fileopen.write('variable vac2 '+vac_two+'\n')
fileopen.close()