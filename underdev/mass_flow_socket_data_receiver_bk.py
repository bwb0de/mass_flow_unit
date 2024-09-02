import socket

ipvh = {}

def start_server(mostrar_dados_recebido=True):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = 11112
        server_socket.bind((host, port))
        server_socket.listen(5)
        while True:
                client_socket, addr = server_socket.accept()
                handle_client(client_socket)
    except KeyboardInterrupt:
        with open('dados_recebidos', 'w') as dados_recebidos:
            dados_recebidos.write(str(1))

        

def handle_client(client_socket) -> str:
    dados_recebidos = client_socket.recv(1024).decode().strip()
    if not dados_recebidos:
        return

    dados_em_processamento = dados_recebidos.strip()
    dados_convertidos = dados_em_processamento
    with open('dados_recebidos', 'w') as dados_recebidos:
        dados_recebidos.write(str(dados_convertidos))



if __name__ == "__main__":
    start_server()








