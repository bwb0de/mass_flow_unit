import time
from mass_flow_unit import MassFlowUnit
from multiprocessing import Process



baud_rate = 9600

mass_flow_unit1 = MassFlowUnit('COM5', baud_rate)
mass_flow_unit2 = MassFlowUnit('COM6', baud_rate)
mass_flow_unit3 = MassFlowUnit('COM7', baud_rate)
mass_flow_unit4 = MassFlowUnit('COM8', baud_rate)

'''
parametros_abertura_tempo = [
    (0.0, 1000),
    (1.0, 500),
    (0.0, 500),
    (5.0, 500),
    (0.0, 500),
    (25.0, 500),
    (0.0, 500),
    (100.0, 500)
]
'''

parametros_abertura_tempo = [
    (0.0, 10),
]

for abertura, tempo in parametros_abertura_tempo:
    print(mass_flow_unit1.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
    print(mass_flow_unit2.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
    print(mass_flow_unit3.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
    print(mass_flow_unit4.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
    time.sleep(tempo)

