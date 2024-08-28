from mass_flow_unit import MassFlowUnit
#from orquestrador_mass_flow import Orquestrador
from orquestrador_mass_flow_v2 import Orquestrador

taxa_de_transmissao = 9600

mass_flow_unit1 = MassFlowUnit('COM5', taxa_de_transmissao)
mass_flow_unit2 = MassFlowUnit('COM6', taxa_de_transmissao)
mass_flow_unit3 = MassFlowUnit('COM7', taxa_de_transmissao)
mass_flow_unit4 = MassFlowUnit('COM8', taxa_de_transmissao)


o1 = Orquestrador([mass_flow_unit1, mass_flow_unit2, mass_flow_unit3, mass_flow_unit4])

lista_fluxo_nao_ar_tempo = [
    (0,10),
    (6,10),
    (0,10),
    (12,10),
    (0,10),
    (24,10),
    (0,10),
    (36,10),
    (0,10),
    (48,10),
]

o1.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
o1.executar_rotina()


        