# e-Nose orquestrator

ATENÇÃO! 'main' é o ramo de desenvolvimento deste projeto. As diferentes versões estão em ramos nominados como v#. Dessa forma, para utilizar a versão mais recente, clone o repositório principal e, em seguida, troque para o ramo com o número de versão mais alto.

## Informações gerais

Pacote com para plataforma e-Nose. Inclui:
    [1] MassFlowUnit, classe para comunicação simples com MassFlow utilizando pyserial.
    [2] ArduinoUnit, classe para comunicação com Arduino.
    [3] LCRUnit, classe para comunicação com LCR TH2816B.
    [4] ipvh_srv, script com servidor socket-TCP para acumulo e registro dos dados lidos pelo LCR.
    [5] Orquestrador, script que inicializa o equipamento (MassFlow, Arduino, LCR) e executas as etapas do experimento. 
    [6] FlaskSrv, aplicação web para manipulação.
    [7] Testes de conectividade e execução do experimento.
    [8] Script .BAT de inicialização


## Como o conjunto funciona?

### Visão geral e arquivos de configuração

O ponto de entrada do aplicativo é o arquivo 'main.py' que inicializar o servidor Flask.

Os dados de configuração do equipamento e do experimento estão na pasta 'config'. Parte das configurações como os dados do 'experimento' e os 'parâmetos de fluxo' podem ser acessados pela interface web do e-Nose. 

Ao editar os parâmetros é necessário definir, no primeiro campo do formulário, a quantidades de alterações de fluxo que representam um ciclo. Isso é importante para que ao final do ciclo seja feito o registro do caractere de corte nos dados, representado por uma '@'.

Na edição das informações da experiência, o 'nome do pesquisador' define o nome da pasta de saída onde os dados são gravados. A pasta raiz de destino pode ser definida dentro do arquivo 'ipvh_srv.py', as informações de configuração serão extratidas para um arquivo do tipo .env no futuro.

Na pasta de registro dos dados as informações são salvas em subpastas com a data e hora do início do experimento. Há um arquivo de informações, no formato texto, criado com as informações do experimento, e um arquivo '.json' quando o servidor 'ipvh_srv.py' é inicializado. Ao iniciar o experimento é importante observar se a pasta de destino onde os dados serão salvos foi devidamente criada antes de permitir que toda a rotina seja executada. Se a pasta não tiver sido criada, observe se há mensagens de erro no console. Caso não exista informações de erro no console, finalize o experimento e reinicie reinicie o arquivo 'main.py'.

Ao modificar as portas de conexão dos dispositivos, verifique no sistema operacional seus respectivos valores para que essas informações sejam atualizadas nos arquivos de configuração 'arduino.json', 'lcr.json' e 'mass_flow.json'. A estrutura de organização de dados desses arquivos não deve ser alterada. A título de informação a estrutura dos arquivos são as seguintes: 

#### arduino.json

[
    {
        "nome": "Sensores",
        "modelo": "uno",
        "porta": "COM10",
        "taxa_de_transmissao": 9600,
        "tempo_espera": 3
    }
]

#### lcr.json

[
    {
        "nome": "LCR",
        "porta": "COM5",
        "taxa_de_transmissao": "9600",
        "parity": "N",
        "stopbits": 1,
        "bytesize": 8,
        "timeout": 1,
        "numero_medidas": "10"
    }
]

#### mass_flow.json

[
    {
        "porta": "COM6",
        "taxa_de_transmissao": 9600,
        "fluxo_maximo": 200,
        "conteudo_fluxo": "Ar"
    },
    {
        "porta": "COM7",
        "taxa_de_transmissao": 9600,
        "fluxo_maximo": 200,
        "conteudo_fluxo": "Ar"
    },
    {
        "porta": "COM8",
        "taxa_de_transmissao": 9600,
        "fluxo_maximo": 100,
        "conteudo_fluxo": "produto"
    }
]


Observe que todos arquivos possuem "[]" como delimitador de campo mais externo, isso ocorre devido a possibilidade de configurarmos mais de um dispositivo, muito embora, no momento, com excessão dos dispositivos mass_flow, os dispositicos Arduino e LCR possuam um único comportamento definido.

Nos dispositivos mass_flow, a propriedade 'conteudo_fluxo' é importante para definir o papel do equipamento no experimento. Há no momento apenas dois valores possíveis: "Ar" e "produto".

### Descrição do funcionamento

Antes de iniciar os experimentos recomendamos a edição/atualização das 'informações do experimento' e 'parametros de fluxo', essas informações podem ser editadas pelos seus respectivos formulários na interface web.

Atualizadas as configurações, o aplicativo será redirecionado para a página de início.

O experimento pode ser iniciado ao clicar no botão 'Executar rotina'. A partir desse comando o aplicativo realiza algumas tarefas:
    - configura e inicializa o Orquestrador e os dispositivos como subprocessos autônomos, separados do servidor e-Nose. 
    - inicializar o servidor de coleta de dados 'ipvh_srv.py' como um processo autônomo.
    - carrega o parametros de fluxo repassando ao Orquestrador que, por sua vez, repassa as informações dispositivos MassFlow


Os subprocessos do mass_flow executam um loop com base nos tempos definidos nos parâmetros de fluxo do experimento. A cada invocação do do método '.executar_acao_da_fila()' os subprocessos paralelos avançam para as próximas etapas do experimento. Após a execução de uma dada quantidade de ações arbitrárias, definidas como delimitadora do microciclo da rotina, a classe MassFlowUnit envia ao servidor 'ipvh_srv.py' o sinal '@' para que seja feito um corte nos dados, conforme indicado anteriormente.

O subprocesso Arduino executa um loop independente dos loops dos mass_flow aternando entre os sensores em intervalos fixos de tempo. A cada troca de sensor, o objeto ArduinoUnit, que possui referencia do objeto LCRUnit, aciona o LCR para executar a quantidade de leituras definidas na configuração do lcr.json. Ao obter esses dados, o subprocesso arduino calcula a mediana das leituras e envia os resultados para o servidor 'ipvh_srv.py' como um par de dados 'primary' e 'secundary' associados a um sensor.

O servidor 'ipvh_srv.py' ao receber os dados da classe ArduinoUnit registra as inforamações no arquivo de dados do experimento.

As mudanças de estado relevantes para acompanhar o andamento do experimento em relação aos dispositivos Arduino e do MassFlow e LCR são salvos na pasta 'dados_execucao'. Essas informações de andamento podem ser acessadas pela interface e-Nose ao clicar no botão 'Checar andamento'. 

Na interface e-Nose, se o botão 'Para rotina' for acionado o orquestrador recebe o sinal de interrupção e o subprocesso 'ipvh_srv.py' é finalizado.


