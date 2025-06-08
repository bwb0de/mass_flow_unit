import json
import time

from nucleo.globals.paths import lcr_config
from nucleo.devices.lcr_unit import LCRUnit

lcr_unit = None
with open(lcr_config) as arquivo_lcr_config:
    definicoes = json.loads(arquivo_lcr_config.read())
    if len(definicoes) == 1:
        definicoes = definicoes[0]
        lcr_unit = LCRUnit(definicoes['porta'], definicoes['taxa_de_transmissao'], definicoes['parity'], definicoes['stopbits'], definicoes['bytesize'], definicoes['timeout'], definicoes['numero_medidas'])

print(lcr_unit)
for _ in range(3):
    print(lcr_unit.ler_medidas())
lcr_unit.desconectar()
print("")
