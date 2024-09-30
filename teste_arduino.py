import time
import serial
from nucleo.devices.arduino_unit import ArduinoUnit

porta_de_conexao = 'COM10'

arduino = ArduinoUnit('COM10', 9600)
arduino.desconectar()
