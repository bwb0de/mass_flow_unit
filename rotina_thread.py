from orquestrador_mass_flow_v3 import Orquestrador
from parametros import lista_fluxo_nao_ar_tempo
from mass_flow_unit import MassFlowUnitTest


taxa_de_transmissao = 9600

mu1 = MassFlowUnitTest('COM3', 9600, 100, 'produto')
mu2 = MassFlowUnitTest('COM4', 9600, 200, 'Ar')
mu3 = MassFlowUnitTest('COM5', 9600, 200, 'Ar')

o1 = Orquestrador([mu1, mu2, mu3])


o1.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
o1.executar_rotina()
