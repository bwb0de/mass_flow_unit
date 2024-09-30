import json

from .devices.mass_flow_unit import MassFlowUnit, MassFlowUnitTest
from .devices.lcr_unit import LCRUnit
from .devices.arduino_unit import ArduinoUnit
from .orquestrator_parallel import Orquestrador

from .paths import mass_flow_config
from .paths import arduino_config
from .paths import lcr_config

def inicializar_orquestrador_mass_flow():
    mass_flow_units = []
    with open(mass_flow_config) as arquivo_mass_flow_config:
        definicoes = json.loads(arquivo_mass_flow_config.read())
        for unit in definicoes:
            #mass_flow_unit = MassFlowUnitTest(unit['porta'], unit['taxa_de_transmissao'], unit['fluxo_maximo'], unit['conteudo_fluxo'])
            mass_flow_unit = MassFlowUnit(unit['porta'], unit['taxa_de_transmissao'], unit['fluxo_maximo'], unit['conteudo_fluxo'])
            mass_flow_units.append(mass_flow_unit)

    arduino_unit = None
    with open(arduino_config) as arquivo_arduino_config:
        definicoes = json.loads(arquivo_arduino_config.read())
        for unit in definicoes:
            #arduino_unit = ArduinoUnitTest(unit['porta'], unit['taxa_de_transmissao'], unit['modelo'], unit['nome'])
            arduino_unit = ArduinoUnit(unit['porta'], unit['taxa_de_transmissao'], unit['modelo'], unit['nome'])

    lcr_unit = None
    with open(lcr_config) as arquivo_lcr_config:
        definicoes = json.loads(arquivo_lcr_config.read())
        if len(definicoes) == 1:
            #lcr_unit = LCRUnitTest(unit['porta'], unit['taxa_de_transmissao'], unit['modelo'], unit['nome'])
            lcr_unit = LCRUnit(unit['porta'], unit['taxa_de_transmissao'], unit['parity'], unit['stopbits'], unit['bytesize'], unit['timeout'])

    o1 = Orquestrador(mass_flow_units, exp_max_flow=400)
    o1.adicionar_lcr(lcr_unit)
    o1.adicionar_arduinos(arduino_unit)
    
    return o1



