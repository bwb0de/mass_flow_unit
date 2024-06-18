from mass_flow_unit import MassFlowUnit
from multiprocessing import Process

baud_rate = 9600

mass_flow_unit1 = MassFlowUnit('COM4', baud_rate)
mass_flow_unit2 = MassFlowUnit('COM5', baud_rate)

lista_arquivos_rotina1 = ['/home/danielc/Documentos/Devel/GitHub/mass_flow_unit/arquivos_de_rotinas/sequencia_argumentos.json']
lista_arquivos_rotina2 = ['/home/danielc/Documentos/Devel/GitHub/mass_flow_unit/arquivos_de_rotinas/sequencia_argumentos2.json']


def executa_subprocesso(objeto: MassFlowUnit, argumento):
    resultado = objeto.executar_arquivos_de_rotina_sequencialmente(argumento)
    return resultado


if __name__ == "__main__":
    instancias = [
        mass_flow_unit1, 
        mass_flow_unit2
    ]

    argumentos = [
        lista_arquivos_rotina1,
        lista_arquivos_rotina2,
    ]

    processos = []

    for instancia, argumento in zip(instancias, argumentos):
        processo = Process(target=executa_subprocesso, args=(instancia, argumento))
        processos.append(processo)
        processo.start()
