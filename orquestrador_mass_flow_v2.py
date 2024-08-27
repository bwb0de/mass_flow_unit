import time

from multiprocessing import Process
from mass_flow_unit import MassFlowUnit

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
        self.script_fluxo = []
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
    
    def distribuir_fluxo_nas_unidades(self, lista_fluxo_nao_ar_tempo:list):
        self.script_fluxo = lista_fluxo_nao_ar_tempo
        self.script_ajustado_fluxo_tempo_produto = []
        self.script_ajustado_fluxo_tempo_ar = []
        
        for fluxo, tempo in lista_fluxo_nao_ar_tempo:
            assert fluxo <= self.exp_max_flow, "Fluxo definido supera o fluxo máximo do orquestrador..."
            fluxo_produto = fluxo / self.numero_unidades_produto
            fluxo_ar = (self.exp_max_flow - fluxo) / self.numero_unidades_ar
            self.script_ajustado_fluxo_tempo_produto.append((fluxo_produto, tempo))
            self.script_ajustado_fluxo_tempo_ar.append((fluxo_ar, tempo))
        
        for unidade in self.unidades_ar:
            unidade.inserir_na_fila_execucao(self.script_ajustado_fluxo_tempo_ar)

        for unidade in self.unidades_produto:
            unidade.inserir_na_fila_execucao(self.script_ajustado_fluxo_tempo_produto)


    def executar_rotina(self):
        def executa_subprocesso(objeto: MassFlowUnit):
            n = 1
            tempo_espera = objeto.executar_acao_da_fila()
            print(f'{objeto} executando passo {n}')
            time.sleep(tempo_espera)
            while True:
                n += 1
                tempo_espera = objeto.executar_acao_da_fila()
                if tempo_espera is None: break
                time.sleep(tempo_espera)                

        print(f'Executando rotina: {self.script_fluxo}'); print('')
        for unidade in self.unidades:
            unidade.modo_digital()

        self.processos = []

        for unidade in self.unidades:
            processo = Process(target=executa_subprocesso, args=(unidade,))
            self.processos.append(processo)
            processo.start()

    def status_das_rotinas_em_execucao(self):
        return [p.is_alive() for p in self.processos]

    def interromper(self):
        print('interrompendo...')
        return [p.terminate() for p in self.processos]

