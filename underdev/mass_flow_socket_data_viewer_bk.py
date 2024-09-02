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


def start_server(mostrar_dados_recebido=True):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11112
    server_socket.bind((host, port))
    server_socket.listen(5)
    sistematizador = SistematizadorStatus()
    n, uv, mv = sistematizador.retornar_valores()
    mv2, valores = sistematizador.retornar_valores_adicionais()
    tela_de_informacoes(n, uv, mv, mv2, valores)
    while True:
        client_socket, addr = server_socket.accept()
        dados_convertidos = int(handle_client(client_socket))
        sistematizador.receber_valor(dados_convertidos)
        n, uv, mv = sistematizador.retornar_valores()
        mv2, valores = sistematizador.retornar_valores_adicionais()
        tela_de_informacoes(n, uv, mv, mv2, valores)
        

def handle_client(client_socket) -> str:
    while True:
        dados_recebidos = client_socket.recv(1024).decode().strip()
        if not dados_recebidos:
            break

        dados_em_processamento = dados_recebidos.strip()
        dados_convertidos = dados_em_processamento
        return dados_convertidos


        

if __name__ == "__main__":
    start_server()






