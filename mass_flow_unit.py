import serial
import time
import json


### Funções de execução
# enviar_comandos
# enviar_comando
# executar_arquivos_de_rotina_psp_sequencialmente


class MassFlowUnit:
    def __init__(self, port_add, baud_rate, flux_max_v=100, timeout=1) -> None:
        self.flux_max_v = flux_max_v
        self.port_add = port_add
        self.baud_rate = baud_rate
        self.routine_file = None
        
        self.alarm_st_translator = {
            "D": "Disabled",
            "N": "Normal",
            "H": "High",
            "L": "Low"
        }
        self.totalizer_status_translator = {
            "D": "Disabled",
            "E": "Enabled",
        }
        self.analog_output_translator = {
            "0": "0-5 Vdc",
            "1": "0-10 Vdc",
            "2": "4-20 mA",
        }
        self.mod_buss_translator = {
            "0": "Installed",
            "1": "Not installed",
        }

        # Testar, aparentemente com o código vigente o hex precisa possuir 4 digitos ex: '0xaaaa' verificar tamanho de retorno do equipamento
        self.alarm_events_register = {
            0: "High Flow Alarm",
            1: "Low Flow Alarm",
            2: "Flow Between High and Low Limits",
            3: "Totalizer#1 Exceed Set Event Volume Limit",
            4: "Totalizer#2 Exceed Set Event Volume Limit",
            5: "High Pressure Alarm",
            6: "Low Pressure Alarm",
            7: "Pressure between High and Low Limits",
            8: "Low Temperature Alarm",
            9: "Low Temperature Alarm",
            10: "Temperature Between High and Low Limits",
            11: "Pulse Output Queue overflow",
            12: "Password Event (attempt to change password)",
            13: "Power On Event (power on delay > 0)",
        }

        # Testar, aparentemente com o código vigente o hex precisa possuir 4 digitos ex: '0xaaaa' verificar tamanho de retorno do equipamento
        self.diagnostic_events_register = {
            1: "CPU Temperature Too High",
            2: "DP Sensor Initialization Error",
            3: "AP Sensor Initialization Error",
            4: "2.5 Vdc Reference Out of Range",
            5: "Flow Out of Permissible Range",
            6: "Absolute Pressure over Permissible Range",
            7: "Gas Temperature Out of Range",
            8: "Analog Output Alarm Flag",
            9: "UART Serial Communication Error",
            10: "Modbus Serial Communication Error",
            11: "EEPROM R/W Error",
            12: "Auto Zero Failure Flag",
            13: "AP Tare Failure Flag",
            14: "DP ADC Counts Invalid",
            15: "AP ADC Counts Invalid",
            16: "Fatal Error",
        }


        self.setpoint_saved_routine = [
           (0.0, 1),
           (0.0, 1000),
           (1.0, 1),
           (1.0, 500),
           (0.0, 1),
           (0.0, 500),
           (5.0, 1),
           (5.0, 500),
           (0.0, 1),
           (0.0, 500),
           (25.0, 1),
           (25.0, 500),
           (0.0, 1),
           (0.0, 500),
           (100.0, 1),
           (100.0, 500)
         ]

    def criar_rotina_de_setpoints_psp(self, command_args: list, loops: int = 1):
        psp_base = [
            'M:P',           #Inicia program set_point
            'VM:C',          #Fecha a válvula
            'AIM:2',         #Define novo modo de input analógico
            'PSM:E',         #Habilita modo PSP (program set point) (16) slots
            'PSC:S.01',      #Habilita modo PSP (program set point) (16) slots
            'PSL:E',         #Habilita modo loop do PSP
            'PSA:0xFFFF'     #Habilita modo loop do PSP
        ]

        command_args_extended = []

        while loops:
            command_args_extended.extend(command_args)
            loops -= 1

        rotina = {}
        output_wait_time = []

        output = []
        output.extend(psp_base)

        n = 1
        arguments_pending = len(command_args_extended)
        wait_time = 0

        for percent_arg, time_arg in command_args_extended:
            n_str = str(n).zfill(2)
            wait_time += int(time_arg)
            output.append(f'PSP{n}:{percent_arg},{time_arg}')
            n += 1
            arguments_pending -= 1
            if n == 17 and arguments_pending > 0:
                output.append('PSC:R')
                output.extend(psp_base)
                output_wait_time.append(wait_time)
                wait_time = 0
                n = 1

        output.append('PSC:R')
        output_wait_time.append(wait_time)

        rotina['commands'] = output
        rotina['wait_time'] = output_wait_time

        return rotina        

    def executar_rotina_de_comandos(self, command_routine):
        assert isinstance(command_routine, dict)
        assert not command_routine.get('commands') is None
        assert not command_routine.get('wait_time') is None

        print(f"MassFlowUnit em '{self.port_add}' {time.ctime()}: iniciando rotina!")

        commands = command_routine['commands']
        wait_time = command_routine['wait_time']
        wait_step = 0

        sequencia_comandos_para_envio = []
        numero_comandos_executados = 0
        numero_total_comandos = len(commands)

        for command in commands:
            sequencia_comandos_para_envio.append(command)
            numero_comandos_executados += 1
            if command == 'PSC:R':
                print(f"MassFlowUnit em '{self.port_add}' {time.ctime()}: executando {numero_comandos_executados} de {numero_total_comandos} [{(numero_comandos_executados/numero_total_comandos)*100:.2f}%], tempo espera {wait_time[wait_step]}s...")
                v = self.enviar_comandos(sequencia_comandos_para_envio)
                if v == 'Erro': return
                time.sleep(wait_time[wait_step])
                wait_step += 1
                sequencia_comandos_para_envio = []

        v = self.enviar_comandos(sequencia_comandos_para_envio)
        if v == 'Erro': return

        print(f"MassFlowUnit em '{self.port_add}' {time.ctime()}: rotina concluída!")

    def definir_arquivo_de_rotina_alvo(self, caminho_para_arquivo):
        self.routine_file = caminho_para_arquivo

    def executar_arquivo_de_rotina(self):
        with open(self.routine_file, 'r') as f:
            conteudo = f.read()
            conteudo = json.loads(conteudo)
            assert not conteudo.get('loops') is None, "Arquivo em formato incorreto... Possui o campo 'loops'?"
            assert not conteudo.get('argumentos') is None, "Arquivo em formato incorreto... Possui o campo 'argumentos'?"
            rotina = self.criar_rotina_de_setpoints_psp(conteudo['argumentos'], loops=conteudo['loops'] )
            self.executar_rotina_de_comandos(rotina)

    def executar_arquivos_de_rotina_psp_sequencialmente(self, aquivos_de_rotina: list):
        assert isinstance(aquivos_de_rotina, list), "O argumento 'arquivos_de_rotina' deve ser uma lista com caminhos válidos para os arquivos de rotina..."

        for caminho_para_arquivo in aquivos_de_rotina:
            self.definir_arquivo_de_rotina_alvo(caminho_para_arquivo)
            self.executar_arquivo_de_rotina()

    def executar_rotina_padrao(self):
        rotina = self.criar_rotina_de_setpoints_psp(self.setpoint_saved_routine)
        self.executar_rotina_de_comandos(rotina)

    def enviar_comandos(self, commandos: list):

        if commandos == []: return

        try:
            with serial.Serial(self.port_add, self.baud_rate, timeout=1) as ser:
                respostas = []
                for cmd in commandos:
                    comando_teste = bytes(f'{cmd}\r\n', 'utf-8')
                    ser.write(comando_teste)
                    resposta = ser.readline().decode().strip()
                    respostas.append((cmd, resposta))
                return respostas

        except serial.SerialException as e:
            print(f"Erro ao conectar na porta serial: {e}")    
            return "Erro"    

    def enviar_comando(self, comando: str):
        try:
            with serial.Serial(self.port_add, self.baud_rate, timeout=1) as ser:
                comando_teste = bytes(f'{comando}\r\n', 'utf-8')  
                ser.write(comando_teste)
                resposta = ser.readline().decode().strip()
                return resposta

        except serial.SerialException as e:
            print(f"Erro ao conectar na porta serial: {e}")        

    def decodificar_valor_hexadecimal_de_alarm_or_diagnostic_ev_register(self, hex_value, alarm_event_mapping):
        
        #Verificar no manual
        
        """
        Decodifica o valor hexadecimal com base no alarm_event_mapping.
        
        :param hex_value: Hexadecimal value as a string (e.g., '0x05')
        :param event_mapping: Dictionary mapping bit positions to event descriptions
        :return: List of active events
        """
        
        # Convertendo de string_hex para binário
        binary_value = bin(int(hex_value, 16))[2:].zfill(8)
        print(binary_value)
        binary_value = binary_value[::-1]
        print(binary_value)
        print("Size",len(binary_value))
    
        eventos_ativos = []
        for bit_pos, event_desc in alarm_event_mapping.items():
            print(bit_pos)
            if binary_value[bit_pos] == '1':
                eventos_ativos.append(event_desc)
        
        return eventos_ativos
    
    def decodificar_diagnostic_event(self, hex_value_str):
        return self.decodificar_valor_hexadecimal_de_alarm_or_diagnostic_ev_register(hex_value_str, self.diagnostic_events_register)

    def decodificar_alarm_event(self, hex_value_str):
        return self.decodificar_valor_hexadecimal_de_alarm_or_diagnostic_ev_register(hex_value_str, self.alarm_events_register)

    def obter_estado_equipamento(self): #Pendente
        r_di = self.enviar_comando(["pi"])
        r_pi = self.enviar_comando("di").split(',')
        r_pulse = self.enviar_comando("p:s")
        r_v = self.enviar_comando("v")
        r_totalizer1 = self.enviar_comando("t1s")
        r_totalizer2 = self.enviar_comando("t2s")

        return r_di, r_pi, r_pulse, r_v, r_totalizer1, r_totalizer2

        #mass_flow, volumetric_flow, total_meu_1, total_meu_2, gas_temp, gas_press, flow_alarm_st, temp_alarm_st, press_alarm_st, alarm_ev_register, diagnostic_ev_register = r_pi
        #gas_idx, gas_name, current_mass_eng_unit, current_volum_eng_unit, totalizer1_mode, totalizer2_mode, analog_output, mod_buss = r_di
        #pulse_mode, flow_start, unit_per_pulse, pulse_time_interval = r_pulse 
        #_, start_flow_condition1, limit_volume1, pow_on_delay1, autoreset_mode1, autoreset_delay1 = r_totalizer1
        #_, start_flow_condition2, limit_volume2, pow_on_delay2, autoreset_mode2, autoreset_delay2 = r_totalizer2

        resposta = {
            "Mass Flow": float(mass_flow),
            "Volumetric Flow": float(volumetric_flow),
            "Total1 MEU": float(total_meu_1),
            "Total2 MEU": float(total_meu_2),
            "Temperatura Gás": float(gas_temp), #Firehaint?
            "Pressão Gás": float(gas_press),
            "Situação Alarme Flow": self.alarm_st_translator[flow_alarm_st],
            "Situação Alarme Temperatura": self.alarm_st_translator[temp_alarm_st],
            "Situação Alarme Pressão": self.alarm_st_translator[press_alarm_st],
            "Alarm Event Register": alarm_ev_register, #Tradutor hexcode
            "Diagnostic Event Register": diagnostic_ev_register, #Tradutor hexcode
            "Gás Index": gas_idx,
            "Gás Name": gas_name,
            "Current Mass Unit":current_mass_eng_unit,
            "Current Volumetric Unit": current_volum_eng_unit,
            "Analog Output": self.analog_output_translator[analog_output],
            "ModBuss": self.mod_buss_translator[mod_buss],
            "Valve Info": r_v,
            "Pulse Mode": pulse_mode,
            "Pulse Flow Start": flow_start,
            "Pulse Unit per Pulse": unit_per_pulse,
            "Pulse Time Interval [25-3276ms]": pulse_time_interval,
            "Totalizer #1 Mode": self.totalizer_status_translator[totalizer1_mode],
            "Totalizer #1 Start Flow Condition": start_flow_condition1,
            "Totalizer #1 Limit Volume": limit_volume1,
            "Totalizer #1 Pow on Delay": pow_on_delay1,
            "Totalizer #1 Autoreset Mode": autoreset_mode1,
            "Totalizer #1 Autoreset Delay": autoreset_delay1,
            "Totalizer #2 Mode": self.totalizer_status_translator[totalizer2_mode],
            "Totalizer #2 Start Flow Condition": start_flow_condition2,
            "Totalizer #2 Limit Volume": limit_volume2,
            "Totalizer #2 Pow on Delay": pow_on_delay2,
            "Totalizer #2 Autoreset Mode": autoreset_mode2,
            "Totalizer #2 Autoreset Delay": autoreset_delay2,
        }


        return resposta

