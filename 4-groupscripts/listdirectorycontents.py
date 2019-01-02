import os

dirlist=os.listdir("/home/tboland1/temp")
filedata=[]
dateAndTime=[]

for element in dirlist:
    element=element.strip(' \t\n\r')
    filedata.append(element)
    temp=element.split('2017 ')
    temp=temp[1].split(' - pellet')
    dateAndTime.append(temp[0])

