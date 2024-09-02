import time
import socket
import random

def enviar_dados(dados):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11112
    client_socket.connect((host, port))
    client_socket.send(str(dados).encode())
    client_socket.close()
    

if __name__ == "__main__":
    for n in range(0,10000000):
        enviar_dados(random.randint(2,100))
        time.sleep(0.25)
