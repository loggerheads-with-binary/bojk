from sys import argv					#Transmit the Arguments Directly
from _pickle import load as p_load 		#Program Name is stored in this section
from subprocess import Popen 			#To Pass the Arguments on
from os import path as OSP

#Very Special Extension Used: ".dtte_data"
#File_Syntax: "*/*.dtte_data"
#DTTE: Dummy Transmission Text Editor

#This file keeps changing based on the Executable Name

pickle_file = OSP.join(   OSP.dirname(OSP.realpath(__file__))      ,
							"Jillian_Cache_Editor.dtte_data")

with open(pickle_file , 'rb') as file:
	editor_name = p_load(file)


Popen(  [ editor_name   ] + argv[1:] )
