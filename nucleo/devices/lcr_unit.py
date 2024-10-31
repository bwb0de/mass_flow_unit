import os
import json
import time
import serial
import random
import statistics

from ..paths import units_lcr_info_folder

TERMINATOR = "\n"
ENCODING = "ascii"


class LCRUnitTest:
    def __init__(self, port, taxa_de_transmissao, parity='N', stopbits=1, bytesize=8, timeout=1, numero_medidas=10):
        self.name = "LCR"
        self.ser = None
        self.transport = None
        self.protocol = None
        self.thread = None
        self.port = port
        self.url = port
        self.baudrate = 9600
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.timeout = timeout
        self.numero_medidas = numero_medidas
        self.ser_parameters = {
            "url": self.url,
            "baudrate": self.baudrate,
            "stopbits": self.stopbits,
            "bytesize": self.bytesize,
            "timeout": self.timeout,
        }
        self.tempo_total_execucao = None
        self.tempo_transcorrido = None        
        self.numero_equipamento = '1_mock'
        self.status = []
        self.conectar()

    def __repr__(self) -> str:
        return f'LCR ID({self.numero_equipamento}:{self.port})'

    def conectar(self, wait=None): pass

    def desconectar(self): pass

    def enviar_comando(self, comando): pass

    def ler(self): pass

    def enviar_comandos(self, comandos): pass

    def ler_medidas(self):
        resposta = []
        for _ in range(10):
            primario = random.randint(3, 7) / 100
            secundario = random.randint(3, 7) / 100            
            resposta.append(f'{primario},{secundario}')

        self.status.append(f"[{time.ctime()}] => {self}: executando {self.numero_medidas} medidas...")
        with open(f'{units_lcr_info_folder}{os.sep}{self.numero_equipamento}.json', 'w') as unit_status_file:
            json.dump(self.status, unit_status_file, indent=4)        

        return resposta






class LCRUnit:
    def __init__(self, port, taxa_de_transmissao, parity='N', stopbits=1, bytesize=8, timeout=1, numero_medidas=10):
        self.name = "LCR"
        self.ser = None
        self.transport = None
        self.protocol = None
        self.thread = None
        self.port = port
        self.url = port
        self.baudrate = 9600
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.timeout = timeout
        self.numero_medidas = numero_medidas
        self.ser_parameters = {
            "url": self.url,
            "baudrate": self.baudrate,
            "stopbits": self.stopbits,
            "bytesize": self.bytesize,
            "timeout": self.timeout,
        }
        self.tempo_total_execucao = None
        self.tempo_transcorrido = None        
        self.numero_equipamento = 1
        self.status = []
        self.conectar()

    def __repr__(self) -> str:
        return f'LCR ID({self.numero_equipamento}:{self.port})'

    def conectar(self, wait=None):
        self.ser = serial.serial_for_url(**self.ser_parameters, do_not_open=False)
        time.sleep(2)
        

    def desconectar(self):
        try: self.ser.close()
        except AttributeError: pass
        self.ser = None


    def enviar_comando(self, comando):
        if self.ser == None:
            self.conectar()
        comando_teste = bytes(comando+f'{TERMINATOR}', ENCODING)# + b'\x10'
        self.ser.write(comando_teste)
        self.ser.flush()
        time.sleep(0.1)
        try: resposta = self.ser.readline().decode().strip()
        except UnicodeDecodeError: resposta = ""
        return resposta

    def ler(self):
        resposta = self.ser.readline().decode().strip()
        #print(resposta)

    def enviar_comandos(self, comandos):
        respostas = []
        for msg in comandos:
            resposta = ''
            #print("Comando:", msg)
            while resposta == '':
                resposta = self.enviar_comando(msg).strip()
                self.ler()
                time.sleep(0.01)
            respostas.append(resposta)
        return respostas

    def ler_medidas(self):
        def ignore_trg_response(res):
            if res == "*TRG":
                return None
            return res
        
        if self.ser is None:
            self.conectar()

        comandos = ["*TRG"]
        comandos *= int(self.numero_medidas)
        resposta = self.enviar_comandos(comandos)
        
        respostas_primarias = []
        respostas_secundarias = []
        resposta_processada = []

        for linha in resposta:
            if linha == '*TRG': continue
            try:
                valor_primario, valor_secundario = linha.split(",")
                valor_primario, valor_secundario = float(valor_primario.replace("*TRG", "")), float(valor_secundario.replace("*TRG", ""))
                respostas_primarias.append(valor_primario)
                respostas_secundarias.append(valor_secundario)
                resposta_processada.append((valor_primario, valor_secundario))
            except ValueError: pass
        
        resposta_processada = (statistics.mean(respostas_primarias), statistics.mean(respostas_secundarias))

        self.status.append(f"[{time.ctime()}] => {self}: executando {self.numero_medidas} medidas...")
        with open(f'{units_lcr_info_folder}{os.sep}{self.numero_equipamento}.json', 'w') as unit_status_file:
            json.dump(self.status, unit_status_file, indent=4)        
        self.desconectar()
        #return resposta
        return resposta_processada



