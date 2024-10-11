import time
import serial
from nucleo.devices.lcr_unit import LCRUnit

porta_de_conexao = 'COM5'

lcr = LCRUnit('COM5', 9600)
print(lcr.ler_medidas())
lcr.desconectar()
