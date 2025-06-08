# e-Nose orquestrator
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
    [9] Scripts .py: [a] finalização servidor ipvh_srv, [b] construção de tabela resultados


## Como o conjunto funciona?

### Visão geral e arquivos de configuração

O ponto de entrada do aplicativo é o arquivo 'main.py' que inicializar o servidor Flask.

Os dados de configuração do equipamento e do experimento estão na pasta 'config'. Parte das configurações como os dados do 'experimento' e os 'parâmetos de fluxo' podem ser acessados pela interface web do e-Nose. 

Ao editar os parâmetros é necessário definir, no primeiro campo do formulário, a quantidades de alterações de fluxo que representam um ciclo. Isso é importante para que ao final do ciclo seja feito o registro do caractere de corte nos dados, representado por uma '@'.

Na edição das informações da experiência, o 'nome do pesquisador' define o nome da pasta de saída onde os dados são gravados. A pasta raiz de destino pode ser definida dentro do arquivo 'ipvh_srv.py', as informações de configuração serão extratidas para um arquivo do tipo .env no futuro.

Na pasta de registro dos dados as informações são salvas em subpastas com a data e hora do início do experimento. Há um arquivo de informações, no formato texto, criado com as informações do experimento, e um arquivo '.json' quando o servidor 'ipvh_srv.py' é inicializado. Ao iniciar o experimento é importante observar se a pasta de destino onde os dados serão salvos foi devidamente criada antes de permitir que toda a rotina seja executada. Se a pasta não tiver sido criada, observe se há mensagens de erro no console. Caso não exista informações de erro no console, finalize o experimento e reinicie reinicie o arquivo 'main.py'.

Ao modificar as portas de conexão dos dispositivos, verifique no sistema operacional seus respectivos valores para que essas informações sejam atualizadas nos arquivos de configuração 'arduino.json', 'lcr.json' e 'mass_flow.json'. A estrutura de organização de dados desses arquivos não deve ser alterada. A título de informação a estrutura dos arquivos são as seguintes: 

#### arduino.json

```
[
    {
        "nome": "Sensores",
        "modelo": "uno",
        "porta": "COM10",
        "taxa_de_transmissao": 9600,
        "tempo_espera": 3
    }
]
```

#### lcr.json

```
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
```

#### mass_flow.json

```
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
```

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

### Estrutura do projeto

```
.
│ 
│   [informaçãoes dos dispositivos]
├── config 
│   ├── arduino.json
│   ├── experimento.json
│   ├── lcr.json
│   ├── mass_flow.json
│   └── parametros.json
│ 
│ 
│   [dados de execução dos dospositivos e log]
├── dados_execucao
│   ├── arduino_data
│   │   └── unit_status
│   │       └── 1.json
│   ├── lcr_data
│   │   └── unit_status
│   │       └── 1.json
│   └── mass_flow_data
│       └── unit_status
│           ├── 608314-1.json
│           ├── 608315-1.json
│           └── 624644-1.json
│ 
│ 
│ 
│   [classes dos dispositivos, IPVH server, Orquestrador e scripts]
├── nucleo
│   ├── classes
│   │   └── construtor.py [!não implementado/integrado]
│   ├── construtor_tabela_resultados.py
│   ├── devices
│   │   ├── arduino_unit.py
│   │   ├── lcr_unit.py
│   │   └── mass_flow_unit.py
│   ├── globals
│   │   ├── logger.py
│   │   └── paths.py
│   ├── ipvh_srv.py
│   ├── kill_ipvh_srv.py
│   ├── mass_flow_client.py
│   ├── mass_flow_info_reader.py
│   ├── orquestrator_parallel.py
│   ├── orquestrator_setup.py
│   └── update_experiment_info.py
│ 
│ 
│   [material de consulta sobre dispositivos e código do Arduino]
├── resources
│   ├── Arduino_Serial
│   │   └── Arduino_Serial.ino
│   ├── dpc_manual.pdf
│   └── notes.md
│ 
│ 
│   [pasta para conteúdo estático do Flask]
├── static
│   ├── css
│   │   └── pearl_style_compilado.min.css
│   ├── img
│   │   ├── check.svg
│   │   ├── copy-to.png
│   │   ├── cross.svg
│   │   ├── favicon.ico
│   │   └── menu-burger.svg
│   └── js
│       ├── api_call.js
│       ├── my_js_modules.js
│       └── my_script.js
│ 
│ 
│   [página com templates do Flask]
├── templates
│   ├── about.html
│   ├── footer.html
│   ├── form.html
│   ├── formulario_arduino.html
│   ├── formulario_experimento.html
│   ├── formulario_lcr.html
│   ├── formulario_rotina.html
│   ├── index.html
│   ├── layout.html
│   ├── manutencao.html
│   ├── message.html
│   ├── monitor.html [!não implementado, depende e construtor]
│   └── navbar.html
│ 
│ 
│   [arquivos para testagem a partir da linha de comando]
├── teste_arduino.py
├── teste_experimento.py
├── teste_graf.py
├── teste_inicializar_dispositivos.py
├── teste_ipvh_srv.py
├── teste_lcr2.py
├── teste_lcr-FROM_TH2816B.py
├── teste_lcr.py
├── teste_mass_flow_close.py
├── teste_mass_flow.py
│ 
│ 
│   [scripts de entrada da aplicação e informações do projeto]
├── init.bat
├── main.py
├── pyproject.toml
└── uv.lock
```
19 directories, 67 files
