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


    def enviar_comando(self, comando):
        comando_teste = bytes(comando, ENCODING) + b'\x10'
        self.ser.write(comando_teste)
        self.ser.flush()
        time.sleep(4)
        resposta = self.ser.readline().decode().strip()
        print(resposta)

    def ler(self):
        resposta = self.ser.readline().decode().strip()
        print(resposta)




lcr = LCRConnection('COM5')
#"TRIG:SOUR MAN"

"APER SLOW"
"TRIG:SOUR INT"

for msg in ["APER SLOW", "TRIG:SOUR INT"]:
#for msg in ["TRIG:SOUR BUS", "VOLT?", "DISP:PAGE?"]:
    #lcr.enviar_comando(msg)
    lcr.ler()


lcr.close()
