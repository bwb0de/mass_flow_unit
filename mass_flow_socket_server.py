import time
import socket
import json

from mass_flow_unit import MassFlowUnitTest
#from orquestrador_mass_flow_v3 import Orquestrador
from orquestrador_mass_flow_v2 import Orquestrador

taxa_de_transmissao = 9600

def inicializar_orquestrador():
    mu1 = MassFlowUnitTest('COM3', 9600, 100, 'produto')
    mu2 = MassFlowUnitTest('COM4', 9600, 200, 'Ar')
    mu3 = MassFlowUnitTest('COM5', 9600, 200, 'Ar')
    o1 = Orquestrador([mu1, mu2, mu3])
    return o1


mostrar_dados_recebidos = True

def start_server(mostrar_dados_recebido=True):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11111
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor MassFlow escutando em {host}:{port}")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão recebida de {addr}")
        handle_client(client_socket)
        


def handle_client(client_socket) -> str:
    global mostrar_dados_recebidos
    while True:
        data = client_socket.recv(1024).decode().strip()
        if not data:
            break
        if data == 'exit': continue
        if mostrar_dados_recebidos: print(f"··> {data}")

        comando = data.strip()

        if comando == "run":
            lista_fluxo_nao_ar_tempo = None
            with open('parametros.json', 'r') as arquivo_parametros:
                lista_fluxo_nao_ar_tempo = json.loads(arquivo_parametros.read())
            o1 = inicializar_orquestrador()
            o1.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
            o1.executar_rotina()
            client_socket.send("executando procedimento...".encode())
            
        elif comando == "check":
            data_to_send = str(o1.status_das_rotinas_em_execucao())
            client_socket.send(data_to_send.encode())

        elif comando == "stop":
            o1.interromper()
            client_socket.send("procedimento interrompido...".encode())


        

if __name__ == "__main__":
    start_server()






