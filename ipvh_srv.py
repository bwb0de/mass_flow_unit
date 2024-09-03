import time
import socket
import json


IPVH_HOST = '127.0.0.1'
IPVH_PORT = 11112

def start_server(mostrar_dados_recebido=True):
    ipvh = {}
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = IPVH_HOST
    port = IPVH_PORT
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor IPVH escutando em {host}:{port}")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão recebida de {addr}")
        ipvh = handle_client(client_socket, ipvh)
        


def handle_client(client_socket, ipvh) -> str:
    while True:
        data = client_socket.recv(1024).decode().strip()
        if not data:
            break

        instrucoes = data.strip().split(' ')

        if instrucoes[0] == "set":
            variavel = instrucoes[1]
            valor = instrucoes[2]
            ipvh[variavel] = valor
            client_socket.send(" ".encode())
            
        elif instrucoes[0] == "get":
            valor = ipvh[instrucoes[1]]
            client_socket.send(valor.encode())
    
    return ipvh


def set_value(key, value):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = IPVH_HOST
    port = IPVH_PORT
    client_socket.connect((host, port))
    data_to_send = f'set {key} {value}'
    client_socket.send(data_to_send.encode())
    data = client_socket.recv(1024).decode().strip()
    client_socket.close()


def set_values(keys: list, values: list):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = IPVH_HOST
    port = IPVH_PORT
    client_socket.connect((host, port))
    for key, value in zip(keys, values):
        data_to_send = f'set {key} {value}'
        client_socket.send(data_to_send.encode())
        _ = client_socket.recv(1024).decode().strip()
    client_socket.close()


def get_value(key):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = IPVH_HOST
    port = IPVH_PORT
    client_socket.connect((host, port))
    data_to_send = f'get {key}'
    client_socket.send(data_to_send.encode())
    data = client_socket.recv(1024).decode().strip()
    client_socket.close()
    return data


def get_values(keys: list):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = IPVH_HOST
    port = IPVH_PORT
    client_socket.connect((host, port))
    output = {}
    for key in keys:
        data_to_send = f'get {key}'
        client_socket.send(data_to_send.encode())
        data = client_socket.recv(1024).decode().strip()
        output[key] = data
    client_socket.close()
    return output


if __name__ == "__main__":
    start_server()






