import socket


ipvh = {'sensor_loop': 
        str([
                  {"S0": {"primary": "0.0", "secondary": "0.0"} },
                  {"S1": {"primary": "0.0", "secondary": "0.0"} },
                  {"S2": {"primary": "0.0", "secondary": "0.0"} },
                  {"S3": {"primary": "0.0", "secondary": "0.0"} },
                  {"S4": {"primary": "0.0", "secondary": "0.0"} },
                  {"S5": {"primary": "0.0", "secondary": "0.0"} },
                  {"S6": {"primary": "0.0", "secondary": "0.0"} },
                  {"S7": {"primary": "0.0", "secondary": "0.0"} }
            ]),
        'sensor_corrente': ""
        }

def start_server(mostrar_dados_recebido=True):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11112
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor IPVH escutando em {host}:{port}")
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

        instrucoes = data.strip().split(' ')

        if instrucoes[0] == "set":
            variavel = instrucoes[1]
            valor = instrucoes[2]
            ipvh[variavel] = valor
            client_socket.send(" ".encode())
            
        elif instrucoes[0] == "get":
            
            valor = ipvh[instrucoes[1]]
            client_socket.send(valor.encode())


def set_value(key, value):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11112
    client_socket.connect((host, port))
    data_to_send = f'set {key} {value}'
    client_socket.send(data_to_send.encode())
    data = client_socket.recv(1024).decode().strip()
    client_socket.close()


def get_value(key):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11112
    client_socket.connect((host, port))
    data_to_send = f'get {key}'
    client_socket.send(data_to_send.encode())
    data = client_socket.recv(1024).decode().strip()
    client_socket.close()
    return data


if __name__ == "__main__":
    start_server()






