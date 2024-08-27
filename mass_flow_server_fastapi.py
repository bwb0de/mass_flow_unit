import time
import socket

from mass_flow_unit import MassFlowUnitTest
from orquestrador_mass_flow_v2 import Orquestrador
from fastapi import FastAPI

app = FastAPI()

taxa_de_transmissao = 9600

mu1 = MassFlowUnitTest('COM3', 9600, 100, 'produto')
mu2 = MassFlowUnitTest('COM4', 9600, 200, 'Ar')
mu3 = MassFlowUnitTest('COM5', 9600, 200, 'Ar')


o1 = Orquestrador([mu1, mu2, mu3])

lista_fluxo_nao_ar_tempo = [
    (0,10),
    (6,10),
    (0,10),
    (12,10),
    (0,10),
    (24,10),
    (0,10),
    (36,10),
    (0,10),
    (48,10),
]

o1.distribuir_fluxo_nas_unidades(lista_fluxo_nao_ar_tempo)


@app.get('/run')
def executar():
    o1.executar_rotina()
    return {'message': 'iniciando execução das rotinas...'}

@app.get('/check')
def executar():
    resposta = o1.status_das_rotinas_em_execucao()
    return {'message': resposta}

@app.get('/stop')
def parar():
    o1.interromper()
    return {'message': 'execução interrompida...'}








