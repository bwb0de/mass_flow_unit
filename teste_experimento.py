import time
import os
import json
from multiprocessing import freeze_support

from nucleo.orquestrator_setup import inicializar_orquestrador_mass_flow
from nucleo.mass_flow_info_reader import update_info
from nucleo.globals.paths import root, parametros_mass_flow, arduino_config, lcr_config

if __name__ == '__main__':
    freeze_support()
    lista_fluxo_nao_ar_tempo = None
    with open(parametros_mass_flow, 'r') as arquivo_parametros:
        lista_fluxo_nao_ar_tempo = json.loads(arquivo_parametros.read())

    print(f'Tempo: {lista_fluxo_nao_ar_tempo}s')
    try: os.system(f'python {root}\\nucleo\\ipvh_srv.py&')
    except: pass
    orq_mass_flow = inicializar_orquestrador_mass_flow()
    orq_mass_flow.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
    orq_mass_flow.executar_rotina()
    

