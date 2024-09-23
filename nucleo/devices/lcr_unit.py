import random
import time
import serial


class LCRUnitTest:
    def __init__(self, porta, taxa_de_transmissao=9600, parity='N', stopbit=1, bytesize=8, timeout=1, name='LCR'):
        self.name = name
        self.porta = porta
        self.taxa_de_transmissao = taxa_de_transmissao
        self.parity = parity
        self.stopbits = stopbit
        self.bytesize = bytesize
        self.timeout = timeout
        self.conexao = None
        self.parametros_de_conexao = {
            "url": self.porta,
            "baudrate": self.taxa_de_transmissao,
            "stopbits": self.stopbits,
            "bytesize": self.bytesize,
            "timeout": self.timeout,
        }

    def conectar(self, wait=None): return

    def desconectar(self): return

    def enviar_comando(self, comando): return

    def ler_resposta(self): return
    
    


class LCRUnit:
    def __init__(self, porta, taxa_de_transmissao=9600, parity='N', stopbit=1, bytesize=8, timeout=1, name='LCR'):
        self.name = name
        self.porta = porta
        self.taxa_de_transmissao = taxa_de_transmissao
        self.parity = parity
        self.stopbits = stopbit
        self.bytesize = bytesize
        self.timeout = timeout
        self.conexao = None
        self.parametros_de_conexao = {
            "url": self.porta,
            "baudrate": self.taxa_de_transmissao,
            "stopbits": self.stopbits,
            "bytesize": self.bytesize,
            "timeout": self.timeout,
        }


    def conectar(self, wait=None):
        self.conexao = serial.serial_for_url(**self.parametros_de_conexao, do_not_open=False)

    def desconectar(self):
        self.conexao.close()
        self.conexao = None

    def enviar_comando(self, comando):
        #"TRIG:SOUR MAN" => desligamento?
        self.conexao.write(bytes(str(comando), 'utf-8')) 
    
    
