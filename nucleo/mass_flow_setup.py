import json

from .devices.mass_flow_unit import MassFlowUnit, MassFlowUnitTest
from .mass_flow_orquestrator_parallel import Orquestrador

from .paths import mass_flow_config

def inicializar_orquestrador_mass_flow():
    mass_flow_units = []
    with open(mass_flow_config) as arquivo_mass_flow_config:
        definicoes = json.loads(arquivo_mass_flow_config.read())
        for unit in definicoes:
            mass_flow_unit = MassFlowUnitTest(unit['porta'], unit['taxa_de_transmissao'], unit['fluxo_maximo'], unit['conteudo_fluxo'])
            #mass_flow_unit = MassFlowUnit(unit['porta'], unit['taxa_de_transmissao'], unit['fluxo_maximo'], unit['conteudo_fluxo'])
            mass_flow_units.append(mass_flow_unit)

    o1 = Orquestrador(mass_flow_units, exp_max_flow=400)
    return o1



