import os
import time
import socket
import json


class SistematizadorStatus:
    def __init__(self) -> None:
        self.n = 0
        self.uv = None
        self.mv = None
        self.mv2 = None
        self.valores = []

    def receber_valor(self, valor):
        self.uv = valor
        self.valores.append(valor)
        self.n += 1
        if self.n == 1:
            self.mv = self.uv
        else:
            self.mv = ((self.mv * (self.n - 1)) + self.uv) / self.n
            self.mv2 = sum(self.valores) / self.n

    def retornar_valores(self):
        return self.n, self.uv, self.mv

    def retornar_valores_adicionais(self):
        return self.mv2, self.valores


def tela_de_informacoes(n, uv, mv, mv2, valores):
    null = os.system('cls')
    print(f"Servidor de status MassFlow")
    print(f' -> último valor recebido: {uv}')
    print(f' -> media dos valores recebidos: {mv}')
    print(f' -> media dos valores recebidos[2]: {mv2}')
    print(f' -> quantidade total de valores recebidos: {n}')
    print(f' -> valores: {valores}')



def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11112
    
    client_socket.connect((host, port))
    while True:
        data_to_send = input("exp_view ··> ")
        if data_to_send.lower().strip() == 'sair':
            break

        try:
            comando, variavel, valor = data_to_send.split('::')
        except:
            comando, variavel = data_to_send.split('::')

        if comando.lower().strip() == 'set':
            client_socket.send(data_to_send.encode())

        elif comando.lower().strip() == 'get':
            client_socket.send(data_to_send.encode())
            data = client_socket.recv(1024).decode().strip()
            print(data)
    
    client_socket.close()
    

if __name__ == "__main__":
    start_client()






