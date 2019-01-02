# Ethan's program Look Up table export file reader & plot generator


import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
from mpl_toolkits.basemap import Basemap
#import pybinding as pb
import networkx as nx

## Data File Structure
# 0 = filename with atomic layer popupimage.#atomiclayers_Ce
# 1 = feature number
# 2 = Mean Area (pixel^2)
# 3 = x coord
# 4 = y coord
# 5 = Mean pixel intensity
# 6 = trash
# 7 = integrated intensity (sanity check)

fileprefix="../../../4-JEMS/lookuptable/EthansFolder/"
# CHANGE FOR EVEN AND ODD SLICES 
filelist=['CeO2-lookup-table-even.txt','CeO2-lookup-table-odd-ED.txt']
slicelist=[12,11]           # even is site b  #slices=12 | # odd is site a  #slices=11

for counts in range(len(filelist)):
    linecounter=0
    featurecounter=0
    featurecount=51
    arraydim=0
    filecount=12
    
    name=   [[i for i in range(featurecount)] for j in range(filecount)]
    feature=[[i for i in range(featurecount)] for j in range(filecount)]
    area=   [[i for i in range(featurecount)] for j in range(filecount)]
    locx=   [[i for i in range(featurecount)] for j in range(filecount)]
    locy=   [[i for i in range(featurecount)] for j in range(filecount)]
    mean=   [[i for i in range(featurecount)] for j in range(filecount)]
    sanity= [[i for i in range(featurecount)] for j in range(filecount)]
    
    test=   [[i for i in range(featurecount)] for j in range(filecount)]
    meanint=[[i for i in range(featurecount)] for j in range(filecount)]
    normalizedint=[[]]*filecount
    vacuumint=[]
    layer=[]
    
    file = "../../../4-JEMS/lookuptable/EthansFolder/" +filelist[counts]
    slices=slicelist[counts]
    
    
    ## Read File & Append Data
    fileopen=open(file)
    for line in fileopen:
        #print(line)
        line=line.split()
        
        # REMOVE header lines
        if linecounter < 1:
            linecounter+=1
        # sort data
        else:
            if featurecounter < 51:
                name[arraydim][featurecounter]=line[0]       
                feature[arraydim][featurecounter]=int(line[1])
                area[arraydim][featurecounter]=(float(line[2]))
                locx[arraydim][featurecounter]=(float(line[3]))
                locy[arraydim][featurecounter]=(float(line[4]))
                mean[arraydim][featurecounter]=(float(line[5]))
                sanity[arraydim][featurecounter]=(float(line[7]))
                featurecounter+=1
            elif featurecounter == 51:
                layer.append(int((line[0].split('image.'))[1].split('atomiclayer')[0]))
                vacuumint.append(float(line[5]))
                featurecounter=0
                arraydim+=1
    # close the file
    fileopen.close()
    
    ## Normalize Data
    for index in range(0,slices):
        vacint=np.multiply(area[index],vacuumint[index])
        meanint[index]=np.multiply(area[index],mean[index])
        normalizedint[index]=np.divide(meanint[index],vacint)
    
    
    # #FEATURE MAP
    # for i in range(slices):
    #     fig = plt.figure()
    #     
    #     x1=locx[i]
    #     y1=locy[i]
    #     
    #     labels=[str(p) for p in feature[i]]
    #     
    #     plt.scatter(x1, y1, marker='.', )
    #     for label, x, y in zip(labels, x1, y1):
    #         plt.annotate(label, xy=(x, y), xytext=(-5, 5), textcoords='offset points', ha='right', va='bottom')
    #     
    #     plt.title("Atomic Ce Columns Per Feature")
    #     plt.ylabel(r'y (pixels)',fontsize=14)
    #     plt.xlabel("x (pixels)",fontsize=14)
    #     plt.rc('xtick',labelsize=12)
    #     plt.rc('ytick',labelsize=12)
    #     plt.tight_layout()
    #     plt.minorticks_on()
    #     fig.show()
    
    
    if slices == 12:
        # EVEN INDEX'S
        bulkindexa1=[24,26,26,25,25,22,24,24,21,23,23,22]           # 4 atomic layers x,y
        bulkindexa2=[22,21,21,24,20,23,26,22,23,24,24,23]           # 4 atomic layers x, 5 atomic layers y
        surfindexa1=[48,50,51,47,47,50,46,48,46,51,47,47]           # 3 y
        surfindexa2=[51,47,50,49,48,51,47,49,49,47,50,51]           # 4 y
        layera=layer
        
        # PLOT
        bulkinta1=[]
        for i,atomiclayer in zip(bulkindexa1,range(slices)):
            bulkinta1.append(normalizedint[atomiclayer][i-1])
            
        bulkinta2=[]
        for i,atomiclayer in zip(bulkindexa2,range(slices)):
            bulkinta2.append(normalizedint[atomiclayer][i-1])
            
        surfinta1=[]
        for i,atomiclayer in zip(surfindexa1,range(slices)):
            surfinta1.append(normalizedint[atomiclayer][i-1])
        
        surfinta2=[]
        for i,atomiclayer in zip(surfindexa2,range(slices)):
            surfinta2.append(normalizedint[atomiclayer][i-1])
    
        ## PLOTTING PER SLICE ------------------ even slice number are type A even are type B
        
        # # Ce  Column Intensity per Slice Surface
        fig = plt.figure()
        
        plt.plot(layera,surfinta1,'-..',label='A1',color='green',mew=3)
        plt.plot(layera,surfinta2,'-..',label='A2',color='green',mew=3)
        
        plt.legend(loc='upper right')
        plt.title("Surface Ce Column Intensity for Site A")
        plt.ylabel(r'Intensity (arb. Units)',fontsize=14)
        plt.xlabel("Slice Layer Thickness (Number of layers)",fontsize=14)
        plt.rc('xtick',labelsize=12)
        plt.rc('ytick',labelsize=12)
        plt.tight_layout()
        plt.minorticks_on()
        fig.show()
        filesave=fileprefix+"Surf-Ce-A-site.png"
        fig.savefig(filesave, transparent=True,figsize=(30,30)) 
        
        
        # # Ce  Column Intensity per Slice Bulk
        fig = plt.figure()
        plt.plot(layera,bulkinta1,'-..',label='A1',color='green',mew=3)
        plt.plot(layera,bulkinta2,'-..',label='A2',color='green',mew=3)
        
        plt.legend(loc='upper right')
        plt.title("Bulk Ce Column Intensity for Site A")
        plt.ylabel(r'Intensity (arb. Units)',fontsize=14)
        plt.xlabel("Slice Layer Thickness (Number of layers)",fontsize=14)
        plt.rc('xtick',labelsize=12)
        plt.rc('ytick',labelsize=12)
        plt.tight_layout()
        plt.minorticks_on()
        fig.show()
        filesave=fileprefix+"Bulk-Ce-A-site.png"
        fig.savefig(filesave, transparent=True,figsize=(30,30)) 
        
    ## odd plots B site
    elif slices == 11:
        
        # ODD INDEX'S
        bulkindexb1=[22,26,24,23,26,26,24,22,21,26,21]           # 4 atomic layers x,y
        bulkindexb2=[21,22,25,25,23,21,22,23,25,23,25]           # 4 atomic layers x, 5 atomic layers y
        surfindexb1=[49,50,51,46,50,48,47,49,49,50,50]           # 3 y
        surfindexb2=[46,49,46,49,48,47,46,46,48,46,47]           # 4 y
        layerb=layer
        bulkintb1=[]
        
        for i,atomiclayer in zip(bulkindexb1,range(slices)):
            bulkintb1.append(normalizedint[atomiclayer][i-1])
            
        bulkintb2=[]
        for i,atomiclayer in zip(bulkindexb2,range(slices)):
            bulkintb2.append(normalizedint[atomiclayer][i-1])
            
        surfintb1=[]
        for i,atomiclayer in zip(surfindexb1,range(slices)):
            surfintb1.append(normalizedint[atomiclayer][i-1])
        
        surfintb2=[]
        for i,atomiclayer in zip(surfindexb2,range(slices)):
            surfintb2.append(normalizedint[atomiclayer][i-1])
        
        
        ## PLOT
        # # Ce  Column Intensity per Slice Surface
        fig = plt.figure()
        
        plt.plot(layerb,surfintb1,'-..',label='B1',color='black',mew=3)
        plt.plot(layerb,surfintb2,'-..',label='B2',color='black',mew=3)
        
        plt.legend(loc='upper right')
        plt.title("Surface Ce Column Intensity for Site B")
        plt.ylabel(r'Intensity (arb. Units)',fontsize=14)
        plt.xlabel("Slice Layer Thickness (Number of layers)",fontsize=14)
        plt.rc('xtick',labelsize=12)
        plt.rc('ytick',labelsize=12)
        plt.tight_layout()
        plt.minorticks_on()
        fig.show()
        filesave=fileprefix+"Surf-Ce-B-site.png"
        fig.savefig(filesave, transparent=True,figsize=(30,30)) 
        
        
        # # Ce  Column Intensity per Slice Bulk
        fig = plt.figure()
        plt.plot(layerb,bulkintb1,'-..',label='B1',color='black',mew=3)
        plt.plot(layerb,bulkintb2,'-..',label='B2',color='black',mew=3)
        
        plt.legend(loc='upper right')
        plt.title("Bulk Ce Column Intensity for Site B")
        plt.ylabel(r'Intensity (arb. Units)',fontsize=14)
        plt.xlabel("Slice Layer Thickness (Number of layers)",fontsize=14)
        plt.rc('xtick',labelsize=12)
        plt.rc('ytick',labelsize=12)
        plt.tight_layout()
        plt.minorticks_on()
        fig.show()
        filesave=fileprefix+"Bulk-Ce-B-site.png"
        fig.savefig(filesave, transparent=True,figsize=(30,30))
    


fig = plt.figure()
 
plt.plot(layerb,surfintb1,'.',label='Surf-B1',color='black',mew=3)
plt.plot(layerb,surfintb2,'.',label='Surf-B2',color='black',mew=3)
plt.plot(layera,surfinta1,'.',label='Surf-A1',color='green',mew=3)
plt.plot(layera,surfinta2,'.',label='Surf-A2',color='green',mew=3)

plt.plot(layerb,bulkintb1,'.',label='Bulk-B1',color='black',mew=3)
plt.plot(layerb,bulkintb2,'.',label='Bulk-B2',color='black',mew=3)
plt.plot(layera,bulkinta1,'.',label='Bulk-A1',color='green',mew=3)
plt.plot(layera,bulkinta2,'.',label='Bulk-A2',color='green',mew=3)


plt.legend(loc='lower right')
plt.title("Ce Column Intensity for Site A and B")
plt.ylabel(r'Intensity (Normalized Units)',fontsize=14)
plt.xlabel("Slice Layer Thickness (Number of layers)",fontsize=14)
plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)
plt.tight_layout()
plt.minorticks_on()
#plt.grid()
fig.show()
filesave=fileprefix+"Bulk-Surf-Ce-A-B-site.png"
fig.savefig(filesave, transparent=True,figsize=(30,30))





# ### PER ATOM PLOTS ----------------------
# # FOR A SITE
# fig = plt.figure()
# 
# plt.plot(atom,bulka,'-..',color='red',label="Bulk",mew=3)
# plt.plot(atom,aSurfint,'-..',color='purple',label="Surface",mew=3)
# 
# plt.legend(loc='upper right')
# plt.title("Site A: Per Atom Ce Column Intensity")    
# plt.ylabel(r'Intensity (arb. Units)',fontsize=14)
# plt.xlabel("Intensity Per Atom",fontsize=14)
# plt.rc('xtick',labelsize=12)
# plt.rc('ytick',labelsize=12)
# plt.tight_layout()
# fig.show()
# 
# # FOR B SITE
# fig = plt.figure()
# 
# plt.plot(atom,bulkb,'-..',color='red',label="Bulk",mew=3)
# plt.plot(atom,bSurfint,'-..',color='purple',label="Surface",mew=3)
# 
# plt.legend(loc='upper right')
# plt.title("Site B: Per Atom Ce Column Intensity")    
# plt.ylabel(r'Intensity (arb. Units)',fontsize=14)
# plt.xlabel("Intensity Per Atom",fontsize=14)
# plt.rc('xtick',labelsize=12)
# plt.rc('ytick',labelsize=12)
# plt.tight_layout()
# fig.show()
# 



# # take images to feed to ethan's & barnaby's code
# # give us intensity of all the columns in the exp image