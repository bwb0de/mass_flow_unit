import os
from pprint import pprint
from mass_flow_unit import MassFlowUnit

baud_rate = 9600  

mass_flow_unit1 = MassFlowUnit('COM4', baud_rate)
mass_flow_unit2 = MassFlowUnit('COM8', baud_rate)

pprint(mass_flow_unit1.obter_estado_equipamento(), os.linesep*2)
pprint(mass_flow_unit2.obter_estado_equipamento())

