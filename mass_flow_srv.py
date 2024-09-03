import os
import socket
import json

from mass_flow_unit import MassFlowUnit, MassFlowUnitTest
from mass_flow_orquestrator_parallel import Orquestrador

from ipvh_srv import get_value

taxa_de_transmissao = 9600

MASS_FLOW_HOST = '127.0.0.1'
MASS_FLOW_PORT = 11111

def inicializar_orquestrador():
    mass_flow_unit1 = MassFlowUnitTest('COM5', taxa_de_transmissao, 200, 'Ar')
    mass_flow_unit2 = MassFlowUnitTest('COM6', taxa_de_transmissao, 200, 'Ar')
    mass_flow_unit3 = MassFlowUnitTest('COM7', taxa_de_transmissao, 100, 'produto')
    mass_flow_unit4 = MassFlowUnitTest('COM8', taxa_de_transmissao, 100, 'produto')    
    #mass_flow_unit1 = MassFlowUnit('COM5', taxa_de_transmissao)
    #mass_flow_unit2 = MassFlowUnit('COM6', taxa_de_transmissao)
    #mass_flow_unit3 = MassFlowUnit('COM7', taxa_de_transmissao)
    #mass_flow_unit4 = MassFlowUnit('COM8', taxa_de_transmissao)
    o1 = Orquestrador([mass_flow_unit1, mass_flow_unit2, mass_flow_unit3, mass_flow_unit4], exp_max_flow=400)
    return o1


mostrar_dados_recebidos = True

def start_server(mostrar_dados_recebido=True):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = MASS_FLOW_HOST
    port = MASS_FLOW_PORT
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor MassFlow escutando em {host}:{port}")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão recebida de {addr}")
        handle_client(client_socket)
        


def handle_client(client_socket) -> str:
    global mostrar_dados_recebidos
    em_execucao = False
    o1 = inicializar_orquestrador()

    while True:
        data = client_socket.recv(1024).decode().strip()
        if not data:
            break

        comando = data.strip()

        if comando == "executar":
            lista_fluxo_nao_ar_tempo = None
            em_execucao = True
            with open('parametros.json', 'r') as arquivo_parametros:
                lista_fluxo_nao_ar_tempo = json.loads(arquivo_parametros.read())
            o1 = inicializar_orquestrador()
            o1.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)
            o1.executar_rotina()
            client_socket.send("Procedimento iniciado...".encode())
            
        elif comando == "checar execução":
            if not em_execucao:
                client_socket.send("Não há o que checar, procedimentos não estão em execução...".encode())
                continue
            
            data_to_send = os.linesep.join(o1.status_das_rotinas_em_execucao())
            client_socket.send(data_to_send.encode())

        elif comando == "equipamento":
            data_to_send = "  "
            for unit_info in o1.status_equipamentos():
                for k, v in unit_info.items():
                    data_to_send += f'  {k}: {v}' + os.linesep
                data_to_send += os.linesep
            client_socket.send(data_to_send.encode())

        elif comando == "parar":
            o1.interromper()
            em_execucao = False
            client_socket.send("Procedimento interrompido...".encode())

        else:
            client_socket.send(" ".encode())


        

if __name__ == "__main__":
    start_server()






