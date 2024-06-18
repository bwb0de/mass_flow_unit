import serial

# Substitua 'COM3' pela porta COM correta do seu computador
porta_serial = 'COM4'  
baud_rate = 9600  # Verifique a taxa de transmissão correta no manual do DPC

try:
    with serial.Serial(porta_serial, baud_rate, timeout=1) as ser:
        # Comando de teste (substitua pelo comando correto do seu DPC)
        n = 0
        while True:
            n += 1
            if n % 2 == 0:
                comando_teste = b'gt\r\n'  
            else:
                comando_teste = b'di\r\n'  

            ser.write(comando_teste)

            # Lê a resposta do controlador
            resposta = ser.readline().decode().strip()
            print(f"{resposta}")

except serial.SerialException as e:
    print(f"Erro ao conectar na porta serial: {e}")

