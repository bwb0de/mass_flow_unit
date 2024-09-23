import json

from .devices.arduino_unit import ArduinoUnit, ArduinoUnitTest
from .arduino_orquestrator_parallel import Orquestrador

from .paths import arduino_config


def inicializar_orquestrador_arduino():
    arduino_units = []
    with open(arduino_config) as arquivo_arduino_config:
        definicoes = json.loads(arquivo_arduino_config.read())
        for unit in definicoes:
            arduino_unit = ArduinoUnitTest(unit['porta'], unit['taxa_de_transmissao'], unit['modelo'], unit['nome'])
            #arduino_unit = ArduinoUnit(unit['porta'], unit['taxa_de_transmissao'], unit['modelo'], unit['nome'])
            arduino_units.append(arduino_unit)

    o1 = Orquestrador(arduino_units)
    return o1



