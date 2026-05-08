
import traceback
from serial.threaded import LineReader, ReaderThread

import time
import serial

porta_de_conexao = 'COM5'

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
        #self.thread = ReaderThread(self.ser, SerialReaderProtocolLine)
        #self.thread.start()
        #self.transport, self.protocol = self.thread.connect()        

    def close(self):
        self.ser.close()

    def enviar_comandos(self, comandos:list):
        print(comandos)
        try:
            respostas = []
            for cmd in comandos:
                comando_teste = bytes(f'{cmd}\n', 'utf-8')
                self.ser.write(comando_teste)
                #self.ser.flush()
                time.sleep(0.5)
                resposta = self.ser.readline().decode().strip()
                respostas.append((cmd, resposta))
            print(respostas)        
        except serial.SerialException as e:
            print(f"Erro ao conectar na porta serial: {e}")    



class SerialReaderProtocolLine(LineReader):
    """read lines of data"""

    TERMINATOR = b"\n"
    ENCODING = "utf-8"

    def __init__(self):
        super(SerialReaderProtocolLine, self).__init__()
        self.received_lines = []

    def connection_made(self, transport):
        """Called when reader thread is started"""
        super(SerialReaderProtocolLine, self).connection_made(transport)
        self.transport.serial.reset_input_buffer()

    def handle_line(self, line):
        """New line waiting to be processed"""
        # line = str(int(round(time.time() * 1000))) + ',' + line # add timestamp
        self.received_lines.append(line)

    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        #cprint.warn("Serial port closed")



#lcr.protocol.write_line("TRIG:SOUR MAN")
#print(lcr.protocol.received_lines)
#lcr.protocol.write_line("DISP:PAGE?")
#print(lcr.protocol.received_lines)
#lcr.protocol.write_line("FREQ?")
#print(lcr.protocol.received_lines)
#print(dir(lcr.protocol))
#lcr.transport.serial.flush()

lcr = LCRConnection('COM5')
lcr.enviar_comandos([""trig:sour bus;*trg"])
lcr.close()