from mass_flow_unit import MassFlowUnit
from multiprocessing import Process



baud_rate = 9600

#mass_flow_unit1 = MassFlowUnit('COM3', baud_rate)
mass_flow_unit2 = MassFlowUnit('COM3', baud_rate)

#print(mass_flow_unit1.enviar_comandos(['DI', 'PI']))
#print(mass_flow_unit2.enviar_comandos(['DI', 'PI', 'MR,1', 'DI', 'MR,2', 'MR,3', 'MR,30', 'AI,M', 'READ,17', 'V,M', 'MR,2', 'M', 'AI,M']))
print(mass_flow_unit2.enviar_comandos(['DI', 'PI', 'SP,0.4', 'SP']))

#SP,Float => Define abertura de fluxo
#SP retorna valor definido...


"""
print(mass_flow_unit2
"""
'''
print(mass_flow_unit2.enviar_comandos([
    'PS,P,1,77.7,8', #SetPoit(%), Time(Sec)
    'PS,A,0xFFFF'])) #Fechamento
'''