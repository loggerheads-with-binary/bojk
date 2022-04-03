"""
Module Name: BOJK -> Brian on Jillian Kernel.
An APIable python script based executable which renders changing to directories super easy
Mode of usage: Check [python bojk.py -h] or [bojk.exe -h], depending on what program you're using for help regarding arguments
"""

"""Logging BOJK"""
import logging
import inquirer
import coloredlogs

coloredlogs.install(fmt = '%(asctime)s || BOJK-%(levelname)s : %(message)s')
logging.basicConfig(format = "BOJK-%(levelname)s: %(message)s")

logging.log( level = 101 , msg = "Configuring the Brian on Jillian Kernel\n")

"""		Parsers - Arguments and YAML	"""
from argparse import ArgumentParser , Namespace
from yaml import CLoader, load as yaml_load , dump as yaml_dump , CDumper
import yaml

"""		Pretty Printing Contents	"""
from termcolor import colored, cprint as termcolor_cprint
from colorama import init as colorama_init , deinit as colorama_deinit
import termtables

"""		Search Engine Functionality		"""
from rapidfuzz import fuzz

""" 	Obtaining Max Elements from Search Engine results	"""
from heapq import nlargest

"""		Path and Folder Functionalities		"""
from os import path as OSP , getcwd, name as os_name
import os
from scandir import walk as scandir_walk , listdir as scandir_listdir
import pathlib

"""		For some goddamn reason, Nuitka doesn't properly compile python exit in a --standalone set.
		And which is why sys.exit has to be used	"""
from sys import exit

"""		Using Cache for the Program 		"""
from _pickle import load as p_load, dump as p_dump

"""		For Final Output to be Copied 		"""
from pyperclip import copy as pyperclip_copy

colorama_init()

path_ = OSP.dirname(os.path.abspath(__file__))


from Shell_Specificity import 	design_ , \
								prog_name , \
								change_dir_command , \
								start_dir_command , \
								default_file , \
								compulsory_first_line,\
								pushd_dir_command


yaml_data = dict()

def cprint(text : str , color : str = 'cyan' , end = '\n'):

	"""
	Custom cprint function based on termcolor being used or not.
	Red color text is always printed red since it could be a possible error
	Use the line of code, bojk.use_termcolor_var = True before using cprint for a color print in API
	"""

	global use_termcolor_var

	if color == 'red':
		#Should always be printed as red

		termcolor_cprint(text , color = color , end = end)


	elif use_termcolor_var:
		termcolor_cprint(text , color = color , end = end)

	else:
		print(text , end = end )

	return True

def BOJKError(msg = ''):

	"""Just an Error Message Formatting"""

	#cprint(msg , 'red')
	logging.critical(f"BOJKERROR: {msg}" )
	exit()

use_termcolor_var = False

def check_all_tries_for_path(path):

	"""
	APIable function
	Creates a YAML File in the current directory.
	Parameters: path -> Default filename you want to try
	It checks for all the files possible, [probably file already exists], so it returns a possible filename
	"""

	#Create and return a useful unused path

	if OSP.exists(path):

		filename , ext = OSP.splitext(str(path))

		i = 1

		while True:

			file_ = filename + f'[{i}]' + ext

			if not OSP.exists(file_):
				break

			i = i + 1

	else:
		file_ = path

	return file_

def dns(query: str , path: str , case_sensitivity : bool = False):

	"""
	APIable Function: Returns a suitable score in [0,100] based on the three Fuzzy String Algorithms:
	partial_ratio
	token_set_ratio
	token_sort_ratio

	Parameters: query: str -> Search Query
				path: str -> Technically the path. However, both query and path can both the anything. There is no polarity in the search
				case_sensitivity : bool -> If set to false, the cases are not taken into consideration.
	"""



	##Only to be used on Windows Machines

	if not case_sensitivity:
		query = query.lower()
		path = path.lower()

	partial_ = fuzz.partial_ratio( query , path)
	set__ = fuzz.token_set_ratio(query , path)
	sort__ = fuzz.token_sort_ratio(query , path)


	return (partial_ + set__ + sort__ )/3

def final_output_driver(path : str , action_var : str = 's' , batfile = None, output_var : str = 'b'):

	"""
	Non APIable function for non windows machines. Does the final job from the output including writing the batchfile, copying on the clipboard and printing on the terminal
	Parameters: path : str -> Output path
				action_var : str -> 's' implies shell only[ only change directory]
									'so' implies both shell and explorer [cd and start folder]
									'o' implies only explorer open[start the folder]
				Note action_var is valid only for the batch file. Though you can pass it for other modes, they don't make any sense

				batfile : path -> In case the machine is Windows, this is the path to write onto.

				output_var : str -> 'b' implies write onto the batchfile
									'c' implies copy to the clipboard
									'p' implies print onto the terminal
	"""

	global BOJKError

	path = OSP.abspath(path)

	if output_var == 'b':

		"""
		Appends Content to the Batch File using the action_var variable
		action_var = None -> Write to change directory to the given path
		action_var = 'o' -> Write to open directory in explorer.exe
		action_var = 'so' -> Do both opening in explorer.exe and in the shell
		This works only for the batch file
		"""

		#Write Batch File
		with open(batfile , 'a') as file:

			if 's' ==action_var :

				file.write(f'{change_dir_command(path)}\n')

			elif 'o' == action_var:

				file.write(f'{start_dir_command(path)}\n')

			elif 'so' == action_var :

				file.write(f'{start_dir_command(path)}\n{change_dir_command(path)}\n')

			elif 'p' == action_var :

				file.write(f'{pushd_dir_command(path)}\n')

			elif 'po' == action_var :

				file.write(f'{pushd_dir_command(path)}\n{start_dir_command(path)}\n')

		logging.info("Shell File Created.")

	elif output_var == 'c':
		pyperclip_copy(str(path))
		logging.info("Path copied to the clipboard")

	elif output_var == 'p':
		logging.critical("Here is the directory on the next line in plaintext ")
		cprint(path , 'cyan')

	return None

def show_search(objects : list = [(None , 100)] , defpath = '/' , query = '' ):

	"""
	APIable function
	Shows the search of the items onto the screen for user acceptance.
	Parameters : 	objects : list[path , int] -> List of list/tuples with each list/tuple with [ path , search_accuracy ] for user to choose from
					defpath :  -> Was used initially in BOJK. Needn't pass anything to the defpath
					query: str -> The query which was searched against


	Should be a list of tuples. The 1st item in the tuple should be the returnable.
	The second represents accuracy though it can be anything else tbh
	"""

	choices_ = [item [0] for item in objects]
	choices_.append(None)

	n = len(objects)

	questions = [
	 				 inquirer.List('dir_',
	                message="Which Directory should BOJK Open for you?",
	                choices= choices_ , #['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
	                default = choices_[0] ,
	                carousel = True ,
	            ),
	]

	dir_ = inquirer.prompt(questions)['dir_']

	if dir_ == None:

		logging.critical("User has chosen to not select any directory")
		exit()

	else:
		return dir_


	"""


	global BOJKError

	n = len(objects)

	to_print =  list()

	for i , item in enumerate(objects):

		to_print.append( [ i+1 ,  query , item[0] , item[1] ]  )
		#Query Index + 1 , Query , Path , Accuracy

	#Query index should be choosable
	headers = ["No" , "Query" , "Path" , "Accuracy"]


	to_print = termtables.to_string(   to_print ,
							header = headers ,
							style = termtables.styles.ascii_thin_double)

	#This code can be changed for printing improvements
	to_print_lines = to_print.split('\n')

	for line in to_print_lines:
		if line.startswith('+'):
			cprint(line , 'yellow')

		else:
			cprint(line, 'green')

	#cprint(to_print, 'magenta')
	#Changeable Code Ends Here

	cprint('\nWhat should BOJK choose for you?: ' , 'cyan' , end = '')
	query_index = input('').strip()

	if query_index.isdigit() == False:
		BOJKError(f"Index {query_index} is invalid in range(1 , {n})")

	query_index = int(query_index)

	if (query_index > n) or (query_index < 1):

		BOJKError(f"Index {query_index} is invalid in range(1 , {n})")

	else:
		dir_ = objects[query_index - 1][0]

	return dir_

	"""

##Returns If the Actual Path is a file, parses symlinks too
def find_all_dirs_backend(file):

	if os.path.isfile(file):

		return None
		#return ( True, None)

	elif os.path.isdir(file):

		return file
		#return ( False , file)

	file = os.path.realpath(file)

	if os.path.isdir(file):

		return file

def solely_check_file_type(file):

	if os.path.isfile(file):

		return True

	elif os.path.isdir(file):

		return False

	return os.path.isfile(os.path.realpath(file))

def find_all_dirs(path):

	#global main_list

	main_list = { os.path.abspath(file) }

	for item in scandir_listdir(path) :

		fp =  os.path.join(path , item)

		s_  = find_all_dirs_backend(fp)

		if s_ != None:

			main_list.update(find_all_dirs(fp))

	return main_list

def sbf_search_engine(path , query : str  , case_sensitivity : bool  = False , full_path: bool = False ):

	main_list = set()

	xx_ = [ ( find_all_dirs_backend(os.path.join(path , item)) , dns(query , os.path.join(path , item ) if full_path else item , case_sensitivity= case_sensitivity) ) for item in scandir_listdir(path)]

	if len(xx_) > 0 :

		main_list.update( { ( os.path.abspath(path) , max(xx_ , key = lambda x9: x9[-1])[-1] ) } )

	for item , dns_val in xx_ :

		if item != None :

			main_list.update(sbf_search_engine(item, query , case_sensitivity , full_path) )

	return main_list

def search_engine( query : str , mode : str  , defpath = '/' , cache_file = 'Directories.bojk' , return_index : int = 5 , full_path : bool = False , case_sensitivity : bool = False):

	r"""
	APIable function. Returns a list of lists -> list[ [ directory, search_accuracy    ]     ]
	Parameters: query : str -> The query which has to be searched against
				mode: str -> 	'c' -> Use the cache file given [cache_file compulsory]
								'w' -> Walk the defpath [defpath compulsory]
								'f' -> Search by File Mode (Walks defpath by default. Cannot use cache)  [defpath compulsory]
				defpath : path like object -> Path to be walked (directories of this folder will be searched for the results), should be specified in case of using walk mode
				cache_file : path like object -> Cache file with stored directory list, should be properly specified in case of using cache mode
				return_index : int -> How many search results should be returned
				full_path : bool -> Should the directory name's entire path be used. By default only directory name is used
									Ex: for "C:\Users\NoobCoder\Desktop" if full_path is True; "C:\Users\NoobCoder\Desktop" will be used otherwise "Desktop" will be used
				case_sensitivity : bool -> Should the searches be case sensitive. Technically more useful in Linux Machines. Set to False by default. Which is useful for Windows Machines
	"""

	#global main_list

	search_paths = list()

	if mode == 'c':
		#Use cache

		with open(cache_file , 'rb') as file:

			all_paths = p_load(file)

		if full_path:

			search_paths = { ( item , dns(query , item , case_sensitivity= case_sensitivity))  for item in all_paths }

		else:

			search_paths = { (item  , dns(query , OSP.split(item)[-1] , case_sensitivity= case_sensitivity)) for item in all_paths    }

		del all_paths

	elif mode == 'w':
		#Walking The Directories


		main_list = find_all_dirs(defpath)

		if full_path :

			search_paths = {  (item , dns(item , query, case_sensitivity= case_sensitivity) ) for item in main_list  }

		else:

			search_paths = { (item , dns(os.path.split(item)[-1], query , case_sensitivity= case_sensitivity)) for item in main_list }

		del main_list

		# for directory , paths , files in scandir_walk(defpath):

		# 	for single_path in paths:

		# 		ind_path = OSP.join(directory , single_path)

		# 		if full_path:
		# 			search_paths.append([ind_path , dns(query , ind_path , case_sensitivity= case_sensitivity)])

		# 		else:
		# 			search_paths.append([ind_path , dns(query , single_path , case_sensitivity= case_sensitivity)])

	elif mode == 'f':
		#Search by File

		search_paths = sbf_search_engine(defpath , query , case_sensitivity= case_sensitivity , full_path= full_path)


		# main_list = [defpath]
		# main_list.extend(find_all_dirs(defpath))

		# for item in main_list :

		# 	s_ = [dns(query , file , case_sensitivity= case_sensitivity)  for file in scandir_listdir(item) if check_file_type(file)[0]]

		# 	if len(s_) > 0 :

		# 		search_paths.append(( item , max(s_) ) )

		# for directory, _ , files in scandir_walk(defpath):

		# 	temp_dirs_list = list()

		# 	temp_dirs_list = [  dns(file , query , case_sensitivity= case_sensitivity)  for file in files   ]

		# 	if len(temp_dirs_list) >0:

		# 		max_accuracy = max(temp_dirs_list)

		# 		search_paths.append([directory , max_accuracy])

	logging.info("BOJK Search Assignment Operation Completed")

	return nlargest(return_index , search_paths , key = lambda x: x[-1])

def brian_driver(parser : Namespace , data_dict : dict = None):

	"""APIable function(somewhat):

	Checks for the commands or search as needed. And calls other relevant functions as needed.

	parser : argparse.Namespace -> Namespace object similar to the output from the arguments() function.
	data_dict : dict -> Dictionary similar to the YAML file dictionary.
	"""

	global BOJKError

	if data_dict == None:
		global yaml_data
		data_dict = yaml_data

	##Check Configuration

	if not (parser.command == None):
		#Command exists

		dir_ = data_dict['Abspaths'].get(parser.command , None)

		if dir_ == None:

			#Result not found in Abspaths

			dir_ = data_dict['Relpaths'].get(parser.command , None)

			if (dir_ == None) :

				#Results not found in relpaths

				#Check for Failsafe
				if not (data_dict.get('Command_Failsafe' , None) == True):

					logging.info("The command was not found in the configuration")
					logging.critical("The program now exits")
					exit()

				#Try Rapidfuzz

				logging.warning("The command was not found in configuration. Using Search Engine Functionality")

				paths_ = list()
				defpath_ = data_dict['Defpath']

				for key, value in data_dict['Abspaths'].items():

					paths_.append((value , dns(key , parser.command)))

				for key, value in data_dict['Relpaths'].items():

					value = OSP.join(defpath_ , value)

					paths_.append((value , dns(key , parser.command)))

				"""Find User Answer"""

				#dir_ = sorted(paths_ , key = lambda x:x[-1] , reverse = True)[0][0]
				dir_ = max(paths_ , key = lambda x: x[-1])[0]

				#Reducing the complexity from n^2 to n


				confirm = {
						    inquirer.Confirm('confirmed',
						                     message= f"Do you wish to use this path {dir_}?" ,

						                     default=True),
						}

				answer = inquirer.prompt(confirm)["confirmed"]

				#OLD BOJK CODE
				"""
				answer = None

				while answer not in ['y' , 'n']:

					cprint("Should we use this path?: ", 'yellow' , end = '')
					cprint(dir_ + ':', 'red' , end = '')

					answer = input("	").strip().lower()
				"""


				if answer:
					return dir_
					#final_output_driver(dir_ , parser.action_var , data_dict['Batfile'] , parser.output_var)

				else:
					logging.critical("Sorry we couldn't find the relevant path.." )

			else:
				dir_ = OSP.join(data_dict['Defpath']  , dir_)
				return dir_
				#final_output_driver(dir_ , parser.action_var , data_dict['Batfile'] , parser.output_var)


		else:
			return dir_
			#final_output_driver(dir_ , parser.action_var , data_dict['Batfile'] , parser.output_var)

	elif not (parser.search_ == None):

		dir_objects = search_engine(parser.search_ , parser.search_mode , data_dict['Defpath'] ,
							parser.cache_file , data_dict['Return_Index'] , parser.full_path_var)

		dir_ = show_search(objects = dir_objects , defpath = data_dict['Defpath'] ,
		query = parser.search_)

		if not (dir_ == None):
			return dir_
			#final_output_driver(dir_ , parser.action_var , data_dict['Batfile'] , parser.output_var)

	else:
		BOJKError("Choose some option at least")

	return None

def initialize(cache_file , defpath):

	"""
	APIable function.
	Parameters:	cache_file : path to a file -> To be used as the cache file for the cache output
				defpath : path to a directory -> Directory to be walked
	"""

	global BOJKError

	all_paths = set(find_all_dirs(defpath))


	with open(cache_file , 'wb') as file:


		p_dump(all_paths , file)

	logging.critical("Cache Initialiation Complete" )

	return None

def arguments():

	"""
	To be modified before using as an API
	In the raw form it is not an APIable function due to python programming concerns.
	Better copy this function
	"""

	global design_ , prog_name

	parser = ArgumentParser(prog = prog_name , description = f"Brian on Jillian Kernel[BOJK] is a master directory change program based on a highly complex set of commands inspired from 'roscd' command. Check arguments for usage. Current BOJK is designed for {design_}" )

	parser.add_argument('-o' , '--open' , dest = 'action_var' , action = 'store_const' , const = 'o' , default = 's' ,
	help = 'Opens the directory in the explorer')

	parser.add_argument('--so' , '-so' , '--shell-and-open' , dest = 'action_var' , action = 'store_const' , default = 's' , const = 'so' ,
	help = "Opens the final obtained directory both in the shell and in explorer" )

	parser.add_argument('-c' , '--command' , dest = 'command' , action = 'store' , default = None , metavar = "Command" ,
	help = 'Use a command from the YAML like Configuration file.')

	parser.add_argument('-s' , '--search-engine' , '--search' , dest = 'search_' , action = 'store' , default = None , metavar = "Search_Term" ,
	help = 'Search for this directory')

	parser.add_argument('--fp' , '--full-path-search' , dest = 'full_path_var' , action = 'store_true' ,
	help = 'Forces the search engine to search for the entire path. Defaults to only directory name')

	parser.add_argument('-f' , '--config' , dest= 'config_var' , action = 'store' , const = [] , nargs = '?' , default = None ,
	help = 'Shows the present configuration using the YAML like Configuration File. Syntax: <Path> -f/--config [options to choose]')

	parser.add_argument('-y' , '--yaml' , dest = 'yaml' , action = 'store' , default = OSP.join(getcwd() , 'config.jillian') , metavar = "<PATH to YAML FILE>" ,
	help = 'Change the YAML like configuration file. Default is `config.jillian` in the current working directory')

	parser.add_argument('-V' , '--version' , dest = 'first_action' , action = 'store_const' , const = 'version' , default = None ,
	help = 'Show details about version of BOJK')

	parser.add_argument('-u' , '--usage' , dest = 'first_action' , action = 'store_const' , const = 'usage' , default = None ,
	help = 'Show how to use Brian on Jillian Kernel')

	parser.add_argument('-g' , '--generate' , '--create' , '--touch' , dest = 'first_action' , action = 'store_const' , const = 'gen' , default = None ,
	help = 'Generate a blank config YAML like file in the current working directory')

	parser.add_argument('-i' , '--init-cache' , dest = 'first_action' , action = 'store_const' , const = 'init' , default = None ,
	help = 'Initialize the BOJK Cache feature which can be used later')

	parser.add_argument('--cache-file' , dest = 'cache_file' , action = 'store' , default = OSP.join(path_ , "docs" , 'Directories.bojk') , metavar = "<PATH to CACHE FILE>" ,
	help = 'Cache File to be used for BOJK. Default to `Directories.bojk`in the docs folder within the program folder')

	parser.add_argument('--uc' , '--use-cache' , dest = 'search_mode' , action = 'store_const' , default = 'w' , const = 'c' ,
	help = 'Use Cache Instead of Walking the Folders in Realtime for the Search Engine Functionality')

	parser.add_argument('--sbf' , '--search-by-file' , dest = 'search_mode' , action = 'store_const' , const = 'f' , default = 'w' ,
	help = 'Searches the directory based on the files inside it. NOTE CACHE FEATURE CANNOT BE USED FOR THIS MODE')

	parser.add_argument('--tc' , '--term-color' , dest = 'color_var' , action = 'store_true' ,
	help = 'If flagged, the terminal prints a very colorful text. Sets to OFF by default' )

	parser.add_argument( '-C'  ,'--copy' , dest = 'output_var' , action = 'store_const' , default = 'b' , const = 'c' ,
	help = 'Copy the final output folder instead of changing directory into it')

	parser.add_argument('-P' , '--print' , dest = 'output_var' , action = 'store_const' , default = 'b' , const = 'p' ,
	help = 'Print the final output on the screen')

	parser.add_argument('-p' , '--pushd' ,
						dest = 'action_var' , action = 'store_const' , const = 'p' , default = 's' ,
						help = 'Push the directory on the shell stack, i.e. the `pushd` command')

	parser.add_argument('--po' , '--pushd-and-open' ,
						dest = 'action_var' , action = 'store_const' , const = 'po' , default = 's' ,
						help = 'Push the directory and open it in the explorer.')

	parser.add_argument('-E' , '-e' , '--edit' , dest = 'first_action' , action = 'store_const' , const = 'edit' , default = None ,
	help = 'BETA functionality: Edit the configuration[YAML File]. uses Ipython Backend. ')

	return parser.parse_args()

def config_print(yaml_file = None , configuration_ = 'all' ):

	"""
	Non APIable function
	Prints all relevant BOJK data
	Case Insensitive variable configuration_
	"""

	global yaml_data , BOJKError

	if not (yaml_file == None):

		with open(yaml_file , 'r') as filex:

			yaml_data = yaml.load(filex , Loader = yaml.CLoader)

		logging.info("The Configuration Data has been loaded\n")


	assert isinstance(yaml_data , dict) or isinstance(yaml_data , defaultdict) , f"The Loaded Data needs to be of type dictionary/defaultdict. Not {type(yaml_data)}"

	options_dict = {
		'all' : 'ALL' ,
		'ctrl' : "Control Variables" ,
		'abspaths' : "Absolute Paths" ,
		'relpaths' : "Relative Paths" ,
		'defpath' : 'Default Path' ,
		'batfile' : 'Shell File Path'  ,
		'return_index' : 'Search Engine Default Total Searches' ,
		'command_failsafe' : 'Command Failsafe Mode' ,
		'none' : None
	}

	if configuration_ == [] :

		questions = [
		  inquirer.List('choice',
		                message= "What do you want to check in the BOJK Configuration?",
		                choices= options_dict.values(),
		            ),
		]

		configuration_ = inquirer.prompt(questions)["choice"]

	else:

		if configuration_.lower() not in options_dict:

			logging.critical(f"The option {configuration_} is not allowed on the system. Allowed options are {list(options_dict.keys())} in arguments, or give no arguments for the interactive prompt\n\n")

			return None

		configuration_ = options_dict.get(configuration_.lower() , False)

	#Configuration_ has now been converted to the choice

	if configuration_ == "ALL":

		config_print(None , 'ctrl')
		config_print(None , 'abspaths')
		config_print(None , 'relpaths')

	elif configuration_ == None:

		logging.warning("The user has chosen to not show any parts of the configuration. Program Exiting")

	elif configuration_ == "Control Variables" :

		logging.info(f"BOJK Program File: [{os.path.abspath(__file__) }]")
		logging.info(f"Shell File used for Control: [{yaml_data['Batfile']}]")
		logging.info(f"YAML like Configuration File under consideration: [{yaml_file}]")
		logging.info(f"Default Search Path: [{yaml_data['Defpath']}]")
		logging.info(f"The Return Index for Search Engine Results: [{yaml_data['Return_Index']}] ")
		logging.info(f"Command-Failsafe Search Engine Mode: [{'Operational' if yaml_data['Command_Failsafe'] else 'Not Operational'}]\n\n")

	elif configuration_ == "Absolute Paths" :

		headers = [  "Command" , "Path"  ]

		data_list = list(yaml_data['Abspaths'].items())

		if len(data_list) == 0:

			logging.info("There are no absolute path commands in the current configuration\n\n")
			return None

		else:
			logging.info("These are the absolute paths in the current configuration")
			print('')
			##Ome Empty Lines


		to_print = termtables.to_string( data_list   ,
								header = headers ,
								style = termtables.styles.ascii_thin_double)

		#This code can be changed for printing improvements
		to_print_lines = to_print.split('\n')

		for line in to_print_lines:
			if line.startswith('+'):
				cprint(line , 'yellow')

			else:
				cprint(line, 'green')

	elif configuration_ == "Relative Paths" :

		relpath_ = yaml_data['Defpath']


		logging.info(f"Defpath: {relpath_}")

		headers = [  "Command" , "Absolute Path"  ]

		data_list = list(yaml_data['Relpaths'].items())

		if len(data_list) == 0:

			logging.info("There are no relative path commands in the current configuration\n\n")
			return None

		else:

			data_list = [ ( key , OSP.join(relpath_ , value) )  for key , value in data_list ]


			logging.info("These are the following commands relative to the defpath ONLY!")
			print('')
			#One Empty Line

		to_print = termtables.to_string( data_list   ,
								header = headers ,
								style = termtables.styles.ascii_thin_double)




		#This code can be changed for printing improvements
		to_print_lines = to_print.split('\n')

		for line in to_print_lines:
			if line.startswith('+'):
				cprint(line , 'yellow')

			else:
				cprint(line, 'green')

	elif configuration_ =='Default Path' :

		logging.info(f"Default Search Path: [{yaml_data['Defpath']}]\n\n")

	elif configuration_ == 'Shell File Path' :

		logging.info(f"Shell File used for Control: [{yaml_data['Batfile']}]\n\n")

	elif configuration_ == 'Search Engine Default Total Searches' :

		logging.info(f"The Return Index for Search Engine Results: [{yaml_data['Return_Index']}]\n\n")

	elif configuration_ == 'Command Failsafe Mode' :

		logging.info(f"Command-Failsafe Search Engine Mode: [{'Operational' if yaml_data['Command_Failsafe'] else 'Not Operational'}]\n\n")

	return None

def driver_main(parser : Namespace ):

	"""
	Non APIable function technically.
	Parameters: parser :  argparse.Namespace -> Namespace object similar to the arguments function in the program
	"""

	global path_

	global yaml_data

	global BOJKError

	#First check for version
	#Then check for generate
	#Then check for yaml's existence
	#Then check for config
	#Then check for command
	#Then check for search_engine

	if parser.first_action == 'version' :

		logging.info("Version and Basic Detais")

		#Definitely both files, version.txt and usage.txt should exist

		with open(OSP.join(path_ , "docs" , 'version.txt') , 'r') as file:
			data = file.read()

		cprint(data.format(**{"path_" : path_}) , 'green')
		#Using this format to print the path where it is currently present

		del data


		print('')
		logging.critical("Program Now Exits")
		exit()

	elif parser.first_action == 'usage' :

		logging.info('How to use BOJK?')

		with open(OSP.join(path_ , "docs" , 'usage.txt') , 'r') as file:
			data = file.read()

		cprint(data , 'green')

		del data

		print('')
		logging.critical("Program Now Exits" )
		exit()

	elif parser.first_action == 'gen' :

		logging.info('Generating YAML Like Configuration File' )

		yaml_file = OSP.join(getcwd() , 'config.jillian')

		yaml_file = check_all_tries_for_path(yaml_file)
		#Checks for existence of path until you get one. Defaults using
		#jillian[1].yaml, jillian[2].yaml , etc.

		from shutil import copyfile

		default_blank_yaml_file = OSP.join(path_ , "docs" , 'default.jillian')


		copyfile(default_blank_yaml_file , yaml_file)

		logging.critical(f"Standard Blank YAML like File generated by the name of {yaml_file}")

		del default_blank_yaml_file , yaml_file


		print('')
		logging.critical("Program now exits")

		exit()

	else:
		#Now Compulsorily we need a YAML file to proceed with

		if not OSP.exists(parser.yaml):
			BOJKError(f"Given YAML like Configuration FIle {parser.yaml} does not exist")

		# if parser.clean_yaml_var:
		# 	config_clean(parser.yaml)
		# 	exit()

		with open(parser.yaml , 'r') as file:
			yaml_data = yaml_load(file , Loader = CLoader)

		#For non standardized BOJK. Stupid People code in some sense

		with open(yaml_data['Batfile'] , 'w+') as file:

			file.write(compulsory_first_line)
			file.write('\n')

		if parser.first_action == 'edit' :

			import IPython

			#logging.info(f'YAML File-> parser.yaml , Data -> yaml_data. Writing of file is done by default. ')


			def config_write(data , file = parser.yaml):

				# print(data)
				# print(file)


				with open(file , 'w+') as filex :

					yaml.dump(data , filex,  Dumper = CDumper)

			mainstr_ ='\n'.join([item.strip() for item in """
			Welcome to the Brian on Jillian Kernel Editor Terminal.
			Use `data` for the data dictionary
			Use `parser.yaml` for the YAML file
			Ensure that global keyword is used for variable assignment and such.
			Take this as a multiline exec command
			Finally to Write the Configuration, use `config_write(data)`
			NOTE: The limitations of IPython make it impossible to edit it after shutting the editor. So please use `config_write(data)`  to write data into the configuration file
			""".split('\n')	] )

			data = yaml_data

			IPython.embed(header = mainstr_ ) #, local_ns  = locals() )

			logging.critical(f'Shutting the program. Hope you wrote the configuration file using ```config_write(data)```')
			exit()

		elif parser.first_action == 'init':

			initialize(parser.cache_file , yaml_data['Defpath'])

			#print('')
			logging.critical("Program now Exits")

			exit()

		elif not (parser.config_var == None):

			config_print(yaml_file = parser.yaml , configuration_ = parser.config_var)
			#cprint("Program now Exits" , 'red')
			#print('')
			logging.critical("Program now Exits")
			exit()

		else:

			dir_  = brian_driver(parser = parser)
			if not (dir_ == None):
				#Use the final_output_driver Function Here. This is not an API Function for this individual reason.
				final_output_driver(dir_ , parser.action_var , yaml_data['Batfile'] , parser.output_var )

	return None

def config_clean(yaml_file):


	"""
	Non APIable function in its technicality
	"""

	with open(yaml_file , 'r') as file:
		data_dict = yaml_load(file, Loader = CLoader)

	#If Defpath is wrong, tell user to change it and only then the program will move forward
	#Same for the directory of the batch file
	#If the Return_Index is not integerable or is negative -> Make 5
	#FailSafe and Command_Failsafe if not bool -> Change Failsafe to True and Command Failsafe to False

	#Defpath check
	if not OSP.exists(data_dict['Defpath']):

		logging.critical(f"The Defpath `{data_dict['Defpath']}` does not exist at all")
		exit()

	#Batchfile Directory Check
	bat_dir = OSP.dirname(data_dict['Batfile'])

	if not OSP.exists(bat_dir):
		logging.critical(f"The Batch File Directory `{bat_dir}` does not exist at all")
		exit()

	del bat_dir

	#Return Index
	if not ( type(data_dict['Return_Index']) == int):
		data_dict['Return_Index'] = 5

	#Command_Failsafe
	if not (type(data_dict['Command_Failsafe']) == bool):
		data_dict['Command_Failsafe'] = True


	#Check Abspaths

	for command_ , dirname in data_dict['Abspaths'].items():

		if not OSP.exists(dirname):

			#Delete the command_
			data_dict['Abspaths'].pop(command_ , None)
			#The "":"" will surely survive this due to os.getcwd() obviously existing lol

	defpath_ = data_dict['Defpath']

	for command_ , dirname in data_dict['Relpaths'].items():

		dirname = OSP.join(defpath_ , dirname)

		if not OSP.exists(dirname):

			#Delete the command_
			data_dict['Relpaths'].pop(command_ , None)

	#Now all checks are complete. We can dump the data

	with open(yaml_file , 'w+') as file:

		#Write the Dictionary Data onto the YAML File
		#Comments are discarded unfortunately

		yaml_dump(data_dict , file , Dumper = CDumper)

	return None

if __name__ == '__main__':

	##This line of code is useful for the default file to be free from the clutter of data being provided to it. It's not a part of the standard BOJK

	with open(default_file , 'w+') as filex:

		filex.write(compulsory_first_line)
		filex.write('\n')

	parser = arguments()

	use_termcolor_var = parser.color_var

	driver_main(parser)

colorama_deinit()
