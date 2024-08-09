from mass_flow_unit import MassFlowUnit
from multiprocessing import Process



baud_rate = 9600

mass_flow_unit1 = MassFlowUnit('COM3', baud_rate)
mass_flow_unit2 = MassFlowUnit('COM4', baud_rate)

print(mass_flow_unit1.enviar_comandos(['DI', 'PI']))
print(mass_flow_unit2.enviar_comandos(['DI', 'PI']))

