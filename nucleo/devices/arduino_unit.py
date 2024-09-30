import os
import json
import random
import time
import serial

from nucleo.ipvh_srv import set_value

from ..paths import units_arduino_info_folder

class ArduinoUnitTest:
    def __init__(self, porta, taxa_de_transmissao:int=9600, modelo:str='uno', nome=None, tempo_espera=3) -> None:
        modelos = {'uno': 14, 'mega': 54}
        assert(modelo in modelos), "Os modelos conhecidos são UNO ou MEGA..."
        self.nome = str(random.randint(0,1000)).zfill(4) if nome is None else nome
        self.modelo = modelos[modelo.lower()]
        self.porta_de_conexao = porta
        self.taxa_de_transmissao = taxa_de_transmissao
        self.conexao = None
        self.sensor_corrente = None
        self.tempo_total_execucao = None
        self.tempo_transcorrido = 0
        self.status = []
        self.numero_equipamento = '1_mock'
        self.sensor_corrente = 0
        self.conectar()

    def __repr__(self) -> str:
        return f'Arduino ID({self.numero_equipamento}:{self.porta_de_conexao})'

    def definir_tempo_total_execucao(self, tempo):
        self.tempo_total_execucao = tempo

    def vincular_lcr(self, lcr):
        self.lcr = lcr

    def conectar(self): pass

    def desconectar(self): pass

    def enviar_comando(self, comando): pass

    def ler_resposta(self): pass

    def executar_acao_da_fila(self):
        self.sensor_corrente += 1
        if self.sensor_corrente > 8:
            self.sensor_corrente = 1
        self.valores_lcr = self.lcr.ler_medidas()
        set_value('sensor_corrente', self.sensor_corrente)

        tempo_step = 3

        self.status.append(f"[{time.ctime()}] => {self}: modificando sensor para {self.sensor_corrente}")
        with open(f'{units_arduino_info_folder}{os.sep}{self.numero_equipamento}.json', 'w') as unit_status_file:
            json.dump(self.status, unit_status_file, indent=4)        

        self.tempo_transcorrido += tempo_step
        if self.tempo_transcorrido > self.tempo_total_execucao:
            return None
        
        return tempo_step




class ArduinoUnit:
    def __init__(self, porta, taxa_de_transmissao:int=9600, modelo:str='uno', nome=None, tempo_espera=3) -> None:
        modelos = {'uno': 14, 'mega': 54}
        assert(modelo in modelos), "Os modelos conhecidos são UNO ou MEGA..."
        self.nome = str(random.randint(0,1000)).zfill(4) if nome is None else nome
        self.modelo = modelos[modelo.lower()]
        self.porta_de_conexao = porta
        self.taxa_de_transmissao = taxa_de_transmissao
        self.conexao = None
        self.sensor_corrente = None
        self.tempo_total_execucao = None
        self.tempo_transcorrido = None
        self.status = []
        self.numero_equipamento = 1
        self.tempo_espera = tempo_espera
        self.conectar()

    def __repr__(self) -> str:
        return f'Arduino ID({self.numero_equipamento}:{self.porta_de_conexao})'

    def definir_tempo_total_execucao(self, tempo):
        self.tempo_total_execucao = tempo

    def vincular_lcr(self, lcr):
        self.lcr = lcr

    def conectar(self):
        self.conexao = serial.Serial(port=self.porta_de_conexao, baudrate=self.taxa_de_transmissao, timeout=.1)
        time.sleep(1.50)

    def desconectar(self):
        self.conexao.close()
        time.sleep(1.50)
        self.conexao = None

    def enviar_comando(self, comando):
        if self.conexao is None: print("É necessário conectar antes de enviar comandos..."); return
        self.conexao.write(bytes(str(comando), 'utf-8'))
        time.sleep(0.5)

    def ler_resposta(self):
        resposta = self.conexao.readline().decode('utf-8').strip()
        return resposta

    def executar_acao_da_fila(self):
        if self.conexao is None:
            self.conectar()
        if self.tempo_transcorrido is None:
            self.tempo_transcorrido = 0

        self.enviar_comando('proximo_sensor')

        self.sensor_corrente = self.ler_resposta()
        self.valores_lcr = self.lcr.ler_medidas()
        set_value('sensor_corrente', self.sensor_corrente)

        tempo_step = self.tempo_espera

        self.status.append(f"[{time.ctime()}] => {self}: modificando sensor para {self.sensor_corrente}")
        with open(f'{units_arduino_info_folder}{os.sep}{self.numero_equipamento}.json', 'w') as unit_status_file:
            json.dump(self.status, unit_status_file, indent=4)        

        self.tempo_transcorrido += tempo_step
        if self.tempo_transcorrido > self.tempo_total_execucao:
            return None
        return tempo_step


