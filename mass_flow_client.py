import os
import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11111

    print('Linha de comando, "Mass Flow Controller", v0.01.')
    print('para ajuda, digite "?"; para fechar a linha de comando digite "sair".')
    
    client_socket.connect((host, port))
    while True:
        data_to_send = input("$: ")
        if data_to_send.lower().strip() == 'sair':
            break

        elif data_to_send.lower().strip() == '?':
            print('')
            print('Comandos disponíveis:')
            print(' - editar: abre o arquivo de parâmetros com o editor de texto padrão...')
            print(' - executar: inicia a execução da rotina definida...')
            print(' - parar: interrompe execução da rotina...')
            print(' - sair: finaliza a linha de comando...')
            print('')


        elif data_to_send.lower().strip() == 'editar':
            os.system('gedit /home/danielc/Documentos/Devel/GitHub/mass_flow_unit/parametros.json')

        client_socket.send(data_to_send.encode())
        data = client_socket.recv(5000).decode().strip()
        print(data)
    
    client_socket.close()


def send_message(msg):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11111
    client_socket.connect((host, port))
    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode().strip()
    client_socket.close()
    return data
    

if __name__ == "__main__":
    start_client()
