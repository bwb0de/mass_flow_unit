from mass_flow_unit import MassFlowUnit
from multiprocessing import Process



baud_rate = 9600

#mass_flow_unit1 = MassFlowUnit('COM3', baud_rate)
mass_flow_unit2 = MassFlowUnit('COM4', baud_rate)

#print(mass_flow_unit1.enviar_comandos(['DI', 'PI']))
print(mass_flow_unit2.enviar_comandos(['DI', 'PI', 'MR,1', 'DI', 'MR,2', 'MR,3', 'MR,30', 'AI,M', 'READ,17', 'V,M', 'MR,2', 'M', 'AI,M']))
print(mass_flow_unit2.enviar_comandos([
    'PS,M',
    'PS,C',
    'PS,L',
    'PS,P,1',
    'PS,P,2',
    'PS,P,3',
    'PS,P,4',
    'PS,P,5',
    'PS,P,6',
    'PS,P,7',
    'PS,P,8',
    'PS,P,9',
    'PS,P,10',
    'PS,P,11',
    'PS,P,12',
    'PS,P,13',
    'PS,P,14',
    'PS,P,15',
    'PS,P,16']))

