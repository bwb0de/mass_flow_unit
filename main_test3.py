#Orquestrador

import time

class MassFlowUnitMock:
    def __init__(self, porta, taxa_de_transmissao, fluxo_maximo:int, conteudo_fluxo:str) -> None:
        self.porta_de_conexao = porta
        self.taxa_de_transmissao = taxa_de_transmissao
        self.arquivo_de_rotina = None
        self.numero_equipamento = '999999-9mock'
        self.fluxo_maximo = fluxo_maximo
        self.conteudo_fluxo = conteudo_fluxo
        self.fracao_de_fluxo = 100/self.fluxo_maximo

class Orquestrador:
    def __init__(self, mass_flow_units:list=[]) -> None:
        self.mass_flow_units = mass_flow_units

    def unidades_vinculadas(self) -> None:
        for unit in self.mass_flow_units:
            print(f'MassFlowUnit ID: {unit.numero_equipamento}')
            print(f'Porta: {unit.porta_de_conexao}')
            print(f'Fluxo máximo: {unit.fluxo_maximo}')
            print(f'Conteúdo fluxo: {unit.conteudo_fluxo}')
            print(f'Fração de fluxo: {unit.fracao_de_fluxo}')
            print('')

mu1 = MassFlowUnitMock('COM3', 9600, 100, 'produto')
mu2 = MassFlowUnitMock('COM3', 9600, 200, 'Ar')
mu3 = MassFlowUnitMock('COM3', 9600, 200, 'Ar')

o = Orquestrador([mu1, mu2, mu3])

o.unidades_vinculadas()
        