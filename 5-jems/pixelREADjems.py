import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import math



filelist=["../../JEMS/test.txt"]
lines=[[0]*128]*128  # intensity, x,y given by index Intensity in 2d array
pixelx=range(0,128)
for file in filelist:
    fileopen=open(file)
    linecounter=0                            # count the lines for reading dump file
    countery=0
    # READ the DUMP file 
    for line in fileopen:
        # if to: remove the header lines from dump file
        if linecounter < 5 :
            linecounter+=1
        else:
            line=line.rstrip()
            line=line.lstrip()
            line=line.strip('')
            line=line.split(',')
            for i in range(len(line)-1):             # run over NNint and turn into a number
                lines[countery][i]=float(line[i+1])
            countery+=1
            # Separate out the list of displaced atoms from atoms not in the displaced atoms group by removing all 0 filled numbers
            # close the file
    fileopen.close()


H=lines

fig = plt.figure()

ax = fig.add_subplot(111)
ax.set_title('colorMap')
plt.imshow(H)
ax.set_aspect('equal')

#cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
#cax.get_xaxis().set_visible(False)
#cax.get_yaxis().set_visible(False)
#cax.patch.set_alpha(0)
#cax.set_frame_on(False)
plt.colorbar(orientation='vertical')
plt.show()