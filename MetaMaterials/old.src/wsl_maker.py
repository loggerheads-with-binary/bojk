##Updating Script for WSL. 

#Functionality -> Converts stuff to WSL like structure 

import re 
import os 
import yaml 
import _pickle 
from argparse import Namespace , ArgumentParser 

def ValidFile(file):

	if not os.path.exists(file):
		raise FileNotFoundError('No file on the FS')

	file  = os.path.realpath(file)

	if not os.path.isfile(file):

		raise FileNotFoundError('The file is not valid')

	return file 

def arguments():

	parser = ArgumentParser(prog = 'WSL Brian Converter' , description = "Prepare Config Files and Pickle Files between WSL/Linux<--->Windows") 

	parser.add_argument('--op' , '--old-pickle' , action = 'store' , type = ValidFile , dest = 'pickle_old' , 
	help = 'Old Pickle File')

	parser.add_argument('--np' , '--new-pickle' , action = 'store' , type = ValidFile , dest =  'pickle_new'  , 
	help = 'New Pickle File')

	parser.add_argument('--oy' , '--old-yaml' , action = 'store' , type = ValidFile , dest = 'yaml_old' , 
	help = 'Old Yaml file')

	parser.add_argument('--ny' , '--new-yaml' , action = 'store' , type = ValidFile  , dest = 'yaml_new' , 
	help = 'New Yaml File')

	return parser.parse_args() 

def wsl_converter(path):

	import re 

	dir_letter , TrailingPath = re.findall(r'(?P<dir_letter>[A-Z|a-z]+):\\(?P<TrailingPath>.*)' , path)[0]

	b1 = '\\'

	return f"/mnt/{dir_letter.lower()}/{TrailingPath.replace(b1 , '/')}"

def lsw_converter(path):

	import re 	

	dir_letter , TrailingPath = re.findall(r'/mnt/(?P<dir_letter>[A-Z|a-z]+)/(?P<TrailingPath>.*)' , path)[0]

	b1 = '\\'

	return f"{dir_letter.upper()}:{b1}{TrailingPath.replace('/' , b1)}"


converter_func = wsl_converter if os.name == 'nt' else lsw_converter


def read_yaml(yaml_file): 
	
	with open(yaml_file , 'r' , encoding = 'utf-8') as filex:

		data = yaml.load(filex , Loader = yaml.CLoader )

	return data 

def configuration_rewrite(data_dict):



	if os.name == 'nt' : 
		data_dict['Batfile'] = wsl_converter(r'D:\Toolkit\Extra\Brian\MetaMaterials\src\WSL\wslbrian.sh')

	elif os.name == 'posix':

		data_dict['Batfile' ] =  r"D:\Toolkit\Custom\lbrian.cmd"

	data_dict['Abspaths'] = {key : converter_func(value) for key , value in data_dict['Abspaths'].items() }

	data_dict['Defpath'] = converter_func((data_dict['Defpath']))

	if os.name == 'nt' : 

		data_dict['Relpaths'] = {key : value.replace('\\' , '/') for key, value in data_dict['Relpaths'].items() }

	elif os.name == 'posix':

		data_dict['Relpaths'] = {key : value.replace('/' , '\\') for key, value in data_dict['Relpaths'].items() }


	return data_dict 

def write_yaml(data_dict , yaml_file):

	with open(yaml_file , 'w+' , encoding = 'utf8') as filex:

		yaml.dump(data_dict, filex)

	return None 

jillian_converter = lambda yaml_file_input , yaml_file_output : write_yaml(  configuration_rewrite(read_yaml(yaml_file_input))   , yaml_file_output)

def pickle_rewrite(input_file , output_file) : 

	with open(input_file, 'rb'  ) as filex:

		data = _pickle.load(filex)
	
	#prin[0]) 
	#exit() 
	
	data = {  converter_func(str(path))  for path in data  }

	with open(output_file , 'wb' ) as filex: 

		_pickle.dump(data , filex )


	return None 

if __name__ == '__main__' : 

	item = arguments() 

	jillian_converter(item.yaml_old , item.yaml_new)

	pickle_rewrite(item.pickle_old , item.pickle_new)