import random
import time
import serial

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

    def conectar(self):
        self.conexao = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

    def desconectar(self):
        self.conexao.close()
        time.sleep(0.05)
        self.conexao = None

    def enviar_comando(self, comando):
        if self.conexao is None: print("É necessário conectar antes de enviar comandos..."); return
        self.conexao.write(bytes(str(comando), 'utf-8')) 
        time.sleep(0.05)

    def ler_resposta(self):
        resposta = self.conexao.readline().decode('utf-8').strip()

        respostas = {
            '1': 'Luzes ligadas',
            '2': 'Luzes desligadas',
            '9': 'Comando desconhecido'
        }

        return respostas.get(resposta) if resposta in respostas else ''

