import time
import serial

TERMINATOR = "\n"
ENCODING = "ascii"


class LCRUnit:
    def __init__(self, port, taxa_de_transmissao, parity, stopbits, bytesize, timeout):
        self.name = "LCR"
        self.ser = None
        self.transport = None
        self.protocol = None
        self.thread = None
        self.port = port
        self.url = port
        self.baudrate = 9600
        self.parity = 'N'
        self.stopbits = 1
        self.bytesize = 8
        self.timeout = 1
        self.ser_parameters = {
            "url": self.url,
            "baudrate": self.baudrate,
            "stopbits": self.stopbits,
            "bytesize": self.bytesize,
            "timeout": self.timeout,
        }
        self.tempo_total_execucao = None
        self.tempo_transcorrido = None        
        self.conectar()

    def conectar(self, wait=None):
        self.ser = serial.serial_for_url(**self.ser_parameters, do_not_open=False)
        time.sleep(2)
        

    def desconectar(self):
        self.ser.close()


    def enviar_comando(self, comando):
        comando_teste = bytes(comando+f'{TERMINATOR}', ENCODING)# + b'\x10'
        self.ser.write(comando_teste)
        self.ser.flush()
        time.sleep(0.1)
        resposta = self.ser.readline().decode().strip()
        return resposta

    def ler(self):
        resposta = self.ser.readline().decode().strip()
        print(resposta)

    def enviar_comandos(self, comandos):
        for msg in comandos:
            resposta = ''
            print("Comando:", msg)
            while resposta == '':
                resposta = self.enviar_comando(msg).strip()
                self.ler()
                time.sleep(0.01)

    def ler_medidas(self):
        respostas = []
        for _ in range(10):
            resposta = self.enviar_comandos(["*TRG"])
            respostas.append(resposta)
        return respostas



