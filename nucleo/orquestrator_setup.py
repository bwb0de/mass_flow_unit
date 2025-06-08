import json

from .devices.mass_flow_unit import MassFlowUnit, MassFlowUnitTest
from .devices.lcr_unit import LCRUnit, LCRUnitTest
from .devices.arduino_unit import ArduinoUnit, ArduinoUnitTest

from .orquestrator_parallel import Orquestrador

from .globals.paths import mass_flow_config
from .globals.paths import arduino_config
from .globals.paths import lcr_config

from .globals import logger

EXP_MAX_FLOW=400

def inicializar_orquestrador_mass_flow(etapas_microciclo):
    logger.escrever("[ORQUESTRADOR] Criando instâncias a partir dos arquivos de configuração...") 
    mass_flow_units = []
    with open(mass_flow_config) as arquivo_mass_flow_config:
        definicoes = json.loads(arquivo_mass_flow_config.read())
        for unit in definicoes:
            mass_flow_unit = MassFlowUnit(unit['porta'], unit['taxa_de_transmissao'], unit['fluxo_maximo'], unit['conteudo_fluxo'])
            mass_flow_units.append(mass_flow_unit)
            mass_flow_unit.etapas_microciclo = etapas_microciclo

    logger.escrever(f"[ORQUESTRADOR] Crianda {len(mass_flow_units)} instâncias MassFlow com flow máximo de {EXP_MAX_FLOW}...") 
    print(mass_flow_units)

    arduino_unit = None
    with open(arduino_config) as arquivo_arduino_config:
        definicoes = json.loads(arquivo_arduino_config.read())
        for unit in definicoes:
            arduino_unit = ArduinoUnit(unit['porta'], unit['taxa_de_transmissao'], unit['modelo'], unit['nome'], unit['tempo_espera'])

    logger.escrever(f"[ORQUESTRADOR] Crianda instância Arduino...") 
    print(arduino_unit)
    arduino_unit.desconectar()

    lcr_unit = None
    with open(lcr_config) as arquivo_lcr_config:
        definicoes = json.loads(arquivo_lcr_config.read())
        if len(definicoes) == 1:
            definicoes = definicoes[0]
            lcr_unit = LCRUnit(definicoes['porta'], definicoes['taxa_de_transmissao'], definicoes['parity'], definicoes['stopbits'], definicoes['bytesize'], definicoes['timeout'], definicoes['numero_medidas'])

    logger.escrever(f"[ORQUESTRADOR] Crianda instância LCR...") 
    print(lcr_unit)
    lcr_unit.desconectar()

    logger.escrever(f"[ORQUESTRADOR] Vinculando instâncias ao orquestrador...") 
    o1 = Orquestrador(mass_flow_units, exp_max_flow=EXP_MAX_FLOW)
    o1.adicionar_lcr(lcr_unit)
    o1.adicionar_arduinos(arduino_unit)

    logger.escrever(f"[ORQUESTRADOR] Devolvendo intancia orquestradora ao flask...") 
    return o1




def inicializar_orquestrador_mass_flow_teste():
    mass_flow_units = []
    with open(mass_flow_config) as arquivo_mass_flow_config:
        definicoes = json.loads(arquivo_mass_flow_config.read())
        for unit in definicoes:
            mass_flow_unit = MassFlowUnitTest(unit['porta'], unit['taxa_de_transmissao'], unit['fluxo_maximo'], unit['conteudo_fluxo'])
            mass_flow_units.append(mass_flow_unit)

    arduino_unit = None
    with open(arduino_config) as arquivo_arduino_config:
        definicoes = json.loads(arquivo_arduino_config.read())
        for unit in definicoes:
            arduino_unit = ArduinoUnitTest(unit['porta'], unit['taxa_de_transmissao'], unit['modelo'], unit['nome'], unit['tempo_espera'])

    lcr_unit = None
    with open(lcr_config) as arquivo_lcr_config:
        definicoes = json.loads(arquivo_lcr_config.read())
        print(definicoes)
        if len(definicoes) == 1:
            for unit in definicoes:
                lcr_unit = LCRUnitTest(unit['porta'], unit['taxa_de_transmissao'], numero_medidas=unit['numero_medidas'])

    o1 = Orquestrador(mass_flow_units, exp_max_flow=EXP_MAX_FLOW)
    o1.adicionar_lcr(lcr_unit)
    o1.adicionar_arduinos(arduino_unit)
    
    return o1

