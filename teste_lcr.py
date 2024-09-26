import time
import serial

porta_de_conexao = 'COM5'
TERMINATOR = "\n"
ENCODING = "ascii"
#ENCODING = "utf-8"

class LCRConnection:
    def __init__(self, port):
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

        self.connect()

    def connect(self, wait=None):
        self.ser = serial.serial_for_url(**self.ser_parameters, do_not_open=False)

    def close(self):
        self.ser.close()

    def enviar_comandos(self, comandos:list):
        respostas = []
        #resposta = b''
        #for cmd in comandos:
        #    comando_teste = bytes(f'{cmd}{TERMINATOR}', ENCODING)
        #    self.ser.write(comando_teste)
        #    n = 0
        #    while True:
        #        n+=1
        #        print(n)
        #        data = self.ser.read(1)  # Read one byte at a time
        #        if data == b'\x10':  # Substituído por b'\x10' (NL)
        #            break
        #        resposta += data
        #        respostas.append((cmd, resposta.decode('ascii')))  # Mantendo 'ascii'
        #        if n==3: break
#
        #print(respostas)        
        respostas = []
        for cmd in comandos:
            comando_teste = bytes(f'{cmd}{TERMINATOR}', ENCODING)
            self.ser.write(comando_teste)
            resposta = self.ser.readline().decode().strip()
            respostas.append((cmd, resposta))
        print(respostas)        

lcr = LCRConnection('COM5')
lcr.enviar_comandos(["TRIG:SOUR MAN", "DISP:PAGE MSET"])
lcr.close()