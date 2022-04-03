design_ = 'Windows Command Prompt[cmd.exe]'

prog_name = 'bojk'

change_dir_command = lambda path: f'cd /d "{path}"'
start_dir_command = lambda path : f'start "" "{path}"'
pushd_dir_command = lambda path: f'pushd "{path}"'


default_file = 'D:\\Toolkit\\Custom\\lbrian.cmd'

compulsory_first_line = '@echo off'
