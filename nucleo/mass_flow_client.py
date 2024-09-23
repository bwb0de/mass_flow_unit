import sys
import os

import requests

MASS_FLOW_SERVER_HOST = '127.0.0.1'
MASS_FLOW_SERVER_PORT = '5000'

from .paths import parametros

def request_api_addr(url, params={}):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response
    return "Erro ao acessar o endereço solicitado..."


def start_client():
    print('Linha de comando, "Mass Flow Controller", v0.01.')
    print('para ajuda, digite "?"; para fechar a linha de comando digite "sair".')
    
    base_api_addr = f'http://{MASS_FLOW_SERVER_HOST}:{MASS_FLOW_SERVER_PORT}/'

    while True:
        data_to_send = input("$: ")
        if data_to_send.lower().strip() == 'sair':
            break

        elif data_to_send.lower().strip() == '?':
            print('')
            print('Comandos disponíveis:')
            print(' - edit: abre o arquivo de parâmetros com o editor de texto padrão...')
            print(' - run: inicia a execução da rotina definida...')
            print(' - stop: interrompe execução da rotina...')
            print(' - check: retorna histórico da rotina em execução...')
            print(' - sair: finaliza a linha de comando...')
            print('')
            continue

        elif data_to_send.lower().strip() == 'edit':
            if sys.platform == 'win32':
                os.system(f'notepad {parametros}')
            else:
                os.system(f'gedit {parametros}')
            continue

        elif data_to_send.lower().strip() == 'run':
            request_addr = base_api_addr + 'api/run'
            data = request_api_addr(request_addr).json()

        elif data_to_send.lower().strip() == 'stop':
            request_addr = base_api_addr + 'api/stop'
            data = request_api_addr(request_addr).json()

        elif data_to_send.lower().strip() == 'check':
            request_addr = base_api_addr + 'api/check'
            data = request_api_addr(request_addr).json()
            
        print(data)

    

if __name__ == "__main__":
    start_client()
