import json
import time
import os
import shutil

from multiprocessing import Process
from nucleo.devices.arduino_unit import ArduinoUnit

from .paths import units_arduino_info_folder

class Orquestrador:
    def __init__(self, arduino_units:list=[]) -> None:
        self.unidades = []
        self.unit_status = {}


    @property
    def unidades(self) -> list:
        return self.unidades
    

    @property
    def unidades_info(self) -> None:
        for unit in self.unidades:
            print(f'Arduino ID: {unit.numero_equipamento}')
            print(f'Porta: {unit.porta_de_conexao}')
            print(f'Taxa de transmissão: {unit.porta_de_conexao}')
            print('')
    


def executa_subprocesso(objeto: ArduinoUnit):
    pass