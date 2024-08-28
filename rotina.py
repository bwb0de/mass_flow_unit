import time
from mass_flow_unit import MassFlowUnit
from orquestrador_mass_flow_v3 import Orquestrador
from parametros import lista_fluxo_nao_ar_tempo

taxa_de_transmissao = 9600

mass_flow_unit1 = MassFlowUnit('COM5', taxa_de_transmissao)
mass_flow_unit2 = MassFlowUnit('COM6', taxa_de_transmissao)
mass_flow_unit3 = MassFlowUnit('COM7', taxa_de_transmissao)
mass_flow_unit4 = MassFlowUnit('COM8', taxa_de_transmissao)


from mass_flow_unit import MassFlowUnitTest
from orquestrador_mass_flow_v3 import Orquestrador

taxa_de_transmissao = 9600

mu1 = MassFlowUnitTest('COM3', 9600, 100, 'produto')
mu2 = MassFlowUnitTest('COM4', 9600, 200, 'Ar')
mu3 = MassFlowUnitTest('COM5', 9600, 200, 'Ar')

o1 = Orquestrador([mu1, mu2, mu3])




o1 = Orquestrador([mass_flow_unit1, mass_flow_unit2, mass_flow_unit3, mass_flow_unit4], exp_max_flow=400)

o1.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
o1.executar_rotina()
