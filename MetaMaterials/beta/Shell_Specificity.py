CaseSensitive = False ##Windows is Generally not Case Sensitive


pushd_Function = lambda path : f'pushd "{path}"'
cd_Function = lambda path : f'cd /d "{path}"'
open_Function = lambda path : f'start "" "{path}"'

ProgramName = 'bojk'
Description = """Brian on Jillian Kernel[BOJK] is a master directory change program based on a highly complex set of commands inspired from 'roscd' command. Check
arguments for usage. Current BOJK is designed for Windows Command Prompt[cmd.exe]"""

shell_name = 'Windows Command Prompt [cmd.exe]'

FirstLine = '@echo off'

def Default_Function(path , ShellFile):

	import os

	with open(ShellFile , 'w+') as filehandle:
		filehandle.write(f'{FirstLine}\n{pushd_Function(os.path.abspath(path))}')

	return None

import os
ProgPath = os.path.dirname(os.path.abspath(__file__))
