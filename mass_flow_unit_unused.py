class MassFlowUnitUnused:
    def __init__(self, porta_de_conexao, taxa_de_transmissao,timeout=1) -> None:
        self.porta_de_conexao = porta_de_conexao
        self.taxa_de_transmissao = taxa_de_transmissao
        self.arquivo_de_rotina = None
        self.numero_equipamento = self.enviar_comando('MR,1')

        if self.numero_equipamento in {'624643-1','608314-1'}:
            self.fluxo_maximo = 100
        elif self.numero_equipamento in {'624644-1','608315-1'}:
            self.fluxo_maximo = 200

        # Ar e não ar...
        if self.numero_equipamento in {'624643-1','608314-1'}:
            self.conteudo_fluxo = 'produto'
        elif self.numero_equipamento in {'624644-1','608315-1'}:
            self.conteudo_fluxo = 'Ar'

        self.fracao_de_fluxo = 100/self.fluxo_maximo
        
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

    #Não usado
    def interromper_execução_psp(self):
        return self.enviar_comandos(['PS,S'])

    #Não usado
    def obter_configuracoes_psp_correntes(self, verbose=False):
        resultados = self.enviar_comandos([
            'PS,P,1',
            'PS,P,2',
            'PS,P,3',
            'PS,P,4',
            'PS,P,5',
            'PS,P,6',
            'PS,P,7',
            'PS,P,8',
            'PS,P,9',
            'PS,P,10',
            'PS,P,11',
            'PS,P,12',
            'PS,P,13',
            'PS,P,14',
            'PS,P,15',
            'PS,P,16'
        ])

        if verbose:
            print(f'MassFlowUnit, em {self.porta_de_conexao}:')
            for comando, resposta in resultados:
                print(f' - {resposta}')        

        return resultados

    #Não usado
    def criar_rotina_de_setpoints_psp(self, command_args: list, loops: int = 1):
        psp_base = [

           #'M,D',    #'M,D': Interface digital, 'M,A': interface analógica, 'M,L': local interface, ''
            'M,P',    #Inicia program set_point
            'V,M,C',  #Fecha a válvula
            'PS,M,E', #Habilita modo PSP
            'PS,L,E', #Habilita modo loop do PSP
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
            output.append(f'PS,P,{n},{percent_arg},{time_arg}')
            n += 1
            arguments_pending -= 1
            if n == 17 and arguments_pending > 0:
                output.append('PS,A,0xFFFF')
                output.append('PS,P,R')
                output.extend(psp_base)
                output_wait_time.append(wait_time)
                wait_time = 0
                n = 1

        output.append('PS,P,R')
        output_wait_time.append(wait_time)

        rotina['commands'] = output
        rotina['wait_time'] = output_wait_time

        return rotina        

    #Não usado
    def executar_rotina_de_comandos(self, command_routine):
        assert isinstance(command_routine, dict)
        assert not command_routine.get('commands') is None
        assert not command_routine.get('wait_time') is None

        print(f"MassFlowUnit em '{self.porta_de_conexao}' {time.ctime()}: iniciando rotina!")

        commands = command_routine['commands']
        wait_time = command_routine['wait_time']
        wait_step = 0

        sequencia_comandos_para_envio = []
        numero_comandos_executados = 0
        numero_total_comandos = len(commands)

        for command in commands:
            sequencia_comandos_para_envio.append(command)
            numero_comandos_executados += 1
            if command == 'PS,P,R':
                print(f"MassFlowUnit em '{self.porta_de_conexao}' {time.ctime()}: executando {numero_comandos_executados} de {numero_total_comandos} [{(numero_comandos_executados/numero_total_comandos)*100:.2f}%], tempo espera {wait_time[wait_step]}s...")
                v = self.enviar_comandos(sequencia_comandos_para_envio)
                if v == 'Erro': return
                time.sleep(wait_time[wait_step])
                wait_step += 1
                sequencia_comandos_para_envio = []

        v = self.enviar_comandos(sequencia_comandos_para_envio)
        if v == 'Erro': return

        print(f"MassFlowUnit em '{self.porta_de_conexao}' {time.ctime()}: rotina concluída!")

    #Não usado
    def definir_arquivo_de_rotina_alvo(self, caminho_para_arquivo):
        self.arquivo_de_rotina = caminho_para_arquivo

    #Não usado
    def executar_arquivo_de_rotina(self):
        with open(self.arquivo_de_rotina, 'r') as f:
            conteudo = f.read()
            conteudo = json.loads(conteudo)
            assert not conteudo.get('loops') is None, "Arquivo em formato incorreto... Possui o campo 'loops'?"
            assert not conteudo.get('argumentos') is None, "Arquivo em formato incorreto... Possui o campo 'argumentos'?"
            rotina = self.criar_rotina_de_setpoints_psp(conteudo['argumentos'], loops=conteudo['loops'] )
            self.executar_rotina_de_comandos(rotina)

    #Não usado
    def executar_arquivos_de_rotina_psp_sequencialmente(self, aquivos_de_rotina: list):
        assert isinstance(aquivos_de_rotina, list), "O argumento 'arquivos_de_rotina' deve ser uma lista com caminhos válidos para os arquivos de rotina..."

        for caminho_para_arquivo in aquivos_de_rotina:
            self.definir_arquivo_de_rotina_alvo(caminho_para_arquivo)
            self.executar_arquivo_de_rotina()

    #Não usado
    def executar_rotina_padrao(self):
        rotina = self.criar_rotina_de_setpoints_psp(self.setpoint_saved_routine)
        self.executar_rotina_de_comandos(rotina)

    #Não usado
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
    
    #Não usado
    def decodificar_diagnostic_event(self, hex_value_str):
        return self.decodificar_valor_hexadecimal_de_alarm_or_diagnostic_ev_register(hex_value_str, self.diagnostic_events_register)

    #Não usado
    def decodificar_alarm_event(self, hex_value_str):
        return self.decodificar_valor_hexadecimal_de_alarm_or_diagnostic_ev_register(hex_value_str, self.alarm_events_register)

