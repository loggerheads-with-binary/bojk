from argparse import ArgumentParser , Namespace 
from _pickle import dump as p_dump 
from os import path as OSP 

def arguments():

	parser = ArgumentParser() 

	#Pickle File and Text Editor Executable Path 

	parser.add_argument(	'-f' , '--file' , dest = 'pickle_file' , action = 'store' , required = True , 
							help = "Pickle/Data Variable File that needs to be appended")

	parser.add_argument(	'-t' , '--text-editor' , dest = 'text_editor' , action = 'store' , required = True ,
							help = "Text Editor Executable Path"		)

	return parser.parse_args()


if __name__ == '__main__':

	parser = arguments()

	#Check if Pickle File Exists 
	if not OSP.exists(parser.pickle_file):

		raise OSError(f"The Pickle File `{parser.pickle_file}` does not exist on the FileSystem")


	#Check if the Text Editor Executable Exists 
	#However, this path should also be an absolute path 

	parser.text_editor = OSP.realpath(parser.text_editor)

	if not OSP.exists(parser.text_editor):
		raise OSError(f"The Text Editor Executable `{parser.text_editor}` does not exist on the FileSystem") 


	with open(parser.pickle_file , 'wb') as file:
		p_dump(parser.text_editor , file)