import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 11111
    
    client_socket.connect((host, port))
    while True:
        data_to_send = input("mass_flow ··> ")
        if data_to_send.lower().strip() == 'sair':
            break
        client_socket.send(data_to_send.encode())
        data = client_socket.recv(1024).decode().strip()
        print(data)
    
    client_socket.close()
    

if __name__ == "__main__":
    start_client()
