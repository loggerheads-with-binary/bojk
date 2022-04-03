from argparse import ArgumentParser as ArgumentParser_src, Namespace
import os, sys
import Shell_Specificity as cfg
import logging
import subprocess
import termcolor
import colorama
from rapidfuzz import fuzz

colorama.init(autoreset = True)

DefaultConfigChoices = {'ctrl' , 'relpaths' , 'abspaths' , 'return-index' , 'defpath' , 'shell-file' , 'codes'}		##Default Config Choices
data = None 																										##Data --> Everything
COLORMODE = False	 																								##Should color be used [off by default from v3]
REALPATH = False 																									##Should Realpath be used

RETURN_CODES = {
					'shell-success' : 0 ,
					'no-shell-success' : 0x1000 ,
					'non-brian-standard' : 0xff00 ,
					'help' : 0xf000 ,
					'argument-error' : 0x1f00 ,
					'other-error' : 0xffff ,
					'failed-brian' : 0x1fff ,
}																												##Defined in the Brian Protocol

class ArgumentParser(ArgumentParser_src):

	def exit(self , status  = 2 , message = ""):
		sys.stderr.write(message)
		sys.exit(status)

	def error(self, message):

		#self.print_help(sys.stderr)
		self.exit(RETURN_CODES['argument-error'], '%s: error: %s\n' % (self.prog, message))
		#sys.exit(2)

	def print_help(self , buffer = sys.stdout):


		buffer.write(self.description)
		buffer.write('\n\n')

		with open(os.path.join(cfg.ProgPath , 'docs' , 'help.txt') , 'r') as filehandle:

			buffer.write(filehandle.read())

		buffer.write('\n')
		buffer.write(self.epilog)

		RepresentationMake = lambda key , val : f'{"".join([item.capitalize() for item in key.split("-")] ) }::{hex(val)}'
		TABCHAR = '\n\t\t'

		buffer.write(f'\n\nSome Defaults:\n\tReturn Codes: {TABCHAR}{TABCHAR.join([RepresentationMake(*item) for item in RETURN_CODES.items()])}\n\n\tProgram Location: `{cfg.ProgPath}`\n\tScript Location: `{os.path.abspath(__file__)}`\n\tShell Configuration Location: `{os.path.abspath(cfg.__file__)}`\n\tShell Designed for: `{cfg.shell_name}`\n\tCase-Sensitivity: {"ON" if cfg.CaseSensitive else "OFF"} \n\tColorful Output: {"ENABLED" if COLORMODE else "DISABLED"} \n\tChoices to check program configuration: {DefaultConfigChoices}.\n\tFast Mode Chaeyoung Translate Location: `{subprocess.Popen(["which" , "c-trans"], stdout = subprocess.PIPE).communicate()[0].decode("utf8").strip()}`')
		buffer.write('\n')

	def parse_args(self , args : list = None):

		if args == None :
			args = sys.argv[1:]

		if ('-h' in args) or ('--help' in args):
			self.print_help(sys.stdout)
			self.exit(RETURN_CODES['help'])

		return super().parse_args(args)

def Chaeyoungize(TranslablePath):

	proc = subprocess.Popen(['c-trans' , TranslablePath] , stdout = subprocess.PIPE)
	out = proc.communicate()[0].decode('utf8')

	if proc.returncode!= 0 :

		logging.debug(f'Chaeyoungize::({TranslablePath}) failed')
		raise ValueError('Chaeyoung Translate Unsuccessful')

	logging.debug(f'Chaeyoungize::({TranslablePath})-->({out})')

	return out

def ReadConfig(datafile ):

	global data

	if data!= None :

		logging.debug(f'ReadConfig() skipping since BOJK::data is already non empty')
		return None

	else:

		import yaml

		with open(datafile, 'r') as filehandle:

			data = yaml.load(filehandle, Loader = yaml.CLoader)

		logging.debug(f'ReadConfig(@[{datafile}])--> global data')

	return None

def WriteConfig(datafile):

	global data

	assert data != None , \
	f'Cannot Write empty data into a configuration file'

	assert isinstance(data , dict), \
	f'Need a dictionary type variable to be editing the configuration for'

	logging.debug(f'WriteConfig::DataCheck() complete; all checks successful')

	import yaml

	with open(datafile, 'w+' , encoding = 'utf8') as filehandle:

		yaml.dump(data , filehandle , Dumper = yaml.CDumper)
		logging.debug(f'Data-->BOJK::WriteConfig(@[{datafile}])')

	return True

def filtration(options : Namespace):

	if options.config != None:
		options.action = 'config'

	else:
		delattr(options, 'config')

	if options.touch != None:

		if options.touch == True :
			options.datafile = os.path.abspath(options.datafile)

		options.datafile = os.path.abspath(options.touch)
		options.action = 'touch'

	delattr(options, 'touch')

	global REALPATH
	REALPATH = options.realpath_mode
	delattr(options, 'realpath_mode' )

	return options

def cprint(msg , color = 'yellow' , **kwargs):

	global COLORMODE

	(termcolor.cprint(msg , color = color , **kwargs)) if (COLORMODE) else (print(msg , **kwargs ))

def Finalize(path , batfile : str , mode : str ,  chaeyoung_translate : bool  = False):
	#c-mode = True --> Chaeyoungize

	global REALPATH
	import sys

	logging.debug('DriverMain() complete, executing BOJK::Finalize()')

	path = (Chaeyoungize(path)) if (chaeyoung_translate) else (path)
	path = (os.path.realpath(path)) if REALPATH else (os.path.abspath(path))

	if mode == None :

		batfile = os.path.abspath(Chaeyoungize(batfile))
		cfg.Default_Function(path , batfile)
		sys.exit(RETURN_CODES['shell-success'])
		#return None


	elif mode.startswith('\t'):

		import sys

		if mode == '\tquinn':

			#cprint('Quinn Server Output: ' , color = 'red' , end = '')

			import Quinn.Client as qc
			qc.Call(op = 'set' , key = 'bojk', data = path , force = 1 )

			logging.debug(f'Finalize()-->Quinn-->Quinn.Server: Path has been transmitted to the Quinn Server at `bojk` variable')
			sys.exit(RETURN_CODES['no-shell-success'])

		elif mode == '\tcopy':
			import pyperclip

			pyperclip.copy(path)
			logging.debug('Finalize()-->system::clipboard(): Path has been copied to the clipboard')
			#sys.exit(100)
			sys.exit(RETURN_CODES['no-shell-success'])

		elif mode == '\tprint':

			logging.debug('Finalize()-->sys.stdout : Path has been written in plaintext on the terminal')
			sys.stdout.write(path)
			#sys.exit(100)
			sys.exit(RETURN_CODES['no-shell-success'])

		elif mode == '\tstderr':

			logging.debug('Finalize()-->sys.stderr : Path has been written on stderr, god knows why you would want that????')
			sys.stderr.write(path)
			#sys.exit(100)
			sys.exit(RETURN_CODES['no-shell-success'])

		return None

	batfile = os.path.abspath(Chaeyoungize(batfile))

	with open(batfile , 'w+' , encoding = 'utf8') as filehandle:

		filehandle.write(f'{cfg.FirstLine}\n')

		if mode == 's' :
			filehandle.write(cfg.cd_Function(path))

		elif mode == 'o' :
			filehandle.write(cfg.open_Function(path))

		elif mode == 'p':
			filehandle.write(cfg.pushd_Function(path))

		elif mode == 'po':
			filehandle.write(f'{cfg.pushd_Function(path)}\n{cfg.open_Function(path)}')

		elif mode == 'so':
			filehandle.write(f'{cfg.cd_Function(path)}\n{cfg.open_Function(path)}')

		logging.debug(f'Final Path: [{path}]')
		logging.debug(f'Finalize() completed --> Edited @[{batfile}]')

		return (RETURN_CODES['shell-success'])

	return None

def _Inspect_Config_Backend(data_dict : dict , raise_error : bool = True):

	import re

	ChaeyoungSyntax = re.compile(r'\{.+\}.*')
	if raise_error:

		def Activity(msg , ErrorClass= Exception):

			raise ErrorClass(msg)

	else:

		def Activity(msg , ErrorClass = Exception):

			logging.critical(f'{msg}\t[{ErrorClass}]')


	DefiniteKeys = ['Defpath' , 'Relpaths' , 'Abspaths' , 'Return_Index' , 'Command_Failsafe' , 'Batfile' , 'Cache']

	ErrorKeys = [key for key in DefiniteKeys if key not in data_dict ]

	if len(ErrorKeys) > 0 :

		raise KeyError(f'The keys {ErrorKeys} are not present inside the configuration')

	else:
		logging.debug(f'Configuration contains all keys')

	##Defpath

	for key in ['Defpath' , 'Batfile' , 'Cache'] :

		if not ChaeyoungSyntax.fullmatch(data_dict[key]):

			Activity(f'The `{key}` variable is configured incorrectly and does not follow Chaeyoung Strategy')


	##Cleaning Portion
	data_dict['Abspaths'] = {str(key).lower() : str(value) for key, value in data_dict['Abspaths'].items()}
	data_dict['Relpaths'] = {str(key).lower() : str(value) for key, value in data_dict['Relpaths'].items()}

	##Check Abspath syntax:
	error_abspaths = [key for key, value in data_dict['Abspaths'].items() if not ChaeyoungSyntax.fullmatch(value) ]


	GoddamnKeys = set(data_dict['Abspaths'].keys()).intersection(set(data_dict['Relpaths'].keys()))

	if len(GoddamnKeys) > 0 :
		Activity(f'The following keys are used in both `relpaths` and `abspaths`: {GoddamnKeys}. \nThis can confuse the parsers and will give priority to `abspaths`, thus rendering `relpaths` keys useless',
				KeyError)

	else:

		logging.debug(f'All `relpaths` and `abspaths` keys are unique')


	if len(error_abspaths) == 0 :

		logging.debug('All Abspaths are configured correctly')

	else:

		Activity(f'The values of the following keys in `abspaths` do not follow Chaeyoung Syntax: {error_abspaths}' , SyntaxError)

	data_dict['Return_Index'] = int(data_dict['Return_Index'])

	logging.debug('Note all instructions have been provided. Please check the file and make approrpriate changes. Then inspect once again')

	if data_dict['Command_Failsafe'] != False:
		data_dict['Command_Failsafe'] = True

	return data_dict

def _Inspect_Config(datafile, rectification: bool = False , raise_error : bool = True):

	import re, yaml

	with open(datafile , 'r' ) as filehandle:

		data_dict = yaml.load(filehandle , Loader = yaml.CLoader)

	##Now Check for the conditions

	data_dict =  _Inspect_Config_Backend(data_dict , raise_error = raise_error)

	if rectification:

		with open(datafile , 'w+' , encoding = 'utf8') as filehandle:

			yaml.dump(data_dict , filehandle, Dumper = yaml.CDumper)

	return None

def SearchEngineShow(Config : list , Defpath :str , Query : str , sbf : bool = False):

	global COLORMODE

	print('\n')
	Return_Index = len(Config)
	Moder = {'Defpath Searched' : Defpath , 'Total Directories Indexed' : Return_Index , 'Query Provided' : Query , 'Searching By file' : sbf}
	Adjuster = len(max(Moder.keys() , key = lambda x : len(x) )) + 2

	for key , value in Moder.items():

		cprint(key, 'green' , end= '')
		print(' : ' , end= '')
		cprint(value , 'yellow')

	from prettytable import PrettyTable
	x=PrettyTable()
	print('\n')

	if COLORMODE:

		if sbf:
			x.field_names = [	colorama.Fore.MAGENTA + 'Sr' ,
								colorama.Fore.GREEN + 'RelPath' ,
								colorama.Fore.CYAN + 'FileRelPath' ,
								colorama.fore.YELLOW +  'Accuracy']


		else:
			x.field_names = [	colorama.Fore.MAGENTA + 'Sr' ,
								colorama.Fore.GREEN  + 'Relpath' ,
								colorama.Fore.YELLOW +  'Accuracy']

		r= (		colorama.Fore.RED , ## Odd Indices 1, 3 , 5 , etc
					colorama.Fore.CYAN	##Even Indices, 2 , 4 , 6 etc)
			)
		#x.add_row([[ f'{r[index&1]}{item}' for item in ((index) , *piece)  ]	for index , piece in enumerate(Config , 1)])

		for index , piece in enumerate(Config , 1):
			x.add_row([f'{r[index&1]}{item}' for item in (index , *piece)])


	else:

		if sbf:
			x.field_names = ['Sr' , 'RelPath' , 'FileRelPath' , 'Accuracy']


		else:
			x.field_names = ['Sr' , 'Relpath' , 'Accuracy']

		[x.add_row([index, *item]) for index, item in enumerate(Config , 1)]

	print(x)

	cprint('Choose the index of the folder of choice : ' , 'red' , end = '')
	Answer = int(input())
	print()
	if Answer not in range(1,Return_Index+1):
		logging.error(f'BOJK::Jillian::Show() got an unexpected choice of {Answer}. Only values from 1 to {Return_Index+1} are allowed')

		return None

	return Config[Answer-1][0]

##Assumes query is small already, path smallens; case insensitive
def fastdns(query : str , path : str):

	"""
	APIable Function: Returns a score in [0,100]  based on the three Fuzzy String Algorithms:
	partial_ratio
	token_set_ratio
	token_sort_ratio

	Note: This is a fast application with no checks on datatypes, case and such
	It assumes query is lowercase, and lowers the case of path
	Remember to use this tool wisely
	"""


	path = path.lower()

	#logging.debug(f'FASTDNS::(query = {query}, path = {path})')

	partial_ = fuzz.partial_ratio( query , path)
	set__ = fuzz.token_set_ratio(query , path)
	sort__ = fuzz.token_sort_ratio(query , path)


	return (partial_ + set__ + sort__ )/3

##Case sensitive fastdns
def normaldns(query : str , path : str):

	"""
	Like FastDNS but case sensitive
	"""
	#logging.debug(f'NORMALDNS::(query = {query}, path = {path})')


	partial_ = fuzz.partial_ratio( query , path)
	set__ = fuzz.token_set_ratio(query , path)
	sort__ = fuzz.token_sort_ratio(query , path)


	return (partial_ + set__ + sort__ )/3

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

def GetConfirmation(prompt , alias , path):

	answer = 'k'

	while answer not in ['y' , 'n']:

		print(prompt  , end = '')
		cprint(f' {alias}' , 'green' , end = '')
		print(' i.e. ' , end = '')
		cprint(path, 'red' , end = '')
		cprint(f' [y/n]: ' , 'yellow' , end = '')
		answer = input().strip().lower()

	return answer == 'y'

def StandardConfirmation(prompt):

	answer = 'k'

	while answer not in ['y' , 'n']:
		print(prompt , end = '')
		cprint(f' [y/n]: ' , 'yellow' , end = '')
		answer = input().strip().lower()

	return answer == 'y'

relpath = lambda path  , start : os.path.relpath(path , start).replace('\\' , '/')
standardize_path = lambda path : path.replace('\\' , '/')

def DriverMain(options : Namespace):

	global data

	if options.action == 'brian':

		ReadConfig(options.datafile)

		if options.command != None :

			if options.command in data['Abspaths']:

				Finalize(data['Abspaths'][options.command] , data['Batfile'] , options.brian_action , chaeyoung_translate = True)
				return RETURN_CODES['shell-success']

			elif options.command in data['Relpaths']:

				Finalize(f"{data['Defpath']}/{data['Relpaths'][options.command]}" , data['Batfile'] , options.brian_action , chaeyoung_translate = True)
				return RETURN_CODES['shell-success']

			elif data['Command_Failsafe']:

				abspaths_typex = max([ ( fastdns(alias , options.command ) , alias) for alias in data['Abspaths'].keys()] , key = lambda x : x[0])
				relpaths_typex = max([ ( fastdns(alias , options.command ) , alias) for alias in data['Relpaths'].keys()] , key = lambda x : x[0])

				RelpathFinal = Chaeyoungize(f'{data["Defpath"]}/{data["Relpaths"][relpaths_typex[-1]]}')
				AbspathFinal = Chaeyoungize(data["Abspaths"][abspaths_typex[-1]])

				print()
				if relpaths_typex[0] > abspaths_typex[0]:

					if GetConfirmation(f'Did you mean', relpaths_typex[-1], RelpathFinal):

						Finalize(RelpathFinal , data['Batfile'] , options.brian_action , chaeyoung_translate = False)
						return RETURN_CODES['shell-success']

					elif GetConfirmation('Else did you mean', abspaths_typex[-1] ,AbspathFinal):
						Finalize(AbspathFinal , data['Batfile'] , options.brian_action , chaeyoung_translate = False)
						return RETURN_CODES['shell-success']

					else:

						cprint('\n😭😥Sorry The Internal Search Engine was useless😭😥\n' , 'red')
						logging.error(f'alias `{options.command}` not found in the configuration @[{options.datafile}]')
						return RETURN_CODES['failed-brian']

				else:
					if GetConfirmation('Did you mean' ,  abspaths_typex[-1] , AbspathFinal ):
						Finalize(AbspathFinal , data['Batfile'] , options.brian_action , chaeyoung_translate = False)
						return RETURN_CODES['shell-success']

					elif GetConfirmation('Else did you mean', relpaths_typex[-1] , RelpathFinal):

						Finalize(RelpathFinal , data['Batfile'] , options.brian_action , chaeyoung_translate = False)
						return RETURN_CODES['shell-success']


					else:

						cprint('\n\n😭😥Sorry The Internal Search Engine was useless😭😥\n' , 'red')
						logging.error(f'alias `{options.command}` alias not found in the configuration @[{options.datafile}]')
						return RETURN_CODES['failed-brian']

			else:

				logging.error(f'{options.command} alias not found in the configuration @[{options.datafile}]')
				return RETURN_CODES['failed-brian']

		elif options.search != None :

			import heapq,scandir
			Defpath = Chaeyoungize(data['Defpath'])

			"""
			x.field_names = ['Sr' , 'RelPath' , 'FileRelPath' , 'Accuracy']

			else:
				x.field_names = ['Sr' , 'Relpath' , 'Accuracy']
			"""

			dns_function = normaldns if options.case_sensitivity else fastdns

			if not options.case_sensitivity:
				logging.debug('FASTDNS::Case Insensitive Search')
				options.search = options.search.lower()

			else:
				logging.debug('NORMALDNS::Case Sensitive Search')
			if options.search_mode == 'walk':
				##Default
				logging.debug(f'Using Walk Search Mode')

				if options.fps :

					SearchBase = heapq.nlargest(data['Return_Index'] ,

												[(path , dns_function(options.search , relpath(path , Defpath)))
												for path, _ , _ in scandir.walk(Defpath, followlinks = True) ],
												key = lambda x : x[-1])

				else:

					SearchBase = heapq.nlargest(data["Return_Index"] ,

												[(path,dns_function(options.search , os.path.split(path)[-1]))
												for path , _ , _ in scandir.walk(Defpath, followlinks = True)] ,

												key = lambda x : x[-1])

				SearchBase = [(relpath(path , Defpath) , val) for path , val in SearchBase]

			elif options.search_mode == 'sbf':
				##Remember cannot use cache
				logging.debug(f'Using SBF Search Mode')

				SearchBase = list()

				if options.fps:

					for directory , _ , files in scandir.walk(Defpath  , followlinks = True):

						directory = relpath(directory, Defpath)

						SearchBase.extend([(directory , file , dns_function(options.search, os.path.join( directory, file)) )
											for file in files ])

				else:

					for directory , _ , files in scandir.walk(Defpath , followlinks = True):
						SearchBase.extend([(directory , file , dns_function(options.search , file)) for file in files])

				Searchbase = heapq.nlargest(data['Return_Index'] , SearchBase , key = lambda x : x[-1])
				SearchBase = [	(relpath(directory, Defpath) , file , val  )
								for directory , file , val in SearchBase]

			elif options.search_mode == 'cache':

				logging.debug(f'using Cache Search Mode')
				##Use Cache

				if options.cache == None :
					options.cache = Chaeyougize(data['Cache'])

				import _pickle as pickle

				with open(options.cache , 'rb') as filehandle:

					CachedPaths = pickle.load(filehandle)


				if options.fps:

					SearchBase = heapq.nlargest(data['Return_Index'] ,
												[(path , dns_function( options.search , standardize_path(path)  )) for path in CachedPaths] ,
												key = lambda x : x[-1])

				else:

					SearchBase = heapq.nlargest(data['Return_Index'] ,
												[(path , dns_function(options.search  , os.path.split(path)[-1]  )) for path in CachedPaths] ,
												key = lambda x : x[-1])

			path = SearchEngineShow(SearchBase, Defpath , options.search , options.search_mode == 'sbf')
			del SearchBase

			if path == None :
				logging.warning(f'No Path Chosen. Shutting Down')
				return RETURN_CODES['no-shell-success']

			logging.debug(f'Jillian::Search() complete')
			Finalize(os.path.join(Defpath , path ) , data['Batfile'] , options.brian_action , False)
			return RETURN_CODES['shell-success']

		else:

			logging.error(f'At least choose some option you son of a bitch')
			return RETURN_CODES['failed-brian']

	elif options.action in ['version' , 'usage' ]:

		logging.debug(f'Printing {options.action} information')

		with open(os.path.join(cfg.ProgPath , 'docs' , f'{options.action}.txt') , 'r') as filehandle:

			cprint(filehandle.read() , ('magenta') if (options.action == 'version') else 'green')
			return RETURN_CODES['non-brian-standard']

	elif options.action == 'init-cache' :

		##Defpath, cache needed
		ReadConfig(options.datafile)

		Defpath = Chaeyoungize(data['Defpath'])
		Cache = (options.cache) if (options.cache != None ) else (Chaeyoungize(data['Cache']))

		import scandir

		with open(Cache , 'wb') as filehandle:

			AllPaths = [ relpath(dirname , Defpath).replace('\\' , '/') for dirname , _ , _ in scandir.walk(Defpath , followlinks = True) ]
			logging.debug('All Paths Loaded')

			import _pickle as pickle

			pickle.dump(AllPaths, filehandle)
			logging.debug('All necessary filepaths cached')


			print(f'File cache Initialized. Total of ' , end = '' )
			cprint(f'{len(AllPaths)}' , color = 'yellow' , end = '')
			cprint(' directories within ' , end = '')
			cprint(f'{Defpath}' , color = 'green' , end= '')
			cprint(' indexed' )

		logging.info(f'Cache Initialized @[{Cache}]')
		return RETURN_CODES['non-brian-standard']

	elif options.action == 'touch' :

		import shutil
		shutil.copy(src = os.path.join(cfg.ProgPath , 'docs' , 'default.jillian') , dst = options.datafile)
		logging.info(f'Created a sample config file @[{options.datafile}]')
		return RETURN_CODES['non-brian-standard']

	elif options.action == 'edit' :

		ReadConfig(options.datafile)

		import IPython

		header = f"""{colorama.Fore.CYAN if COLORMODE else ""}BOJKonCB Edit Functionality. Add as per known. {colorama.Fore.RED if COLORMODE else ""}Here's a set of useful variables to edit {colorama.Fore.RESET if COLORMODE else ""}\n\n"""
		header+= (colorama.Fore.YELLOW if COLORMODE else "") + "  ".join([f"data['{key}']" for key in data.keys() ] ) + colorama.Fore.RESET
		header+= "\n"

		IPython.embed(	header = header ,
						user_ns = globals(),
						colors="neutral" ,
						exit_msg = f'\n{colorama.Fore.YELLOW if COLORMODE else ""}Thank you for using the Brian on Jillian Kernel v4.0 on Chaeyoung Backend' )


		##data to be written

		if StandardConfirmation(f'Do you wish to edit the {colorama.Fore.RED if COLORMODE else ""}`{options.datafile}`{colorama.Fore.RESET} configuration file with the provided changes?'):
			WriteConfig(options.datafile)
			return RETURN_CODES['non-brian-standard']

		return RETURN_CODES['other-error']

	elif options.action == 'config' :

		ReadConfig(options.datafile)
		Config_Show(options.config, options.datafile)

		return RETURN_CODES['non-brian-standard']

	elif options.action in ['inspect' , 'rectify' ]:

		_Inspect_Config(options.datafile , options.action == 'rectify')

		return RETURN_CODES['non-brian-standard']

def Config_Show(config_type :str = True , datafile : str = 'config.jillian'):

	#DefaultConfigChoices = {'ctrl' , 'relpaths' , 'abspaths' , 'return-index' , 'defpath' , 'shell-file'}
	global data

	if config_type == True:

		Config_Show('abspaths')
		Config_Show('relpaths')
		return None

	if config_type == 'codes':
		cprint('Return Codes:\n' , color = 'green')

		RETURN_CODES_tmp = {"".join([item.capitalize() for item in key.split('-')]) : value for key, value in RETURN_CODES.items()}
		Adjuster = len(max(RETURN_CODES_tmp.keys() , key = lambda x : len(x)))

		for key, value in RETURN_CODES_tmp.items():
			cprint(f'{key.rjust(Adjuster)} : ' ,  end = '' , color = 'cyan')
			cprint(hex(value) , color = 'yellow')

	if config_type == 'return-index' :

		cprint('Return-Index : ' , color = None, end = '' )
		cprint(data['Return_Index'] , color = 'yellow' )

	if config_type == 'ctrl' :

		Moder = {	'[file]   Configuration File' : datafile ,
					'[cfg]    Shell Configuration File' : cfg.__file__ ,
					'[shell]  Shell Configuration' : cfg.shell_name ,
					'[search] Defpath' :  data['Defpath'],
					'[count]  Return Index' : data['Return_Index'],
					'[file]   Shell File' : data['Batfile'],
					'[file]   Cache File' : data['Cache'],
					'[bool]   Command Search Failsafe' : data['Command_Failsafe'], }

		Adjuster = len(max(Moder.keys(), key = lambda x : len(x))) - 9	##max of search

		for key_tmp , value in Moder.items():

			typex = key_tmp[ : key_tmp.find(']') + 1  ]
			key = key_tmp[key_tmp.find(']') + 1 : ].lstrip()

			cprint(typex.ljust(8), color = 'cyan' , end= '')
			cprint(key.rjust(Adjuster) , color =  'green' , end = '')
			cprint(': ' , color = None, end = '')
			cprint(value , color = 'yellow' , end = '\n')

	if config_type == 'defpath':

		cprint('Defpath[Search]' , color = None , end = '' )
		cprint(data['Defpath'] , color = 'yellow' )

	if config_type == 'shell-file':
		cprint('Shell File[file]', color = None , end = '' )
		cprint(data['Batfile'] , color = 'yellow' , end = '\n')


	if config_type in ['relpaths' , 'abspaths']:

		config_type  = config_type.capitalize()

		im_data = data[config_type]

		cprint(f'Here is a list of {config_type} in the configuration file')
		cprint(f'Note: Defpath : {Chaeyoungize(data["Defpath"])}\n')

		global COLORMODE

		import prettytable

		global x
		x = prettytable.PrettyTable()

		if COLORMODE:
			r = ((colorama.Fore.CYAN) if (COLORMODE) else ('') ,  (colorama.Fore.YELLOW) if (COLORMODE) else (''))
			x.field_names = [colorama.Fore.CYAN + 'Alias' , colorama.Fore.YELLOW + 'Path']
			#x.sortby = colorama.Fore.CYAN + 'Alias'
			[x.add_row(( r[index&1] + key , r[index&1] + value.strip('/').strip('\\') ) ) for index, (key , value) in enumerate(data[config_type].items())]
			x.align[colorama.Fore.CYAN + 'Alias' ] = 'r'
			x.align[colorama.Fore.YELLOW + 'Path'] = 'l'

		else:
			x.field_names = ['Alias' , 'Path']
			#x.sortby = 'Alias'
			#x.add_rows([(  key , value.strip('/').strip('\\') ) for key , value in data[config_type].items()])
			[x.add_row(( key , value.strip('/').strip('\\') ) ) for index, (key , value) in enumerate(data[config_type].items())]
			x.align['Alias'] = 'r'
			x.align['Path'] = 'l'

		x.set_style = 'MARKDOWN'
		print(x)

def arguments(args: list = None):

	parser = ArgumentParser(prog = cfg.ProgramName , description = 'Brian on Jillian Kernel on Chaeyoung Backend v 4.1' , epilog = cfg.Description)

	P1 = parser.add_mutually_exclusive_group()

	P1.add_argument('-c' , '--command' ,
					dest = 'command' , default = None , type = lambda x : x.lower() , metavar = '{command}' ,
					help = 'Use a command from the Configuration file.')

	P1.add_argument('-s' , '--search' , '--search-engine' , '--search-facility' ,
					dest = 'search' , default = None , metavar = '{Search Term}' , type = standardize_path ,
					help = 'Search for this directory in the defpath')

	P1.add_argument('-v' , '-V' , '--version' ,
					dest = 'action' , action = 'store_const' , const = 'version'  , default = 'brian' ,
					help = 'Show details about version of BOJKonCB')

	P1.add_argument('-u' , '-U' , '--usage',
					dest = 'action' , action = 'store_const' , const = 'usage' , default = 'brian' ,
					help = 'Show usage of BOJKonCB')

	P1.add_argument('-g' , '--generate' , '--touch' , '--create' ,
					dest = 'touch' , default = None , action = 'store' , metavar = '{Optional File}' , nargs = '?' , const = 'config.jillian' , type = os.path.abspath ,
					help = 'Generates a blank new configuration file. If no path given, defaults to config.jillian')

	P1.add_argument('-i' , '--init-cache' ,
					dest = 'action' , action = 'store_const' , const = 'init-cache' , default = 'brian' ,
					help = 'Initialize the BOJKonCB Cache feature which can be used later')

	P1.add_argument('-f' , '--config' , '--ls' , '--list' ,
					dest = 'config' , choices = DefaultConfigChoices , metavar = '..' , default = None ,  const = True , nargs = '?' ,
					help = 'Show configuration data. Choices : {}'.format(DefaultConfigChoices) )

	P2 = parser.add_mutually_exclusive_group()

	P2.add_argument('-o' , '--open' ,
					dest = 'brian_action' , action = 'store_const' , const = 'o' , default = None ,
					help = 'Open directory in file explorer only')

	P2.add_argument('--so' , '--shell-and-open' ,
					dest = 'brian_action' , action = 'store_const' , const = 'so' , default = None ,
					help = 'Open in the shell as well as the file explorer')

	P2.add_argument('-S' , '--shell' ,
					dest = 'brian_action' , action = 'store_const' , const = 's' , default = None ,
					help = 'Change directory in the shell')

	P2.add_argument('-C' , '--copy' ,
					dest = 'brian_action' , action = 'store_const' , const = '\tcopy' , default = None ,
					help = 'Copy the final path onto the clipboard')

	P2.add_argument('-P' , '--print' ,
					dest = 'brian_action' , action = 'store_const' , const ='\tprint' , default = None ,
					help = 'Print the final path onto the terminal')

	P2.add_argument('--perr' , '--print-on-error' ,
					dest = 'brian_action' , action = 'store_const' , const = '\tstderr' , default = None ,
					help = 'Print the final path on stderr instead of stdout'
					)

	P2.add_argument('-q' , '--quinn' , '--Quinn' ,
					dest = 'brian_action' , action = 'store_const' , const = '\tquinn' , default = None ,
					help = 'Push the final directory onto the `bojk` reserved variable on the Quinn Server')

	P2.add_argument('-p' , '--pushd' ,
					dest = 'brian_action' , action = 'store_const' , const = 'p' , default = None ,
					help = ' Push the directory on the shell stack, i.e. the `pushd` command')

	P2.add_argument('--po' , '--pushd-and-open' ,
					dest = 'brian_action' , action = 'store_const' , const ='po' , default = None ,
					help = 'Push the directory and open it in the explorer.')

	parser.add_argument('-r' , '-r' , '--realpath', '--real', '--Realpath' , '--real-path' , '--resolve' , '--resolve-path' ,
						dest = 'realpath_mode' , action = 'store_true' ,
						help = 'Opens Real Directory(realpath/assesses symlinks) instead of link directory' )

	P1.add_argument('-E' , '--edit' , '-e' ,
					dest = 'action' , action = 'store_const' , const = 'edit' , default = 'brian' ,
					help = 'BETA functionality: Edit the configuration. Uses ipython backend')


	parser.add_argument('--sbf' , '--search-by-file' ,
					dest = 'search_mode' , default = 'walk' , action = 'store_const' , const = 'sbf' ,
					help = 'Searches the directory based on the files inside it. NOTE CACHE FEATURE CANNOT BE USED FOR THIS MODE')

	parser.add_argument('--uc' , '--use-cache' ,
					dest = 'search_mode' , default = 'walk' , action = 'store_const' , const = 'cache' ,
					help = 'Use Cache Instead of Walking the Folders in Realtime for the Search Engine Functionality')

	parser.add_argument('--tc' , '--term-color' ,
						dest = 'termcolor_var' , action = 'store_true' ,
						help = 'If flagged, the terminal prints a very colorful text. Sets to OFF by default')

	parser.add_argument('--fps' , '--full-path-search' ,
						dest = 'fps' , action = 'store_true' ,
						help = 'Forces the search engine to search for the entire path. Defaults to only directory name')

	parser.add_argument('-d' , '-y' , '--yaml' , '--cfg' , '--data' , '--datafile' , '--data-file' ,
						dest = 'datafile' , action = 'store' , default = 'config.jillian'  , type = os.path.abspath ,
						help = 'Configuration python file with .jillian extension. No defaults for this.')

	parser.add_argument('--inspect' , '--investigate' ,
						dest = 'action' , action = 'store_const' , default = 'brian' , const = 'inspect' ,
						help = 'Inspects the configuration file for any imperfections')

	parser.add_argument('--rectify' , '--correct-datafile' ,
						dest = 'action' , action = 'store_const' , default = 'brian' , const = 'rectify' ,
						help = 'Rectifies a configuration file as far as possible by the program')

	parser.add_argument('--debug' , '--debug-mode' ,
						dest = 'log_mode' , action = 'store_const' , const = 'debug' , default = 'info' ,
						help = 'Sets the logging level to `DEBUG` instead of `INFO`')

	parser.add_argument('--cache-file' , '--cache' , '--non-default-cache' ,
						dest = 'cache' , action = 'store' , default = None , ##Note: This cache can be overwritten. Otherwise default from the file will be used
						type = os.path.abspath ,
						help = ' Cache File to be used for BOJKonCB. Default to `Directories.bojk`in the docs folder within the program folder')

	P4 = parser.add_mutually_exclusive_group()

	P4.add_argument('--case-sensitive' , '--CS' ,
						dest = 'case_sensitivity' , action = 'store_const' , default = cfg.CaseSensitive , const = True ,
						help = f'Enable Case Sensitivity of Searches. {"ENABLED" if cfg.CaseSensitive else "DISABLED"} by default' )

	P4.add_argument('--CI' , '--case-insensitive' ,
						dest   = 'case_sensitivity' , action = 'store_const' , default = cfg.CaseSensitive , const =False ,
						help = f'Disable Case Sensitivity of Searches. {"DISABLED" if cfg.CaseSensitive else "ENABLED"} by default')

	if args == None :

		return parser.parse_args()

	return parser.parse_args(args)

if __name__ == '__main__':

	import pretty_traceback

	pretty_traceback.install()

	options = filtration(arguments())

	COLORMODE = options.termcolor_var

	if COLORMODE:
		import coloredlogs
		coloredlogs.install(fmt = '%(asctime)s %(levelname)s : BOJK::%(message)s' , level = options.log_mode)

	else :
		logging.basicConfig()
		logging = logging.getLogger('BOJK:')
		logging.setLevel(level = 10 if (options.log_mode.lower() == 'debug')  else 20)

	logging.debug(f'Setup::Engine::Initialize() Complete; switching to BOJK::DriverMain()')

	status = DriverMain(options)

	if status == None:
		logging.debug(f'DriverMain() returning non-integer Nonetype value')
		sys.exit(RETURN_CODES['other-error'])

	sys.exit(status)

colorama.deinit()
