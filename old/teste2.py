from pprint import pprint
import time

def criar_rotina_de_setpoints(command_args: list):
    psp_base = [
        'M:P',           #Inicia program set_point
        'VM:C',          #Fecha a válvula
        'AIM:2',         #Define novo modo de input analógico
        'PSM:E',         #Habilita modo PSP (program set point) (16) slots
        'PSC:S.01',      #Habilita modo PSP (program set point) (16) slots
        'PSL:E',         #Habilita modo loop do PSP
        'PSA:0xFFFF'     #Habilita modo loop do PSP
    ]

    rotina = {}

    output_wait_time = []

    output = []
    output.extend(psp_base)

    n = 1
    arguments_pending = len(command_args)
    wait_time = 0

    for percent_arg, time_arg in command_args:
        n_str = str(n).zfill(2)
        wait_time += int(time_arg)
        output.append(f'PSP{n}:{percent_arg},{time_arg}')
        n += 1
        arguments_pending -= 1
        if n == 17 and arguments_pending > 0:
            output.append('PSC:R')
            output.extend(psp_base)
            output_wait_time.append(wait_time)
            wait_time = 0
            n = 1

    output.append('PSC:R')
    output_wait_time.append(wait_time)

    rotina['commands'] = output
    rotina['wait_time'] = output_wait_time

    return rotina



teste = [ 
    (0.0, 1),
    (0.0, 1),
    (1.0, 1),
    (1.0, 1),
    (0.0, 1),
    (0.0, 1),
    (5.0, 1),
    (5.0, 1),
    (0.0, 1),
    (0.0, 1),
    (25.0, 1),
    (25.0, 1),
    (0.0, 1),
    (0.0, 1),
    (100.0, 1),
    (100.0, 1),
    (75.0, 1),
    (75.0, 1),
    (85.0, 1),
    (85.0, 1),
    (95.0, 1),
    (95.0, 1),
]

rotina = make_full_psp_command_list(teste)

def execute_command_routine(command_routine):
    assert isinstance(command_routine, dict)
    assert not command_routine.get('commands') is None
    assert not command_routine.get('wait_time') is None

    commands = command_routine['commands']
    wait_time = command_routine['wait_time']
    wait_step = 0

    for command in commands:
        print(command)
        if command == 'PSC:R':
            print("Aguardando execução desta seção da rotina...")
            time.sleep(wait_time[wait_step])
    print("Execução concluída...")



execute_command_routine(rotina)