import random
import time
import serial

from nucleo.ipvh_srv import set_value

class ArduinoUnitTest:
    def __init__(self, porta, taxa_de_transmissao:int=9600, modelo:str='uno', nome=None) -> None:
        self.nome = str(random.randint(0,1000)).zfill(4) + 'mock'
        self.modelo = 14
        self.porta = porta
        self.taxa_de_transmissao = taxa_de_transmissao
        self.conexao = None

    def conectar(self): return
        
    def desconectar(self): return

    def enviar_comando(self, data): return

    def ler_resposta(self): return



class ArduinoUnit:
    def __init__(self, porta, taxa_de_transmissao:int=9600, modelo:str='uno', nome=None) -> None:
        modelos = {'uno': 14, 'mega': 54}
        assert(modelo in modelos), "Os modelos conhecidos são UNO ou MEGA..."
        self.nome = str(random.randint(0,1000)).zfill(4) if nome is None else nome
        self.modelo = modelos[modelo.lower()]
        self.porta = porta
        self.taxa_de_transmissao = taxa_de_transmissao
        self.conexao = None
        self.sensor_corrente = None
        self.tempo_total_execucao = None
        self.tempo_transcorrido = None
        self.conectar()

    def definir_tempo_total_execucao(self, tempo):
        self.tempo_total_execucao = tempo

    def vincular_lcr(self, lcr):
        self.lcr = lcr

    def conectar(self):
        self.conexao = serial.Serial(port=self.porta, baudrate=self.taxa_de_transmissao, timeout=.1)
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

        tempo_step = 3

        self.tempo_transcorrido += tempo_step
        if self.tempo_transcorrido > self.tempo_total_execucao:
            return None
        return tempo_step


