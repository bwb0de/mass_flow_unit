import serial

class MassFlowUnit:
    def __init__(self, port_add, baud_rate, flux_max_v=100, timeout=1) -> None:
        self.__mass_flow_unit = serial.Serial(port_add, baud_rate, timeout=1)
        self.__flux_max_v = flux_max_v
        self.__port_add = port_add
        self.__baud_rate = port_add
        
        self.__alarm_st_translator = {
            "D": "Disabled",
            "N": "Normal",
            "H": "High",
            "L": "Low"
        }
        self.__totalizer_status_translator = {
            "D": "Disabled",
            "E": "Enabled",
        }
        self.__analog_output_translator = {
            "0": "0-5 Vdc",
            "1": "0-10 Vdc",
            "2": "4-20 mA",
        }
        self.__mod_buss_translator = {
            "0": "Installed",
            "1": "Not installed",
        }

        # Testar, aparentemente com o código vigente o hex precisa possuir 4 digitos ex: '0xaaaa' verificar tamanho de retorno do equipamento
        self.__alarm_events_register = {
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
        self.__diagnostic_events_register = {
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

    def verificar_conexao(self):
        if self.__mass_flow_unit.is_open: print(f"MassFlow Device em {self.__port_add} at {self.__baud_rate} baud."); return
        print(f"Falha ao conectar na porta {self.__port_add}.")

    def enviar_comando(self, commando):
        self.__mass_flow_unit.write(commando.encode())
        self.__mass_flow_unit.flush()
        response = self.__mass_flow_unit.readline().decode().strip()
        return response

    def __decodificar_valor_hexadecimal_de_alarm_or_diagnostic_ev_register(self, hex_value, alarm_event_mapping):
        
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
        return self.__decodificar_valor_hexadecimal_de_alarm_or_diagnostic_ev_register(hex_value_str, self.__diagnostic_events_register)

    def decodificar_alarm_event(self, hex_value_str):
        return self.__decodificar_valor_hexadecimal_de_alarm_or_diagnostic_ev_register(hex_value_str, self.__alarm_events_register)


    def obter_estado_equipamento(self):
        r_di = self.enviar_comando("pi").split(',')
        r_pi = self.enviar_comando("di").split(',')
        r_pulse = self.enviar_comando("ps").split(',')
        r_v = self.enviar_comando("v")
        r_totalizer1 = self.enviar_comando("t1s").split(',')
        r_totalizer2 = self.enviar_comando("t2s").split(',')

        mass_flow, volumetric_flow, total_meu_1, total_meu_2, gas_temp, gas_press, flow_alarm_st, temp_alarm_st, press_alarm_st, alarm_ev_register, diagnostic_ev_register = r_pi
        gas_idx, gas_name, current_mass_eng_unit, current_volum_eng_unit, totalizer1_mode, totalizer2_mode, analog_output, mod_buss = r_di
        pulse_mode, flow_start, unit_per_pulse, pulse_time_interval = r_pulse 
        _, start_flow_condition1, limit_volume1, pow_on_delay1, autoreset_mode1, autoreset_delay1 = r_totalizer1
        _, start_flow_condition2, limit_volume2, pow_on_delay2, autoreset_mode2, autoreset_delay2 = r_totalizer2

        resposta = {
            "Mass Flow": float(mass_flow),
            "Volumetric Flow": float(volumetric_flow),
            "Total1 MEU": float(total_meu_1),
            "Total2 MEU": float(total_meu_2),
            "Temperatura Gás": float(gas_temp), #Firehaint?
            "Pressão Gás": float(gas_press),
            "Situação Alarme Flow": self.__alarm_st_translator[flow_alarm_st],
            "Situação Alarme Temperatura": self.__alarm_st_translator[temp_alarm_st],
            "Situação Alarme Pressão": self.__alarm_st_translator[press_alarm_st],
            "Alarm Event Register": alarm_ev_register, #Tradutor hexcode
            "Diagnostic Event Register": diagnostic_ev_register, #Tradutor hexcode
            "Gás Index": gas_idx,
            "Gás Name": gas_name,
            "Current Mass Unit":current_mass_eng_unit,
            "Current Volumetric Unit": current_volum_eng_unit,
            "Analog Output": self.__analog_output_translator[analog_output],
            "ModBuss": self.__mod_buss_translator[mod_buss],
            "Valve Info": r_v,
            "Pulse Mode": pulse_mode,
            "Pulse Flow Start": flow_start,
            "Pulse Unit per Pulse": unit_per_pulse,
            "Pulse Time Interval [25-3276ms]": pulse_time_interval,
            "Totalizer #1 Mode": self.__totalizer_status_translator[totalizer1_mode],
            "Totalizer #1 Start Flow Condition": start_flow_condition1,
            "Totalizer #1 Limit Volume": limit_volume1,
            "Totalizer #1 Pow on Delay": pow_on_delay1,
            "Totalizer #1 Autoreset Mode": autoreset_mode1,
            "Totalizer #1 Autoreset Delay": autoreset_delay1,
            "Totalizer #2 Mode": self.__totalizer_status_translator[totalizer2_mode],
            "Totalizer #2 Start Flow Condition": start_flow_condition2,
            "Totalizer #2 Limit Volume": limit_volume2,
            "Totalizer #2 Pow on Delay": pow_on_delay2,
            "Totalizer #2 Autoreset Mode": autoreset_mode2,
            "Totalizer #2 Autoreset Delay": autoreset_delay2,
        }

        return resposta

