import json
import time
import os
import shutil

from multiprocessing import Process
from nucleo.devices.mass_flow_unit import MassFlowUnit
from nucleo.devices.arduino_unit import ArduinoUnit
from nucleo.devices.lcr_unit import LCRUnit
from nucleo.globals.paths import root


from .globals.paths import units_info_folder, units_arduino_info_folder, units_lcr_info_folder

finaliza_rotina = False

class Orquestrador:
    def __init__(self, mass_flow_units:list=[], exp_max_flow=200) -> None:
        self.mass_flow_units = mass_flow_units
        self.exp_max_flow = exp_max_flow
        self.unidades_mass_flow_produto = []
        self.unidades_mass_flow_ar = []
        self.arduino = []
        self.lcr = None
        for unit in mass_flow_units:
            if unit.conteudo_fluxo == 'Ar':
                self.unidades_mass_flow_ar.append(unit)
            else:
                self.unidades_mass_flow_produto.append(unit)
        self.numero_unidades_produto = len(self.unidades_mass_flow_produto)
        self.numero_unidades_ar = len(self.unidades_mass_flow_ar)
        self.script_fluxo = []
        self.script_ajustado_fluxo_tempo_produto = []
        self.script_ajustado_fluxo_tempo_ar = []
        self.unit_status = {}


    @property
    def unidades(self) -> list:
        resposta = self.unidades_mass_flow_ar[:]
        resposta.extend(self.unidades_mass_flow_produto)
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

    def adicionar_arduinos(self, arduino):
        self.arduino = arduino
        self.arduino.vincular_lcr(self.lcr)

    def adicionar_lcr(self, lcr):
        self.lcr = lcr
    
    def distribuir_fluxo_nas_unidades(self, lista_fluxo_nao_ar_tempo:list):
        self.script_fluxo = lista_fluxo_nao_ar_tempo
        self.script_ajustado_fluxo_tempo_produto = []
        self.script_ajustado_fluxo_tempo_ar = []

        tempo_total = 0
        
        for fluxo, tempo in lista_fluxo_nao_ar_tempo:
            assert fluxo <= self.exp_max_flow, "Fluxo definido supera o fluxo máximo do orquestrador..."
            fluxo_produto = fluxo / self.numero_unidades_produto
            fluxo_ar = (self.exp_max_flow - fluxo) / self.numero_unidades_ar
            self.script_ajustado_fluxo_tempo_produto.append((fluxo_produto, tempo))
            self.script_ajustado_fluxo_tempo_ar.append((fluxo_ar, tempo))
            tempo_total += tempo
        
        for unidade in self.unidades_mass_flow_ar:
            unidade.inserir_na_fila_execucao(self.script_ajustado_fluxo_tempo_ar)

        for unidade in self.unidades_mass_flow_produto:
            unidade.inserir_na_fila_execucao(self.script_ajustado_fluxo_tempo_produto)

        self.arduino.definir_tempo_total_execucao(tempo_total)


    def executar_rotina(self):
        print(f'Executando rotina: {self.script_fluxo}'); print('')
        for unidade in self.unidades:
            unidade.modo_digital()

        shutil.rmtree(units_info_folder)
        os.mkdir(units_info_folder)
        shutil.rmtree(units_lcr_info_folder)
        os.mkdir(units_lcr_info_folder)
        shutil.rmtree(units_arduino_info_folder)
        os.mkdir(units_arduino_info_folder)


        self.processos = []

        for unidade in self.unidades:
            processo = Process(target=executa_subprocesso_mass_flow, args=(unidade, ))
            processo.unit_status = unidade.numero_equipamento
            self.processos.append(processo)
            processo.start()
        
        time.sleep(1)

        processo_arduino = Process(target=executa_subprocesso_arduino, args=(self.arduino, ))
        self.processos.append(processo_arduino)
        processo_arduino.start()

    def status_das_rotinas_em_execucao(self):
        retorno = []
        for p in self.processos:
            print(p.unit_status)
        return retorno

    def status_equipamentos(self):
        retorno = []
        for unit in self.unidades:
            retorno.append(unit.obter_estado_equipamento())
        return retorno

    def interromper(self):
        print('interrompendo...')
        for unit in self.unidades:
            unit.fechar_fluxo()
            
        return [p.terminate() for p in self.processos]




def executa_subprocesso_mass_flow(objeto: MassFlowUnit):
    n = 1
    tempo_espera = objeto.executar_acao_da_fila()
    time.sleep(tempo_espera)
    while True:
        n += 1
        tempo_espera = objeto.executar_acao_da_fila()
        if tempo_espera is None: break
        time.sleep(tempo_espera)
    global finaliza_rotina
    finaliza_rotina = True
    os.system(f'python {root}\\nucleo\\construtor_tabela_resultados.py&')
    os.system(f'python {root}\\nucleo\\kill_ipvh_srv.py&')



def executa_subprocesso_arduino(objeto: ArduinoUnit):
    global finaliza_rotina
    tempo_espera = objeto.executar_acao_da_fila()
    time.sleep(tempo_espera)
    while True:
        tempo_espera = objeto.executar_acao_da_fila()
        if tempo_espera is None: break
        time.sleep(tempo_espera)
        if finaliza_rotina: break

