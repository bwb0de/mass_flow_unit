import time
import serial

class LCRConnection:
  def __init__(self, port):
    self.name = "LCR"
    self.ser = None
    self.port = port
    self.baudrate = 9600
    self.parity = 'N'
    self.stopbits = 1
    self.bytesize = 8
    self.timeout = 1
    self.ser_parameters = {
      "url": self.port,
      "baudrate": self.baudrate,
      "stopbits": self.stopbits,
      "bytesize": self.bytesize,
      "timeout": self.timeout,
    }

    self.connect()

  def connect(self, wait=None):
    self.ser = serial.serial_for_url(**self.ser_parameters, do_not_open=False)
    #self.ser.open()

  def close(self):
    self.ser.close()

  def enviar_comandos(self, comandos: list):
    print(comandos)
    try:
      respostas = []
      for cmd in comandos:
        comando_teste = bytes(f'{cmd}\r\n', 'utf-8')  # Add newline for termination
        self.ser.write(comando_teste)

        # Read data until termination character (check LCR manual)
        resposta = b''
        #while True:
        data = self.ser.read(3)  # Read one byte at a time
        if data == b'\n':  # Replace with actual termination character
          break
        resposta += data

        respostas.append((cmd, resposta.decode('ascii')))  # Assuming ASCII encoding

        print(respostas)
    except serial.SerialException as e:
      print(f"Erro ao conectar na porta serial: {e}")

lcr = LCRConnection('COM5')
lcr.enviar_comandos(["TRIG:SOUR MAN", 'DISP:PAGE?', 'FREQ?'])
lcr.close()