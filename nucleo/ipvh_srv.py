import os
import socket
import json
import datetime
import time

from pprint import pprint

pasta_dados_experimento = "C:\\Users\\Mauro\\Desktop\\Dados Experimentos"
arquivo_dados_experimento = "C:\\Users\\Mauro\\Documents\\Devel\\mass_flow_unit\\config\\experimento.json"

production_root = 'C:\\Users\\Mauro\\Documents\\Devel\\mass_flow_unit'
development_root1 = 'C:\\Users\\Daniel Cruz\\Documents\\Devel\\python\\mass_flow_unit'
development_root2 = '/home/danielc/Documentos/Devel/GitHub/mass_flow_unit'
root = production_root

experimento_ultimos_parametros_windows = f"{root}\\config\\experimento_ultimos_parametros_tempo.txt"
experimento_ultimos_parametros_linux = f"{root}/config/experimento_ultimos_parametros_tempo.txt"
experimento_ultimos_parametros = experimento_ultimos_parametros_windows

diretorio_corrente_dados = None

contador_mensagens_recebidas = 0

ipvh = {'sensor_loop': 
        {
            "S1": {"primary": [], "secondary": []},
            "S2": {"primary": [], "secondary": []},
            "S3": {"primary": [], "secondary": []},
            "S4": {"primary": [], "secondary": []},
            "S5": {"primary": [], "secondary": []},
            "S6": {"primary": [], "secondary": []},
            "S7": {"primary": [], "secondary": []},
            "S8": {"primary": [], "secondary": []}
        },
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
        print(f"conn nfo: {addr} => ", end="")
        handle_client(diretorio_corrente_dados, client_socket)
        


def handle_client(diretorio_corrente_dados, client_socket) -> str:
    global mostrar_dados_recebidos
    global contador_mensagens_recebidas
    contador_mensagens_recebidas += 1

    while True:
        data = client_socket.recv(1024).decode().strip()
        if not data:
            break
        
        if data == 'exit':
            exit()

        elif data == '@':
            if contador_mensagens_recebidas > 6:
                contador_mensagens_recebidas = 0
                for sensor in ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']:
                    ipvh['sensor_loop'][sensor]["primary"].append('@')
                    ipvh['sensor_loop'][sensor]["secondary"].append('@')

            client_socket.send(" ".encode())

        instrucoes = data.strip().split(' ')

        if instrucoes[0] == "set":
            variavel = instrucoes[1]
            valor = instrucoes[2]
            ipvh[variavel] = valor
            print(variavel, valor)
            sensor, dados = valor.split("=>")
            primario, secundario = dados[1:-2].split(":::")
            primario, secundario = float(primario), float(secundario)
            try:
                ipvh['sensor_loop'][sensor]["primary"].append(primario)
                ipvh['sensor_loop'][sensor]["secondary"].append(secundario)
            except KeyError:
                pass

            with open(f"{diretorio_corrente_dados}\\dados_sensores.json", 'w') as arquivo_dados_sensores:
               json.dump(ipvh, arquivo_dados_sensores, indent=4)

            client_socket.send(" ".encode())
            
        elif instrucoes[0] == "get":
            valor = ipvh[instrucoes[1]]
            client_socket.send(valor.encode())

        


def send_command(command):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11112
    client_socket.connect((host, port))
    data_to_send = f'{command}'
    client_socket.send(data_to_send.encode())
    data = client_socket.recv(1024).decode().strip()
    client_socket.close()


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


def mudar_parametros_experimento():
    print(os.linesep)
    print('Atualizando dados da experiência...')
    time.sleep(1)
    with open(arquivo_dados_experimento, 'r') as dados_experimento:
        info = dados_experimento.read()
        info = json.loads(info)
        print(os.linesep)
        pprint(info)
        print(os.linesep)
    
    nome_pesquisador = info[0]["pesquisador"]
    nome_substancia = info[0]["substancia"]
    ano, mes, dia, hora, minuto = datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day, datetime.datetime.today().hour, datetime.datetime.today().minute
    os.chdir(pasta_dados_experimento)
    try: os.mkdir(nome_pesquisador)
    except: pass
    os.chdir(nome_pesquisador)
    try: os.mkdir(nome_substancia)
    except: pass
    os.chdir(nome_substancia)
    try: os.mkdir(f"{ano}_{mes}_{dia}-{hora}_{minuto}")
    except: pass
    os.chdir(f"{ano}_{mes}_{dia}-{hora}_{minuto}")
    global diretorio_corrente_dados
    diretorio_corrente_dados = os.getcwd()

    with open(experimento_ultimos_parametros, 'w') as dados_experimento_ultimos_par:
        dados_experimento_ultimos_par.write(diretorio_corrente_dados)

    with open("info_experimento_sensores.txt", 'w') as arquivo_sensores:
        arquivo_sensores.write(f"Pesquisador: {nome_pesquisador}\n")
        arquivo_sensores.write(f"Substancia: {nome_substancia}\n")
        arquivo_sensores.write(f"Sensor 1: {info[0]["s1"]}\n")
        arquivo_sensores.write(f"Sensor 2: {info[0]["s2"]}\n")
        arquivo_sensores.write(f"Sensor 3: {info[0]["s3"]}\n")
        arquivo_sensores.write(f"Sensor 4: {info[0]["s4"]}\n")
        arquivo_sensores.write(f"Sensor 5: {info[0]["s5"]}\n")
        arquivo_sensores.write(f"Sensor 6: {info[0]["s6"]}\n")
        arquivo_sensores.write(f"Sensor 7: {info[0]["s7"]}\n")
        arquivo_sensores.write(f"Sensor 8: {info[0]["s8"]}\n")    


if __name__ == "__main__":
    mudar_parametros_experimento()
    start_server()






