import os
import serial
import time
import json
import random

from ..paths import units_info_folder
from ..ipvh_srv import send_command

class MassFlowUnitTest:
    def __init__(self, porta, taxa_de_transmissao, fluxo_maximo:int, conteudo_fluxo:str) -> None:
        self.porta_de_conexao = porta
        self.taxa_de_transmissao = taxa_de_transmissao
        self.arquivo_de_rotina = None
        self.numero_equipamento = str(random.randint(0,999999)).zfill(6)+'-'+str(random.randint(0,999)).zfill(3)+'mock'
        self.fluxo_maximo = fluxo_maximo
        self.conteudo_fluxo = conteudo_fluxo
        self.fracao_de_fluxo = 100/self.fluxo_maximo
        self.fila_execucao = [] #incluir
        self.parar_rotina = None
        self.etapa_execucao = 0
        self.fluxo_corrente = None
        self.status = []

    def __repr__(self) -> str:
        label_p = '   ' if self.conteudo_fluxo == 'Ar' else '[p]'
        return f'MassFlowUnit ID({self.numero_equipamento}:{self.porta_de_conexao}){label_p}'

    def inserir_na_fila_execucao(self, script_ajustado_fluxo):
        self.etapa_execucao = 0
        self.fila_execucao = script_ajustado_fluxo

    def executar_acao_da_fila(self):
        if self.fila_execucao == []: 
            self.fechar_fluxo()
            return
        self.etapa_execucao += 1
        self.parar_rotina = False        
        fluxo, tempo = self.fila_execucao[0]
        self.fluxo_corrente = fluxo
        self.fila_execucao = self.fila_execucao[1:]
        print(f"{self}: definindo fluxo para {fluxo}")
        self.status.append(f"[{time.ctime()}] => {self}: definindo fluxo para {fluxo}")
        with open(f'{units_info_folder}{os.sep}{self.numero_equipamento}.json', 'w') as unit_status_file:
            json.dump(self.status, unit_status_file, indent=4)
        return tempo


    def checar_execucao(self):
        return f'{self}: executando etapa {self.etapa_execucao}, com fluxo {self.fluxo_corrente}...'

    def modo_digital(self):
        print(f'{self}: entrando em modo digital com válvula no automático...')

    def fechar_fluxo(self):
        print(f'{self}: fechando fluxo...')
        self.status.append(f'[{time.ctime()}] => {self}: fechando fluxo...')
        with open(f'{units_info_folder}{os.sep}{self.numero_equipamento}.json', 'w') as unit_status_file:
            json.dump(self.status, unit_status_file, indent=4)        

    def obter_estado_equipamento(self):
        resposta = {
            "Mass Flow": "lorem ysilon",
            "Volumetric Flow": "lorem ysilon",
            "Total1 MEU": "lorem ysilon",
            "Total2 MEU": "lorem ysilon",
            "Temperatura Gás": "lorem ysilon", #Firehaint?
            "Pressão Gás": "lorem ysilon",
            "Situação Alarme Flow": "lorem ysilon",
            "Situação Alarme Temperatura": "lorem ysilon",
            "Situação Alarme Pressão": "lorem ysilon",
            "Alarm Event Register": "lorem ysilon", #Tradutor hexcode
            "Diagnostic Event Register": "lorem ysilon", #Tradutor hexcode
            "Gás Index": "lorem ysilon",
            "Gás Name": "lorem ysilon",
            "Current Mass Unit":"lorem ysilon",
            "Current Volumetric Unit": "lorem ysilon",
            "Analog Output": "lorem ysilon",
            "ModBuss": "lorem ysilon"
        }

        return resposta



class MassFlowUnit:
    def __init__(self, porta_de_conexao, taxa_de_transmissao, fluxo_maximo, conteudo_fluxo, timeout=1) -> None:
        self.porta_de_conexao = porta_de_conexao
        self.taxa_de_transmissao = taxa_de_transmissao
        self.arquivo_de_rotina = None
        self.numero_equipamento = self.enviar_comando('MR,1')
        self.parar_rotina = None
        self.etapa_execucao = 0
        self.etapas_microciclo = 0
        self.fluxo_corrente = None
        self.fluxo_maximo = fluxo_maximo
        self.conteudo_fluxo = conteudo_fluxo
        self.status = []

        if self.numero_equipamento in {'624643-1','608314-1'}:
            self.fluxo_maximo = 100
        elif self.numero_equipamento in {'624644-1','608315-1'}:
            self.fluxo_maximo = 200

        # Ar e não ar...
        if self.numero_equipamento in {'624643-1','608314-1'}:
            self.conteudo_fluxo = 'produto'
        elif self.numero_equipamento in {'624644-1','608315-1'}:
            self.conteudo_fluxo = 'Ar'

        self.fracao_de_fluxo = 100/self.fluxo_maximo
        self.fila_execucao = [] 
        
    def __repr__(self) -> str:
        label_p = '   ' if self.conteudo_fluxo == 'Ar' else '[p]'
        return f'MassFlowUnit ID({self.numero_equipamento}:{self.porta_de_conexao}){label_p}'

    def inserir_na_fila_execucao(self, script_ajustado_fluxo):
        self.etapa_execucao = 0
        self.fila_execucao = script_ajustado_fluxo

    def executar_acao_da_fila(self):
        if self.fila_execucao == []: 
            self.fechar_fluxo()
            return
        self.etapa_execucao += 1

        if self.etapa_execucao % self.etapas_microciclo == 0:
            send_command("@")

        self.parar_rotina = False        
        fluxo, tempo = self.fila_execucao[0]
        self.fluxo_corrente = fluxo
        self.fila_execucao = self.fila_execucao[1:]
        print(f"{self}: definindo fluxo para {fluxo}")
        self.enviar_comandos([f'SP,{fluxo}'])
        self.status.append(f"[{time.ctime()}] => {self}: definindo fluxo para {fluxo}")
        with open(f'{units_info_folder}{os.sep}{self.numero_equipamento}.json', 'w') as unit_status_file:
            json.dump(self.status, unit_status_file, indent=4)
        return tempo
    
    def checar_execucao(self):
        return f'{self}: executando etapa {self.etapa_execucao}, com fluxo {self.fluxo_corrente}...'

    def modo_digital(self):
        print(f'{self}: entrando em modo digital com válvula no automático...')
        self.enviar_comandos(['M,D', 'SP,0.0', 'SP', 'V,M,A'])

    def fechar_fluxo(self):
        print(f'{self}: fechando fluxo...')
        self.status.append(f"[{time.ctime()}] => {self}: fechando fluxo...")
        with open(f'{units_info_folder}{os.sep}{self.numero_equipamento}.json', 'w') as unit_status_file:
            json.dump(self.status, unit_status_file, indent=4)
        self.enviar_comandos(['V,M,C'])

    def enviar_comandos(self, commandos: list):
        if commandos == []: return

        try:
            with serial.Serial(self.porta_de_conexao, self.taxa_de_transmissao, timeout=1) as ser:
                respostas = []
                for cmd in commandos:
                    comando_teste = bytes(f'{cmd}\r\n', 'utf-8')
                    ser.write(comando_teste)
                    resposta = ser.readline().decode().strip()
                    respostas.append((cmd, resposta))
                return respostas

        except serial.SerialException as e:
            print(f"Erro ao conectar na porta serial: {e}")    
            return "Erro"    

    def enviar_comando(self, comando: str):
        try:
            with serial.Serial(self.porta_de_conexao, self.taxa_de_transmissao, timeout=1) as ser:
                comando_teste = bytes(f'{comando}\r\n', 'utf-8')  
                ser.write(comando_teste)
                resposta = ser.readline().decode().strip()
                return resposta

        except serial.SerialException as e:
            print(f"Erro ao conectar na porta serial: {e}")        

    def obter_estado_equipamento(self):
        dados = self.enviar_comandos([
            'DI',
            'PI',
            'MR,1',
            'MR,2',
            'MR,3',
            'AI,M',
            'READ,17',
            'V,M'
        ])

        return dados

        gas_idx, gas_name, current_mass_eng_unit, current_volum_eng_unit, totalizer1_mode, totalizer2_mode, analog_output, mod_buss = dados[0][1].split(',')
        mass_flow, volumetric_flow, total_meu_1, total_meu_2, gas_temp, gas_press, flow_alarm_st, temp_alarm_st, press_alarm_st, alarm_ev_register, diagnostic_ev_register = dados[1][1]

        resposta = {
            "Mass Flow": float(mass_flow),
            "Volumetric Flow": float(volumetric_flow),
            "Total1 MEU": float(total_meu_1),
            "Total2 MEU": float(total_meu_2),
            "Temperatura Gás": float(gas_temp), #Firehaint?
            "Pressão Gás": float(gas_press),
            "Situação Alarme Flow": self.alarm_st_translator[flow_alarm_st],
            "Situação Alarme Temperatura": self.alarm_st_translator[temp_alarm_st],
            "Situação Alarme Pressão": self.alarm_st_translator[press_alarm_st],
            "Alarm Event Register": alarm_ev_register, #Tradutor hexcode
            "Diagnostic Event Register": diagnostic_ev_register, #Tradutor hexcode
            "Gás Index": gas_idx,
            "Gás Name": gas_name,
            "Current Mass Unit":current_mass_eng_unit,
            "Current Volumetric Unit": current_volum_eng_unit,
            "Analog Output": self.analog_output_translator[analog_output],
            "ModBuss": self.mod_buss_translator[mod_buss],
            dados[2][0]: dados[2][1],
            dados[3][0]: dados[3][1],
            dados[4][0]: dados[4][1],
            dados[5][0]: dados[5][1],
            dados[6][0]: dados[6][1],
            dados[7][0]: dados[7][1],
        }


        return resposta

