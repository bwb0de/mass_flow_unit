import time
import socket

from mass_flow_unit import MassFlowUnitTest
from orquestrador_mass_flow_v2 import Orquestrador

taxa_de_transmissao = 9600

mu1 = MassFlowUnitTest('COM3', 9600, 100, 'produto')
mu2 = MassFlowUnitTest('COM4', 9600, 200, 'Ar')
mu3 = MassFlowUnitTest('COM5', 9600, 200, 'Ar')


o1 = Orquestrador([mu1, mu2, mu3])

lista_fluxo_nao_ar_tempo = [
    (0,10),
    (6,10),
    (0,10),
    (12,10),
    (0,10),
    (24,10),
    (0,10),
    (36,10),
    (0,10),
    (48,10),
]

o1.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)

mostrar_dados_recebidos = True

def start_server(mostrar_dados_recebido=True):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11111
    server_socket.bind((host, port))
    server_socket.listen(5)
    client_socket, addr = server_socket.accept()
    print(f"Servidor MassFlow escutando em {host}:{port}")

    with client_socket:
        print(f"Conectado a {addr}")
        
        while True:
            handle_client(client_socket)

        


def handle_client(client_socket) -> str:
    global mostrar_dados_recebidos

    data = client_socket.recv(1024).decode().strip()
    
    if mostrar_dados_recebidos: print(f"recebido ··> {data}")

    comando = data.strip()

    if comando == "run":
        o1.executar_rotina()
        
    elif comando == "check":
        o1.status_das_rotinas_em_execucao()

    elif comando == "stop":
        o1.interromper()



        

if __name__ == "__main__":
    start_server()






