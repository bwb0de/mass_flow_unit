from mass_flow_unit import MassFlowUnitTest
from orquestrador_mass_flow import Orquestrador

taxa_de_transmissao = 9600

mu1 = MassFlowUnitTest('COM3', 9600, 100, 'produto')
mu2 = MassFlowUnitTest('COM4', 9600, 200, 'Ar')
mu3 = MassFlowUnitTest('COM5', 9600, 200, 'Ar')


mu4 = MassFlowUnitTest('COM6', 9600, 100, 'produto')
mu5 = MassFlowUnitTest('COM7', 9600, 200, 'produto')
mu6 = MassFlowUnitTest('COM8', 9600, 200, 'Ar')


o1 = Orquestrador([mu1, mu2, mu3])
o2 = Orquestrador([mu4, mu5, mu6])

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

o2.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
o2.executar_rotina()


        