########################################################################
#                       COMMENTS
# to get soft link command read directy below the comments:
# feff eels plotting loadable script file used to 
# store plotting parameters unique to each directory for quick ploting 
# the eels plotting info from each run stay in the local directory, not in python scripts
# to maintain plot upkeep when parameters are changed the 
# python script may remain the same
#########################################################################
# soft link to working python directory commond
# ln -s /home/tboland1/Dropbox/Crozier\ Group\ User-\ Tara\ Boland/3-FEFF/ceria/6-gb/eels-feff.py /home/tboland1/Dropbox/Crozier\ Group\ User-\ Tara\ Boland/scripts/PythonScripts/feff/eelsGBfeff.py
# absolute path to the main directory of interest (where the file of interest is or the directories)

    #set the flag to plot exp data as well    
flag=0          # flag 0 is not exp data | flag 1 exper data
    # absolute path to the data (work comp relative path)
filesave='/home/tara/Dropbox/Crozier Group User- Tara Boland/3-FEFF/ceria/'
    # list all the directories you wish to plot if multilpe directories
listdir=['6-gb']
    # this is needed for convinence of copy & pasting directories
filespace='/'

filelist=['eelsexp.txt']
labels=['Unstrained','Oxidized CeO2 Data']
colors=['black']
figurename='corelossEELS-GB-label.png'
plottitle="O K Edge Bulk Ceria"
disp=[0, 0]
#filesave='../../../3-FEFF/ceria/4-normal/0-data/'





