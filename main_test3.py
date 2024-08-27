#Orquestrador
import itertools
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
    def __init__(self, mass_flow_units:list=[], exp_max_flow=200) -> None:
        self.mass_flow_units = mass_flow_units
        self.exp_max_flow = exp_max_flow
        self.unidades_produto = []
        self.unidades_ar = []
        for unit in mass_flow_units:
            if unit.conteudo_fluxo == 'Ar':
                self.unidades_ar.append(unit)
            else:
                self.unidades_produto.append(unit)
        self.numero_unidades_produto = len(self.unidades_produto)
        self.numero_unidades_ar = len(self.unidades_ar)
        self.script_ajustado_fluxo_tempo_produto = []
        self.script_ajustado_fluxo_tempo_ar = []


    @property
    def unidades(self) -> list:
        resposta = self.unidades_ar[:]
        resposta.extend(self.unidades_produto)
        return resposta
    

    @property
    def unidades_info(self) -> None:
        for unit in self.unidades:
            print(f'MassFlowUnit ID: {unit.numero_equipamento}')
            print(f'Porta: {unit.porta_de_conexao}')
            print(f'Fluxo máximo aparelho unidade: {unit.fluxo_maximo}')
            print(f'Conteúdo fluxo: {unit.conteudo_fluxo}')
            print(f'Fração de fluxo: {unit.fracao_de_fluxo}')
            print('')
    
    def calcular_distribuicao_de_fluxo(self, lista_fluxo_nao_ar_tempo:list):
        self.script_ajustado_fluxo_tempo_produto = []
        self.script_ajustado_fluxo_tempo_ar = []
        
        for fluxo, tempo in lista_fluxo_nao_ar_tempo:
            assert fluxo <= self.exp_max_flow, "Fluxo definido supera o fluxo máximo do orquestrador..."
            fluxo_produto = fluxo / self.numero_unidades_produto
            fluxo_ar = (self.exp_max_flow - fluxo) / self.numero_unidades_ar
            self.script_ajustado_fluxo_tempo_produto.append((fluxo_produto, tempo))
            self.script_ajustado_fluxo_tempo_ar.append((fluxo_ar, tempo))

    def executar_rotina(self):

        script_total = []
        
        for unidade in self.unidades_ar:
            script_parcial = []
            for fluxo, tempo in self.script_ajustado_fluxo_tempo_ar:
                script_parcial.append(unidade, )
            

        script_parcial = []
        for unidade in self.unidades_produto:
            combinacao = itertools.combinations([unidade, self.script_ajustado_fluxo_tempo_produto])
            script_total.append(combinacao)

        for p in script_total:
            print(p)

        '''

        for unit in self.unidades_produto:
            for fluxo, tempo in self.script_ajustado_fluxo_tempo_produto:
                print(f'MassFlowUnit ID[p]: {unit.numero_equipamento}, abetura: fluxo = {fluxo}({fluxo*unit.fracao_de_fluxo}) ++ ({fluxo/unit.fluxo_maximo})')
        
        for unit in self.unidades_ar:
            for fluxo, tempo in self.script_ajustado_fluxo_tempo_ar:
                print(f'MassFlowUnit ID   : {unit.numero_equipamento}, abetura: fluxo = {fluxo}({fluxo*unit.fracao_de_fluxo}) ++ ({fluxo/unit.fluxo_maximo})')
        '''

        '''
        for abertura, tempo in parametros_abertura_tempo:
            print(mass_flow_unit1.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
            print(mass_flow_unit2.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
            print(mass_flow_unit3.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
            print(mass_flow_unit4.enviar_comandos(['DI', 'PI','M,D', f'SP,{abertura}', 'SP', 'V,M,A']))
            time.sleep(tempo)
        '''


            

mu1 = MassFlowUnitMock('COM3', 9600, 100, 'produto')
mu2 = MassFlowUnitMock('COM3', 9600, 200, 'Ar')
mu3 = MassFlowUnitMock('COM3', 9600, 200, 'Ar')

o = Orquestrador([mu1, mu2, mu3])

lista_fluxo_nao_ar_tempo = [
    (0,50),
    (1,50),
    (0,50),
    (2,50),
    (0,50),
    (3,50),
    (0,50),
    (4,50),
    (0,50),
    (10,50),
]

o.calcular_distribuicao_de_fluxo(lista_fluxo_nao_ar_tempo)
o.executar_rotina()


        