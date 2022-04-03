CaseSensitive = True ##UNIX is Generally  Case Sensitive

pushd_Function = lambda path : f'pushd "{path}"'
cd_Function = lambda path : f'cd "{path}"'
open_Function = lambda path : f'xdg-open "{path}"'

ProgramName = 'bojk'
Description = """Brian on Jillian Kernel[BOJK] is a master directory change program based on a highly complex set of commands inspired from 'roscd' command. Check
arguments for usage. Current BOJK is designed for The Bourne Again Shell on *nix systems[/usr/bin/bash]"""

shell_name = '*nix Bourne Again Shell [/usr/bin/bash]'

FirstLine = '#!/bin/bash'

def Default_Function(path , ShellFile):

	import os

	with open(ShellFile , 'w+') as filehandle:
		filehandle.write(f'{FirstLine}\n{pushd_Function(os.path.abspath(path))}')

	return None

import os
ProgPath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)) , '..' ) )
