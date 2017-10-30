#! /usr/bin/python

#------------------------------------------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------------------------------------------ 
# Author: Michael Wolloch, center for computational material science (CMS), TU Wien; mwo@cms.tuwien.ac.at
# Date: September, 20th, 2015
# Version: 1.0; Complete rewrite of an old bashscript/fortran77 hybrid by the same author
#------------------------------------------------------------------------------------------------------------------ 
# Purpose of the script:
# This script can be used to quickly find accurate band gaps from the most basic output file of the DFT code VASP,
# the OUTCAR. After almost any calculation the OUTCAR is kept, even if the DOSCAR or EIGENVALUE file are not, thus
# the script is based on this file.
# The main idea is going through the list of Kpoints and checking the occupancy of each band and its energy.
# Output is written to the screen and into the file "GG.out". If this file exists already it will be appended.
#------------------------------------------------------------------------------------------------------------------ 
# The motivation for rewriting this script comes mainly from the wish to learn python. Thus it is certain that it
# is written in an inperfect way. Feel free to adapt it and improve it if you want, but I would appreciate it if you
# could send me a mail if you do. Especially if you find a bug!
#------------------------------------------------------------------------------------------------------------------ 
# The script has been tested for several systems (ISPIN = 1 and 2; metals, semiconductors, insulators,...) and 
# VASP versions (5.2, 5.3, 5.4) but no guarantuee can be given that the results are correct for your system. 
# Be also advised that bandgaps are usually incorrect with standard GGAs and advanced methods might be needed
# (hybrid functionals, GW, RPA).
#------------------------------------------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------------------------------------------

import os.path

# Defining DOS class to analyze data for one spin channel and return HOMO, LUMO, Gap (direct and indirect), or metallic state
#------------------------------------------------------------------------------------------------------------------
class DOS:
	name = ""										# Name of DOS (spin up or down)
	Data = [0,0]									# 2D list for energy and occupation number
	NKpts = 0										# Number of K-points
	NBands = 0										# Number of bands
	DGap = 0										# Smallest direct gap
	DGapKp = 0										# Kpoint with smalles direct gap
	HOStKp = 0										# Kpoint with highest occupied state
	LUStKp = 0										# Kpoint with lowest unoccupied state
	Gap = 0											# Global gap (might be indirect)
	Met = False										# Switches to true if the spin channel is metallic (partial occupations)

	def __init__(self,name,Data,NKpts,NBands):		# Input data
		self.name = name
		self.Data = Data
		self.NKpts = NKpts
		self.NBands = NBands
	
	def GetGaps(self):								# Calculate Gaps, HOSt, LUSt, etc.
		NonMet=[1.0, 2.0, 0.0]						# All other occupation numbers indicate a metallic state
		Occ=[1.0,2.0]								# Possible occcupation numbers for full occupation
		self.LocHOSt=-10000000							# Setting low initial limit for highest occupied state	
		self.LocLUSt=10000000							# Setting high initial limit for lowest unoccupied state
		self.HOSt = []								# Array for local highest occupied state
		self.LUSt = []								# Array for local lowest unoccupied state
		self.D_Gaps = []							# Array for direct gaps
		for k in range(0,Nkpts):
			for b in range(0,Nbands):
				if self.Data[k*Nbands+b][1] not in NonMet:
					self.Met=True
				elif self.Data[k*Nbands+b][1] in Occ and self.Data[k*Nbands+b][0] > self.LocHOSt:
					self.LocHOSt=self.Data[k*Nbands+b][0]
				elif self.Data[k*Nbands+b][1] == 0.0 and self.Data[k*Nbands+b][0] < self.LocLUSt:
					self.LocLUSt=self.Data[k*Nbands+b][0]
			self.D_Gaps.append(self.LocLUSt-self.LocHOSt)
			self.HOSt.append(self.LocHOSt)
			self.LUSt.append(self.LocLUSt)
			self.LocHOSt = -10000000
			self.LocLUSt =  10000000
		self.DGap, self.DGapKp = min((self.DGap, self.DGapKp) for (self.DGapKp, self.DGap) in enumerate(self.D_Gaps,1))
		self.LUStKp = self.LUSt.index(min(self.LUSt))+1
		self.HOStKp = self.HOSt.index(max(self.HOSt))+1
		self.Gap = min(self.LUSt)-max(self.HOSt)
#------------------------------------------------------------------------------------------------------------------

# Function for on screen output		
#------------------------------------------------------------------------------------------------------------------
def screen_print(d_gap,d_gapkp,tot_gap,tot_gapKp1,tot_gapKp2,met):
	if met == True:
		print "   This spin channel is metallic."
	else:
		print " The smallest direct gap is " +str(d_gap)+ " eV at K-point Nr.: " +str(d_gapkp)+ "."
		print " The global bandgap is " +str(tot_gap)+ " eV beween K-points " +str(tot_gapKp1)+ " and " +str(tot_gapKp2)+ "."
		print " "
#------------------------------------------------------------------------------------------------------------------

# Function for file output
#------------------------------------------------------------------------------------------------------------------
def file_print(NSpin, MetUp, MetDo, tot_gap_up, tot_gap_down, d_gap_up, d_gap_down):
	if MetUp == True:
			tot_gap_up = 0
			d_gap_up = 0
	if MetDo == True:
			tot_gap_down = 0
			d_gap_down = 0
	if os.path.isfile("GG.out") == True:
		try:
			out = open("GG.out", "a")
		except IOError:
			print " "	
			print " Error opening output file, results are only written to screen."
			print " "
		if NSpin == 2:
			out.write(str("{0:21.3f} {1:22.3f} {3:22.3f} {3:23.3f} \n").format(tot_gap_up, tot_gap_down, d_gap_up, d_gap_down))
		elif NSpin == 1:
			out.write(str("{0:21.3f} {1:>22s} {2:22.3f} {3:>23s} \n").format(tot_gap_up, "-", d_gap_up, "-"))
		out.close()
	else:
		try:
			out = open("GG.out", "w")
		except IOError:
			print " "	
			print " Error opening output file, results are only written to screen."
			print " "
		out.write("%   total gap spin up    total gap spin down     direct gap spin up    direct gap spin down\n")
		if NSpin == 2:
			out.write(str("{0:21.3f} {1:22.3f} {3:22.3f} {3:23.3f} \n").format(tot_gap_up, tot_gap_down, d_gap_up, d_gap_down))
		elif NSpin == 1:
			out.write(str("{0:21.3f} {1:>22s} {2:22.3f} {3:>23s} \n").format(tot_gap_up, "-", d_gap_up, "-"))
		out.close()
#------------------------------------------------------------------------------------------------------------------

# Open OUTCAR file for reading
try:
	f = open("OUTCAR", "r")
except IOError:
	print " "	
	print " Error opening OUTCAR"
	print " "
	quit()

if 'k-point     1 :' in f.read():					# VASP has switched Output format between 5.2 and 5.3,
	kpoint_check="k-point     1 :"					# this should now work in both (all?) cases
else:
	kpoint_check="k-point   1 :"
f.seek(0,0)											# Rewind OUTCAR file
	

LineNr=[]											# Initialize line number array
Data=[]												# Initializing array for bandenergy and occupation data

# reading information out of OUTCAR
for count, line in enumerate(f,1):
	if "SYSTEM =" in line:							# Getting system name
		SysName = line.split()[2]
	if "ISPIN  =" in line:							# Determine if calculation was spin polarized
		Spin = int(line.split()[2])
	if kpoint_check in line:						# Determine number of ionic steps.
		LineNr.append(count)						# Get line number of startpoints of data
	if "NKPTS =" in line:							# Determine number of bands and K-points
		Nbands = int(line.split()[14])
		Nkpts = int(line.split()[3])
		

# Determining the beginning end end of relevant data lines and setting read pointer
if Spin == 1:
	StartLine=LineNr[-1]
	EndLine=StartLine+Nkpts*Nbands+Nkpts*3
elif Spin == 2:
	StartLine=LineNr[-2]
	EndLine=StartLine+2*Nkpts*Nbands+2*Nkpts*3
else:
	print " "	
	print " Error encountered regarding spin states. Aborting. "	
	print " "	
	quit()
f.seek(0,0)											# Rewind OUTCAR file

# List of first words in lines to discard
not_these=["k-point", "band", "spin"]

#filling data array
for count, line in enumerate(f,1):
	if not line == '\n':							# Discarding empty lines
		if count >= StartLine and count <= EndLine and line.split()[0] not in not_these:
			Data.append([float(line.split()[1]), float(line.split()[2])])


# Close OUTCAR file again
f.close()


# Distinguish between ISPIN = 1 and ISPIN = 2, calculate bandgaps and print to screen and file
if Spin == 1:
	SpinBo=DOS("Both",Data,Nkpts,Nbands)
	SpinBo.GetGaps()
	print " "
	print " "
	print " Bandgaps for the system: '" + SysName + "' have been evaluated:"
	print " " + str(Nkpts) + " K-points and " + str(Nbands) + " bands have been found."
	print " No spin splitting found for this system."
	print " "
	screen_print(SpinBo.DGap, SpinBo.DGapKp, SpinBo.Gap, SpinBo.HOStKp, SpinBo.LUStKp, SpinBo.Met)
	file_print(Spin,SpinBo.Met,SpinBo.Met,SpinBo.Gap,SpinBo.Gap,SpinBo.DGap,SpinBo.DGap)
elif Spin ==2:
	Data1=Data[:len(Data)/2]
	Data2=Data[len(Data)/2:]
	SpinUp=DOS("Up",Data1,Nkpts,Nbands)
	SpinUp.GetGaps()
	SpinDo=DOS("Down",Data2,Nkpts,Nbands)
	SpinDo.GetGaps()
	print " "
	print " "
	print " Bandgaps for the system: '" + SysName + "' have been evaluated:"
	print " " + str(Nkpts) + " K-points and " + str(Nbands) + " bands have been found."
	print " "
	print " Spin Up: "
	screen_print(SpinUp.DGap, SpinUp.DGapKp, SpinUp.Gap, SpinUp.HOStKp, SpinUp.LUStKp, SpinUp.Met)
	print " Spin Down: "
	screen_print(SpinDo.DGap, SpinDo.DGapKp, SpinDo.Gap, SpinDo.HOStKp, SpinDo.LUStKp, SpinDo.Met)
	print " "
	file_print(Spin,SpinUp.Met,SpinDo.Met,SpinUp.Gap,SpinDo.Gap,SpinUp.DGap,SpinDo.DGap)