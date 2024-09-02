# MassFlowUnit
Pacote com scripts para interação com válvulas MassFlow. Inclui:
    [1] MassFlowUnit, classe para comunicação simples com MassFlow utilizando pyserial.
    [2] Orquestrador, classe para controle simultâneo de multiplas instancias de MassFlowUnit.
    [3] MassFlowSrv, servidor para manipulação do orquestrador.
    [4] MassFlowClient, cliente para envio de comandos ao servidor.
    [5] InterprocessValueHandlerSrv[IPVH], servidor para armazenamento das variávies compartilhadas entre os processos.
    [6] ArduinoSensorStatus, script para obter valores dos sensores via arduino.
    [7] ExpView, monitor de visualização em tempo real das variáveis do experimento...

O arquivo 'parametros.json' guarda os dados de abertura/execução de fluxo...
