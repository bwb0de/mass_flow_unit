import time
import json

from nucleo.globals.paths import mass_flow_config
from nucleo.devices.mass_flow_unit import MassFlowUnit


mass_flow_units = []
with open(mass_flow_config) as arquivo_mass_flow_config:
    definicoes = json.loads(arquivo_mass_flow_config.read())
    for unit in definicoes:
        mass_flow_unit = MassFlowUnit(unit['porta'], unit['taxa_de_transmissao'], unit['fluxo_maximo'], unit['conteudo_fluxo'])
        mass_flow_units.append(mass_flow_unit)

for mass_unit in mass_flow_units:
    print(mass_unit)
    print(mass_unit.fechar_fluxo())

print("")

