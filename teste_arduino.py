import time
import json

from nucleo.paths import arduino_config
from nucleo.devices.arduino_unit import ArduinoUnit

arduino_unit = None
with open(arduino_config) as arquivo_arduino_config:
    definicoes = json.loads(arquivo_arduino_config.read())
    for unit in definicoes:
        arduino_unit = ArduinoUnit(unit['porta'], unit['taxa_de_transmissao'], unit['modelo'], unit['nome'], unit['tempo_espera'])


print(arduino_unit)
arduino_unit.enviar_comando('r')
for _ in range(1000):
    arduino_unit.enviar_comando('p')
    print(f'S{arduino_unit.ler_resposta()}')
    time.sleep(1)
arduino_unit.enviar_comando('r')
arduino_unit.desconectar()
print("")

