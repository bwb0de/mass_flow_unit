# MassFlowUnit

ATENÇÃO! 'main' é o ramo de desenvolvimento deste projeto. As diferentes versões estão em ramos nominados como v#. Dessa forma, para utilizar a versão mais recente, clone o repositório principal e, em seguida, troque para o ramo com o número de versão mais alto.

## Informações gerais

Pacote com scripts para interação com válvulas MassFlow. Inclui:
    [1] MassFlowUnit, classe para comunicação simples com MassFlow utilizando pyserial.
    [2] Orquestrador, classe para controle simultâneo de multiplas instancias de MassFlowUnit.
    [3] MassFlowSrv [exp_http_server], servidor para manipulação do orquestrador.
    [4] MassFlowClient [mass_flow_client (cli)], cliente para envio de comandos ao servidor.
    [6] ArduinoSensorStatus, script para obter valores dos sensores via arduino [não implementado]

O arquivo 'parametros.json' guarda os dados de abertura/execução de fluxo...
