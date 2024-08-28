import time
from mass_flow_unit import MassFlowUnit
from orquestrador_mass_flow import Orquestrador

taxa_de_transmissao = 9600

mass_flow_unit1 = MassFlowUnit('COM5', taxa_de_transmissao)
mass_flow_unit2 = MassFlowUnit('COM6', taxa_de_transmissao)
mass_flow_unit3 = MassFlowUnit('COM7', taxa_de_transmissao)
mass_flow_unit4 = MassFlowUnit('COM8', taxa_de_transmissao)


o1 = Orquestrador([mass_flow_unit1, mass_flow_unit2, mass_flow_unit3, mass_flow_unit4])

lista_fluxo_nao_ar_tempo = [
    (0,25),
    (6,25),
    (0,25),
    (12,25),
    (0,25),
    (24,25),
    (0,25),
    (36,25),
    (0,25),
    (48,25),
]

o1.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
o1.executar_rotina()
