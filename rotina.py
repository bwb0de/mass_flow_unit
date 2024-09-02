import json

from mass_flow_unit import MassFlowUnit
from mass_flow_orquestrator_parallel import Orquestrador

lista_fluxo_nao_ar_tempo = None
with open('parametros.json', 'r') as arquivo_parametros:
    lista_fluxo_nao_ar_tempo = json.loads(arquivo_parametros.read())


taxa_de_transmissao = 9600

mu1 = MassFlowUnit('COM5', taxa_de_transmissao)
mu2 = MassFlowUnit('COM6', taxa_de_transmissao)
mu3 = MassFlowUnit('COM7', taxa_de_transmissao)
mu4 = MassFlowUnit('COM8', taxa_de_transmissao)


if __name__ == '__main__':
    o1 = Orquestrador([mu1, mu2, mu3, mu4])
    o1.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
    o1.executar_rotina()