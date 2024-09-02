import socket

ipvh = {}

def start_server(mostrar_dados_recebido=True):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11112
    server_socket.bind((host, port))
    server_socket.listen(5)
    while True:
        client_socket, addr = server_socket.accept()
        handle_client(client_socket, server_socket)

            
        

def handle_client(client_socket, server_socket):
    dados_recebidos = client_socket.recv(1024).decode().strip()
    print(dados_recebidos)
    if not dados_recebidos:
        return
    
    dados_em_processamento = dados_recebidos.strip()

    valor = None
    
    try:
        comando, variavel, valor = dados_em_processamento.split('::')
    except:
        comando, variavel = dados_em_processamento.split('::')

    print(comando, variavel, valor)

    if comando == 'set':
        ipvh[variavel] = valor

    elif comando == 'get':
        server_socket.send(ipvh[variavel].encode())

    




if __name__ == "__main__":
    start_server()








