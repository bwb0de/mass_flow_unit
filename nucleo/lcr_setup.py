import json

from .devices.lcr_unit import LCRUnit, LCRUnitTest

from .paths import lcr_config

def inicializar_lcr():
    with open(lcr_config) as arquivo_lcr_config:
        definicoes = json.loads(arquivo_lcr_config.read())
        if len(definicoes) == 1:
            lcr_unit = LCRUnitTest(unit['porta'], unit['taxa_de_transmissao'], unit['modelo'], unit['nome'])
            #lcr_unit = LCRUnit(unit['porta'], unit['taxa_de_transmissao'], unit['modelo'], unit['nome'])
            return lcr_unit

        for unit in definicoes:
            pass

    return



