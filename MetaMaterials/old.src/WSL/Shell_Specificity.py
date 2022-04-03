design_ = 'Linux Bourn Again Shell[/bin/bash]'

prog_name = 'bojk'

change_dir_command = lambda path: f'cd  "{path}"'
start_dir_command = lambda path : f'xdg-open "{path}"'
pushd_dir_command = lambda path: f'pushd "{path}"'


default_file = '/mnt/d/Toolkit/Extra/Brian/MetaMaterials/src/WSL/wslbrian.sh'

compulsory_first_line = '#!/bin/bash'