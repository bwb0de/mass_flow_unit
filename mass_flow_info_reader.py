import json
import os

from config import info_file

def update_info():
    init_dir = os.getcwd()
    os.chdir('mass_flow_data/unit_status')
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
    
    os.chdir(init_dir)
    return info_output

      


