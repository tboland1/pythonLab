########################################################################
#                       COMMENTS
# to get soft link command read directy below the comments:
# feff dos plotting file used to 
# store plotting parameters used to plot 
# the dos files from feff in local directory not in python scripts
# to maintain plot upkeep when parameters are changed the 
# python script may remain the same
#########################################################################
# soft link to working python directory commond
# ln -s /home/tboland1/Dropbox/Crozier\ Group\ User-\ Tara\ Boland/3-FEFF/ceria/6-gb/dos-feff.py /home/tboland1/Dropbox/Crozier\ Group\ User-\ Tara\ Boland/scripts/PythonScripts/feff/dos-feff.py
# absolute path to the main directory of interest (where the file of interest is or the directories)
filesave='/home/tara/Dropbox/Crozier Group User- Tara Boland/admin/conferences_workshops/2018/2018_MRS_Spring/Tara_CM06_GBs/'
# list all the directories you wish to plot if multilpe directories
listdir=['0-probe-final-state-7-o137','1-probe-final-state-y-site-o127']
# this is needed for convinence of copy & pasting directories
filespace='/'
# list the SCF value for the feff sim
SCFval='SCF value: 9 '

#############################################
# list the number of ldos data files in files
#############################################
filelist=['ldos01.dat','ldos02.dat']
#filelist=['ldos00.dat','ldos01.dat','ldos02.dat']
#filelist=['ldos01.dat','ldos02.dat','ldos03.dat']
#filelist=['ldos00.dat','ldos01.dat','ldos02.dat','ldos03.dat']


## not normally plotted - for absorbing atom
#file0=filesave+'/ldos00.dat'
## first ATOM DOS data file
#file1=filesave+'/ldos01.dat'
## second Atom DOS data file
#file2=filesave+'/ldos02.dat'
## thirst Atom DOS data file
#file3=filesave+'/ldos03.dat'



