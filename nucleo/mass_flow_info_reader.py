import json
import os

from .globals.paths import root
from .globals.paths import units_info_folder, units_arduino_info_folder, units_lcr_info_folder

def get_logfile_info(unit_folder):
    os.chdir(unit_folder)
    files = os.listdir('.')
    info_output = []
    files_info = {}
    for file in files:
        with open(file) as unit_status_file:
            files_info[file] = json.loads(unit_status_file.read())

    size = None
    step = 0
    global_steps = 1
    for k, vs in files_info.items():
        size = len(vs) * len(files_info)
        break

    while global_steps < size:
        for k, vs in files_info.items():
            info_output.append(vs[step])
            global_steps += 1
        step += 1
    
    os.chdir(root)
    return info_output


def update_info():
    info_mass_flow = get_logfile_info(units_info_folder)
    info_arduinos = get_logfile_info(units_arduino_info_folder)
    info_lcr = get_logfile_info(units_lcr_info_folder)

    info_output = info_arduinos + info_lcr + info_mass_flow 
    info_output.sort()
    
    return info_output

      


