Comandos de configuração básica para setpoint

[
    'M:P',           #Inicia program set_point
    'VM:C',          #Fecha a válvula
    'AIM:2',         #Define novo modo de input analógico
    'PSM:E',         #Habilita modo PSP (program set point) (16) slots
    'PSC:S.01',      #Habilita modo PSP (program set point) (16) slots
    'PSL:E',         #Habilita modo loop do PSP
    'PSA:0xFFFF'     #Habilita modo loop do PSP
]

[    
    'PSP01:0.0,1',    
    'PSP02:0.0,1000',    
    'PSP03:1.0,1',    
    'PSP04:1.0,500',    
    'PSP05:0.0,1',    
    'PSP06:0.0,500',    
    'PSP07:5.0,1',    
    'PSP08:5.0,500',    
    'PSP09:0.0,1',    
    'PSP10:0.0,500',    
    'PSP11:25.0,1',    
    'PSP12:25.0,500',    
    'PSP13:0.0,1',    
    'PSP14:0.0,500',    
    'PSP15:100.0,1',    
    'PSP16:100.0,500',    
]


Usar PSC:R para executar...

1. To get currently selected Gas: !12,G<CR>
The DPC will reply: !12,G:0,AIR<CR>
(assuming the Current Gas is #0, calibrated for AIR)

2. To get current Flow Rate Alarm status:
!12,FA,R<CR>
The DPC will reply: !12,FAR:N<CR> (assuming no flow alarm conditions)

3. To get a mass and volumetric flow reading:
!12,F<CR>
The DPC will reply: !12,50.0,50.3<CR> (assuming the mass flow is at 50% FS)

4. Set the Set Point to 100.0 % full scale:
!12,SP,100.0<CR>
The DPC will reply: !12,SP:100.0<CR>

5. Set the High and Low Flow Alarm limit to 90% and 10% of Full Scale flow rate:
!12,FA,C,90.0,10.0<CR>
The DPC will reply: !12,90.00,10.00,<CR>


Executar, uma vez, rotina para obter lista de gases configurados. Indice vai de [0-128] salvar essas valores em um dict/json.
    Não necessário: Página 33-39 do manual

    Sequência comandos:
        json = {}
        for n in range(0,129):
            G:n
            return val G => json (inverter chave/valor para legibilidade humana; reinverter para enviar número à máquina)



Apresentar todas essas informações na tela de escolha
    Executar rotinas ao iniciar o script para anotar parâmetros do equipamento:
        Comandos:
            F   ·· Retorna dois valores  [testar se estes valores etão em PI, index <MF> e <VF>]
              "Mass Flow","Volumétric Flow"

            PI  ·· Retorna uma tupla de valores separado por vírgula
              <MF>,
              <VF>,
              <Total#1 Value> [MEU],
              <Total#2 Value> [MEU],
              <Gas Temperature>,
              <Gas Pressure>,
              <Flow Alarm Status>,         [valores possíveis D,N,H,L; respectivamente Desativado, Normal, Alto e Baixo]
              <Temp. Alarm Status>,        [valores possíveis D,N,H,L; respectivamente Desativado, Normal, Alto e Baixo]
              <Press. Alarm Status>,       [valores possíveis D,N,H,L; respectivamente Desativado, Normal, Alto e Baixo]
              <Alarm Events Register>,     hex
              <Diagnostic Events Register> hex

              Exemplo: 25.4,23.2,354.2,0.0,24.8,14.95,D,N,D,0x0,0x0
            
            DI  ·· Lê informações de configuração do dispositivo.
              <Current Gas Idx>,
              <Current Gas Name>,
              <Full Scale Range> (L/min),
              <Current MEU>,
              <Current VEU>,
              <Totalizer#1 mode>,       [valores podem ser E, para 'Enabled' ou D, para 'Disabled']
              <Totalizer#2 mode>,
              <Analog Output>,          [valores de 0-2, respectivamente: 0-5 Vdc, 0-10 Vdc, 4-20 mA]
              <ModBus>                  [valores de 0 ou 1, respectivamente: Instalado, Não instalado]
              
              Exemplo: DI:5,Helium,0.200,Sml/min,ml/min,E,D,0,1

            PS .. retorna configurações de pulso corrente
              <Mode> [E, D]
              <FlowStart>
              <Unit/Pulse>
              <PulseTimeInterval>

            



Device info, obtem todas as informações do dispositivo
    => DI

Ler e escrever parâmetros de uma mistura de gases (p.108)
    => CM [obtem a informação dos gases salvos na EEPROM] os índices de alocação variam entre [200-219], 20 slots
    => 


Pulse Output (p.96)
    => P

Totalizar (existem 2)
    => T#<arg> .. o valor de # deve ser substituído por 1 ou 2. 

      args:
      Z -> Zera ou reseta o valor (não pode ser resetado se reset lock estiver ativado -> 1)
      R -> Obtém valor corrente do volume lido
      L -> Obtém status do lock...
      L:n -> Define status do lock... 1 -> Travado; 0 -> Destravado

      <TotalizerMode> []
      <StartFlow>
      <LimitVolume>
      <PowOnDelay>
      <AutoResetMode> [0 - Disable, 1 - Enable]
      <AutoResetDelay>


================================================================================================================
Valve control (p.104) <!!! Do not change these parameters. Consult factory technical support for more info.>
    => V [sem arg, configurações correntes]
    
    => V<Arg>
    
    => VM:[n] =>
        n = C => Fechado
        n = A => Automático
        n = O => Aberto

    => VPR [restaura definições de fábrica]
================================================================================================================


Definição das unidades de medida do fluxo de massa (Mass Flow):
    => U [sem argumento, retorna a unidade corrente].

Definição das unidades de medida do fluxo volumétrico (Volumetric Flow):
    => VU [sem argumento, retorna a unidade corrente].


Calibração (p.99)
    => CS:<TempV>,<PressV>
    => CS
    => Definição de fábrica: S:70.0,14.696 [?] não seria CS:70.0,14.696





Read EEPROM Memory
    => MR<Arg>

    O argumento varia entre 0 e 413 e o retorno é um valor de memória. Pode ser usado para faze um backup dos valores da EEPROM...
    Se fizer essa operação, realizar com intervalos de consulta de 1 minuto. Na página 107 consta um aviso de risco de queima da EEPROM para
    operações de escrita usando o comando Local Set Point Options



UART Error Codes:
1 – Command Not Supported or Back Door is not enabled.
2 – Wrong# of Arguments
3 – Address is Out of Range (MR or MW commands)
4 – Wrong# of the characters in the Argument
5 – Attempt to alter Write-Protected Area in the EEPROM
6 – Proper Command or Argument not found
7 – Wrong value of the Argument
8 – Manufacturer-specific information EE access KEY (wrong key or key is disabled)


Alarm Events codes and bit position:
Code Event Description Bit position
0 FLOW_ALARM_HIGH 0x0001
1 FLOW_ALARM_LOW 0x0002
2 FLOW_ALARM_RANGE 0x0004
3 TOTAL1_HIT_LIMIT 0x0008
4 TOTAL2_HIT_LIMIT 0x0010
5 PRES_ALARM_HIGH 0x0020
6 PRES_ALARM_LOW 0x0040
7 PRES_ALARM_RANGE 0x0080
8 TEMP_ALARM_HIGH 0x0100
9 TEMP_ALARM_LOW 0x0200
A TEMP_ALARM_RANGE 0x0400
B PULSE_OUT_QUEUE 0x0800
C PASSWORD_EVENT 0x1000
D POWER_ON_EVENT 0x2000


Diagnostic Events codes and bit position:
Code Event Description Bit position
0 CPU_TEMP_HIGH 0x0001
1 DP EE INIT ERROR 0x0002
2 AP EE INIT ERROR 0x0004
3 VREF_OUT_OF_RANGE 0x0080
4 FLOW ABOVE LIMIT 0x0010
5 AP OUT OF RANGE 0x0020
6 G TEMP OUT OF RANGE 0x0040
7 ANALOG OUT ALARM 0x0080
8 SER COMM FAILURE 0x0100
9 MB COMM FAILURE 0x0200
A EEPROM FAILURE 0x0400
B AUTOZERO FAILURE 0x0800
C AP TARE FAILURE 0x1000
D DP PRESSURE INVALID 0x2000
E AP PRESSURE INVALID 0x4000
F FATAL_ERROR 0x8000
